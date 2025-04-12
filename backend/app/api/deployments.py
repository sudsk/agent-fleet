from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from datetime import datetime
import uuid

from app.database import get_db, Agent, Deployment, DeploymentStatus
from app.models.agent import DeploymentResponse
from app.services.vertex_ai import VertexAIService

router = APIRouter()
vertex_service = VertexAIService()

@router.post("/deployments", response_model=DeploymentResponse)
async def create_deployment(
    deployment_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Records a new deployment for an agent.
    This can be called from CI/CD pipelines when an agent is deployed.
    """
    try:
        agent_id = deployment_data.get("agentId")
        if not agent_id:
            raise HTTPException(status_code=400, detail="Agent ID is required")
            
        # Check if agent exists
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        # Create new deployment record
        deployment = Deployment(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            deployment_type=deployment_data.get("deploymentType", "AGENT_ENGINE"),
            version=deployment_data.get("version", "1.0.0"),
            environment=agent.environment,  # Use agent's environment
            project_id=deployment_data.get("projectId"),
            region=deployment_data.get("region", "us-central1"),
            resource_name=deployment_data.get("resourceName"),
            status=deployment_data.get("status", DeploymentStatus.SUCCESSFUL.value),
            endpoint_url=deployment_data.get("endpointUrl"),
            deployed_at=datetime.utcnow(),
            deployed_by=deployment_data.get("deployedBy"),
            configuration=deployment_data.get("configuration")
        )
        
        db.add(deployment)
        
        # Update agent status if deployment was successful
        if deployment.status == DeploymentStatus.SUCCESSFUL.value:
            agent.status = "DEPLOYED"
            agent.updated_at = datetime.utcnow()
            
        db.commit()
        db.refresh(deployment)
        
        return {
            "id": deployment.id,
            "agentId": deployment.agent_id,
            "deploymentType": deployment.deployment_type,
            "version": deployment.version,
            "environment": deployment.environment,
            "projectId": deployment.project_id,
            "region": deployment.region,
            "resourceName": deployment.resource_name,
            "status": deployment.status,
            "endpointUrl": deployment.endpoint_url,
            "deployedAt": deployment.deployed_at,
            "deployedBy": deployment.deployed_by,
            "configuration": deployment.configuration
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating deployment: {str(e)}")

@router.get("/deployments", response_model=List[DeploymentResponse])
async def list_deployments(
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    environment: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[Dict]:
    """Lists deployments with optional filtering."""
    try:
        # Base query
        query = db.query(Deployment)
        
        # Apply filters
        if agent_id:
            query = query.filter(Deployment.agent_id == agent_id)
            
        if status:
            query = query.filter(Deployment.status == status)
            
        if environment:
            query = query.filter(Deployment.environment == environment)
            
        # Get deployments
        deployments = query.order_by(Deployment.deployed_at.desc()).all()
        
        return [
            {
                "id": deployment.id,
                "agentId": deployment.agent_id,
                "deploymentType": deployment.deployment_type,
                "version": deployment.version,
                "environment": deployment.environment,
                "projectId": deployment.project_id,
                "region": deployment.region,
                "resourceName": deployment.resource_name,
                "status": deployment.status,
                "endpointUrl": deployment.endpoint_url,
                "deployedAt": deployment.deployed_at,
                "deployedBy": deployment.deployed_by,
                "configuration": deployment.configuration
            }
            for deployment in deployments
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing deployments: {str(e)}")

@router.get("/deployments/{deployment_id}", response_model=DeploymentResponse)
async def get_deployment(
    deployment_id: str,
    db: Session = Depends(get_db)
) -> Dict:
    """Gets a specific deployment by ID."""
    try:
        deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
        
        if not deployment:
            raise HTTPException(status_code=404, detail="Deployment not found")
            
        return {
            "id": deployment.id,
            "agentId": deployment.agent_id,
            "deploymentType": deployment.deployment_type,
            "version": deployment.version,
            "environment": deployment.environment,
            "projectId": deployment.project_id,
            "region": deployment.region,
            "resourceName": deployment.resource_name,
            "status": deployment.status,
            "endpointUrl": deployment.endpoint_url,
            "deployedAt": deployment.deployed_at,
            "deployedBy": deployment.deployed_by,
            "configuration": deployment.configuration
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting deployment: {str(e)}")

@router.put("/deployments/{deployment_id}/status")
async def update_deployment_status(
    deployment_id: str,
    status_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """Updates the status of a deployment."""
    try:
        deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
        
        if not deployment:
            raise HTTPException(status_code=404, detail="Deployment not found")
            
        # Update status
        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(status_code=400, detail="Status is required")
            
        deployment.status = new_status
        
        # If the deployment failed, update the agent status accordingly
        if new_status == DeploymentStatus.FAILED.value:
            agent = db.query(Agent).filter(Agent.id == deployment.agent_id).first()
            if agent:
                # Only revert to TESTED if it was previously set to DEPLOYED
                if agent.status == "DEPLOYED":
                    agent.status = "TESTED"
                    agent.updated_at = datetime.utcnow()
                    
        db.commit()
        
        return {
            "id": deployment.id,
            "status": deployment.status,
            "message": "Deployment status updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating deployment status: {str(e)}")

@router.post("/agents/{agent_id}/deploy")
async def deploy_agent(
    agent_id: str,
    deploy_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Triggers deployment of an agent using the Vertex AI Agent Engine.
    Note: In a real implementation, this would likely queue a deployment task.
    """
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        # Extract deployment parameters
        project_id = deploy_data.get("projectId")
        region = deploy_data.get("region", "us-central1")
        
        if not project_id:
            raise HTTPException(status_code=400, detail="Project ID is required")
            
        # Create deployment record with PENDING status
        deployment_id = str(uuid.uuid4())
        deployment = Deployment(
            id=deployment_id,
            agent_id=agent_id,
            deployment_type="AGENT_ENGINE",
            version=deploy_data.get("version", "1.0.0"),
            environment=agent.environment,
            project_id=project_id,
            region=region,
            status=DeploymentStatus.PENDING.value,
            deployed_at=datetime.utcnow(),
            deployed_by=deploy_data.get("deployedBy"),
            configuration=deploy_data
        )
        
        db.add(deployment)
        db.commit()
        
        # Note: In a real implementation, this would trigger an async deployment process
        # For now, we'll simulate the deployment process
        
        try:
            # Call Vertex AI service to deploy the agent
            # This is a placeholder - would need to be implemented with actual Vertex AI API
            response = await vertex_service.deploy_agent(agent_id, project_id, region)
            
            # Update deployment with success status
            deployment.status = DeploymentStatus.SUCCESSFUL.value
            deployment.resource_name = response.get("resourceName")
            deployment.endpoint_url = response.get("endpointUrl")
            
            # Update agent status
            agent.status = "DEPLOYED"
            agent.updated_at = datetime.utcnow()
            
            db.commit()
            
            return {
                "deploymentId": deployment.id,
                "agentId": agent.id,
                "status": deployment.status,
                "resourceName": deployment.resource_name,
                "endpointUrl": deployment.endpoint_url,
                "message": "Agent deployed successfully"
            }
            
        except Exception as deploy_error:
            # Update deployment with failed status
            deployment.status = DeploymentStatus.FAILED.value
            deployment.configuration = {
                **(deployment.configuration or {}),
                "error": str(deploy_error)
            }
            db.commit()
            
            raise HTTPException(status_code=500, detail=f"Deployment failed: {str(deploy_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deploying agent: {str(e)}")
