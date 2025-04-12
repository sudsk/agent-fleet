
import json
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from datetime import datetime
import uuid

from app.models.agent import (
    CreateAgentRequest, UpdateAgentRequest, RegisterAgentRequest,
    AgentResponse, EnvironmentType, AgentStatus
)
from app.database import get_db, Agent, Deployment, AgentTest, AgentMetrics
from app.services.vertex_ai import VertexAIService
from app.services.agent_registry import AgentRegistryService

router = APIRouter()
vertex_service = VertexAIService()
registry_service = AgentRegistryService()

@router.post("/agents", response_model=AgentResponse)
async def create_agent(
    request: CreateAgentRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """Creates a new agent record in the registry."""
    try:
        # Generate agent family ID if not provided
        agent_family_id = request.agentFamilyId or str(uuid.uuid4())
        
        # Create agent in database
        agent = Agent(
            id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            agent_family_id=agent_family_id,
            framework=request.framework.value,
            repository_url=request.repositoryUrl,
            source_hash=request.sourceHash,
            template_id=request.templateId,
            status=AgentStatus.DRAFT.value,
            environment=request.environment.value,
            model_id=request.modelId,
            temperature=request.temperature,
            max_output_tokens=request.maxOutputTokens,
            system_instruction=request.systemInstruction,
            configuration=request.configuration,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(agent)
        db.commit()
        db.refresh(agent)
        
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "agentFamilyId": agent.agent_family_id,
            "framework": agent.framework,
            "repositoryUrl": agent.repository_url,
            "sourceHash": agent.source_hash,
            "templateId": agent.template_id,
            "status": agent.status,
            "environment": agent.environment,
            "modelId": agent.model_id,
            "temperature": agent.temperature,
            "maxOutputTokens": agent.max_output_tokens,
            "systemInstruction": agent.system_instruction,
            "configuration": agent.configuration,
            "createdAt": agent.created_at,
            "updatedAt": agent.updated_at,
            "createdBy": agent.created_by
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")

@router.post("/agents/register", response_model=AgentResponse)
async def register_agent(
    request: RegisterAgentRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Registers an agent from an external source (like Agent Starter Pack CI/CD pipeline).
    Used for integration with external development workflows.
    """
    try:
        # Check if agent family exists, otherwise create new family ID
        agent_family_id = request.agentFamilyId
        if not agent_family_id:
            # Look for existing agents with same name in the same environment
            existing_agent = db.query(Agent).filter(
                Agent.name == request.name,
                Agent.environment == request.environment.value
            ).first()
            
            if existing_agent:
                agent_family_id = existing_agent.agent_family_id
            else:
                agent_family_id = str(uuid.uuid4())
        
        # Create agent in database
        agent = Agent(
            id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            agent_family_id=agent_family_id,
            framework=request.framework.value,
            repository_url=request.repositoryUrl,
            source_hash=request.sourceHash,
            status=AgentStatus.DRAFT.value,
            environment=request.environment.value,
            model_id=request.modelId,
            temperature=request.temperature,
            max_output_tokens=request.maxOutputTokens,
            system_instruction=request.systemInstruction,
            configuration=request.configuration,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(agent)
        
        # If deployment info is provided, create a deployment record
        if request.deploymentInfo:
            deployment = Deployment(
                id=str(uuid.uuid4()),
                agent_id=agent.id,
                deployment_type=request.deploymentInfo.get("deploymentType", "AGENT_ENGINE"),
                version=request.deploymentInfo.get("version", "1.0.0"),
                environment=request.environment.value,
                project_id=request.projectId,
                region=request.region,
                resource_name=request.deploymentInfo.get("resourceName"),
                status="SUCCESSFUL",
                endpoint_url=request.deploymentInfo.get("endpointUrl"),
                deployed_at=datetime.utcnow(),
                configuration=request.deploymentInfo
            )
            
            db.add(deployment)
            
            # Update agent status to DEPLOYED
            agent.status = AgentStatus.DEPLOYED.value
        
        db.commit()
        db.refresh(agent)
        
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "agentFamilyId": agent.agent_family_id,
            "framework": agent.framework,
            "repositoryUrl": agent.repository_url,
            "sourceHash": agent.source_hash,
            "templateId": agent.template_id,
            "status": agent.status,
            "environment": agent.environment,
            "modelId": agent.model_id,
            "temperature": agent.temperature,
            "maxOutputTokens": agent.max_output_tokens,
            "systemInstruction": agent.system_instruction,
            "configuration": agent.configuration,
            "createdAt": agent.created_at,
            "updatedAt": agent.updated_at,
            "createdBy": agent.created_by
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registering agent: {str(e)}")

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    environment: Optional[EnvironmentType] = None,
    status: Optional[AgentStatus] = None,
    framework: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Lists all agents with optional filtering."""
    try:
        # Base query
        query = db.query(Agent)
        
        # Apply filters
        if environment:
            query = query.filter(Agent.environment == environment.value)
        
        if status:
            query = query.filter(Agent.status == status.value)
            
        if framework:
            query = query.filter(Agent.framework == framework)
        
        # Get agents from database
        agents = query.all()
        
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "agentFamilyId": agent.agent_family_id,
                "framework": agent.framework,
                "repositoryUrl": agent.repository_url,
                "sourceHash": agent.source_hash,
                "templateId": agent.template_id,
                "status": agent.status,
                "environment": agent.environment,
                "modelId": agent.model_id,
                "temperature": agent.temperature,
                "maxOutputTokens": agent.max_output_tokens,
                "systemInstruction": agent.system_instruction,
                "configuration": agent.configuration,
                "createdAt": agent.created_at,
                "updatedAt": agent.updated_at,
                "createdBy": agent.created_by
            }
            for agent in agents
        ]
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing agents: {str(e)}")

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str = Path(..., description="The ID of the agent to retrieve"),
    db: Session = Depends(get_db)
) -> Dict:
    """Gets a specific agent by ID."""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "agentFamilyId": agent.agent_family_id,
            "framework": agent.framework,
            "repositoryUrl": agent.repository_url,
            "sourceHash": agent.source_hash,
            "templateId": agent.template_id,
            "status": agent.status,
            "environment": agent.environment,
            "modelId": agent.model_id,
            "temperature": agent.temperature,
            "maxOutputTokens": agent.max_output_tokens,
            "systemInstruction": agent.system_instruction,
            "configuration": agent.configuration,
            "createdAt": agent.created_at,
            "updatedAt": agent.updated_at,
            "createdBy": agent.created_by
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent: {str(e)}")

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    request: UpdateAgentRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """Updates an existing agent."""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Update fields if provided
        if request.name is not None:
            agent.name = request.name
        
        if request.description is not None:
            agent.description = request.description
            
        if request.repositoryUrl is not None:
            agent.repository_url = request.repositoryUrl
            
        if request.sourceHash is not None:
            agent.source_hash = request.sourceHash
            
        if request.status is not None:
            agent.status = request.status.value
            
        if request.modelId is not None:
            agent.model_id = request.modelId
            
        if request.temperature is not None:
            agent.temperature = request.temperature
            
        if request.maxOutputTokens is not None:
            agent.max_output_tokens = request.maxOutputTokens
            
        if request.systemInstruction is not None:
            agent.system_instruction = request.systemInstruction
            
        if request.configuration is not None:
            agent.configuration = request.configuration
        
        agent.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(agent)
        
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "agentFamilyId": agent.agent_family_id,
            "framework": agent.framework,
            "repositoryUrl": agent.repository_url,
            "sourceHash": agent.source_hash,
            "templateId": agent.template_id,
            "status": agent.status,
            "environment": agent.environment,
            "modelId": agent.model_id,
            "temperature": agent.temperature,
            "maxOutputTokens": agent.max_output_tokens,
            "systemInstruction": agent.system_instruction,
            "configuration": agent.configuration,
            "createdAt": agent.created_at,
            "updatedAt": agent.updated_at,
            "createdBy": agent.created_by
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating agent: {str(e)}")

@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Deletes an agent."""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Delete the agent
        db.delete(agent)
        db.commit()
        
        return {"message": "Agent deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting agent: {str(e)}")

@router.get("/agents/{agent_id}/lineage")
async def get_agent_lineage(
    agent_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Gets the lineage of an agent, showing related agents across the current environment.
    Note: This API would query only the current environment's instance.
    For cross-environment lineage, a separate higher-level federation would be needed.
    """
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Get all agents in the same family in the current environment
        family_agents = db.query(Agent).filter(
            Agent.agent_family_id == agent.agent_family_id
        ).all()
        
        return {
            "agentId": agent.id,
            "agentFamilyId": agent.agent_family_id,
            "relatedAgents": [
                {
                    "id": related_agent.id,
                    "name": related_agent.name,
                    "status": related_agent.status,
                    "environment": related_agent.environment,
                    "createdAt": related_agent.created_at.isoformat()
                }
                for related_agent in family_agents if related_agent.id != agent.id
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent lineage: {str(e)}")

@router.post("/agents/{agent_id}/register-external-reference")
async def register_external_reference(
    agent_id: str,
    reference_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Registers information about related agents in other environments.
    This allows for cross-environment awareness between separate AgentFleet instances.
    """
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Extract external reference data
        external_environment = reference_data.get("environment")
        external_agent_id = reference_data.get("externalAgentId")
        external_endpoint = reference_data.get("externalEndpoint")
        
        if not all([external_environment, external_agent_id, external_endpoint]):
            raise HTTPException(status_code=400, detail="Missing required reference data")
            
        # Update agent configuration with external reference
        if not agent.configuration:
            agent.configuration = {}
            
        if "externalReferences" not in agent.configuration:
            agent.configuration["externalReferences"] = []
            
        # Add or update the external reference
        external_refs = agent.configuration["externalReferences"]
        existing_ref_index = next((i for i, ref in enumerate(external_refs) 
                                 if ref.get("environment") == external_environment), None)
        
        if existing_ref_index is not None:
            external_refs[existing_ref_index].update({
                "externalAgentId": external_agent_id,
                "externalEndpoint": external_endpoint,
                "updatedAt": datetime.utcnow().isoformat()
            })
        else:
            external_refs.append({
                "environment": external_environment,
                "externalAgentId": external_agent_id,
                "externalEndpoint": external_endpoint,
                "registeredAt": datetime.utcnow().isoformat()
            })
        
        db.commit()
        
        return {
            "agentId": agent.id,
            "externalReferences": agent.configuration.get("externalReferences", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registering external reference: {str(e)}")
