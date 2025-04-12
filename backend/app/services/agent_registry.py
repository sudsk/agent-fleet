
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import json
import os
from sqlalchemy.orm import Session
from app.database import Agent, Deployment, AgentStatus

class AgentRegistryService:
    """Service for managing the agent registry."""
    
    def __init__(self):
        # Get current environment
        self.environment = os.getenv("AGENTFLEET_ENVIRONMENT", "DEVELOPMENT")
    
    async def register_agent(self, db: Session, agent_data: Dict[str, Any]) -> Agent:
        """
        Registers a new agent in the registry.
        Returns the created agent.
        """
        try:
            # Generate agent family ID if not provided
            agent_family_id = agent_data.get("agentFamilyId") or str(uuid.uuid4())
            
            # Create agent in database
            agent = Agent(
                id=str(uuid.uuid4()),
                name=agent_data.get("name"),
                description=agent_data.get("description"),
                agent_family_id=agent_family_id,
                framework=agent_data.get("framework"),
                repository_url=agent_data.get("repositoryUrl"),
                source_hash=agent_data.get("sourceHash"),
                template_id=agent_data.get("templateId"),
                status=agent_data.get("status", AgentStatus.DRAFT.value),
                environment=self.environment,
                model_id=agent_data.get("modelId"),
                temperature=agent_data.get("temperature"),
                max_output_tokens=agent_data.get("maxOutputTokens"),
                system_instruction=agent_data.get("systemInstruction"),
                configuration=agent_data.get("configuration"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                created_by=agent_data.get("createdBy")
            )

            db.add(agent)
            db.commit()
            db.refresh(agent)
            
            return agent
            
        except Exception as e:
            db.rollback()
            print(f"Error registering agent: {str(e)}")
            raise
    
    async def update_agent(self, db: Session, agent_id: str, agent_data: Dict[str, Any]) -> Agent:
        """
        Updates an existing agent in the registry.
        Returns the updated agent.
        """
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError(f"Agent not found with ID: {agent_id}")
            
            # Update fields if provided
            for key, value in agent_data.items():
                if key == "name" and value is not None:
                    agent.name = value
                elif key == "description" and value is not None:
                    agent.description = value
                elif key == "repositoryUrl" and value is not None:
                    agent.repository_url = value
                elif key == "sourceHash" and value is not None:
                    agent.source_hash = value
                elif key == "status" and value is not None:
                    agent.status = value
                elif key == "modelId" and value is not None:
                    agent.model_id = value
                elif key == "temperature" and value is not None:
                    agent.temperature = value
                elif key == "maxOutputTokens" and value is not None:
                    agent.max_output_tokens = value
                elif key == "systemInstruction" and value is not None:
                    agent.system_instruction = value
                elif key == "configuration" and value is not None:
                    agent.configuration = value
            
            agent.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(agent)
            
            return agent
            
        except Exception as e:
            db.rollback()
            print(f"Error updating agent: {str(e)}")
            raise
    
    async def register_deployment(self, db: Session, deployment_data: Dict[str, Any]) -> Deployment:
        """
        Registers a new deployment for an agent.
        Returns the created deployment.
        """
        try:
            agent_id = deployment_data.get("agentId")
            if not agent_id:
                raise ValueError("Agent ID is required for deployment registration")
            
            # Check if agent exists
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError(f"Agent not found with ID: {agent_id}")
            
            # Create deployment
            deployment = Deployment(
                id=str(uuid.uuid4()),
                agent_id=agent_id,
                deployment_type=deployment_data.get("deploymentType", "AGENT_ENGINE"),
                version=deployment_data.get("version", "1.0.0"),
                environment=agent.environment,
                project_id=deployment_data.get("projectId"),
                region=deployment_data.get("region", "us-central1"),
                resource_name=deployment_data.get("resourceName"),
                status=deployment_data.get("status", "SUCCESSFUL"),
                endpoint_url=deployment_data.get("endpointUrl"),
                deployed_at=datetime.utcnow(),
                deployed_by=deployment_data.get("deployedBy"),
                configuration=deployment_data.get("configuration")
            )
            
            db.add(deployment)
            
            # Update agent status if deployment was successful
            if deployment.status == "SUCCESSFUL":
                agent.status = "DEPLOYED"
                agent.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(deployment)
            
            return deployment
            
        except Exception as e:
            db.rollback()
            print(f"Error registering deployment: {str(e)}")
            raise
    
    async def track_agent_lineage(self, db: Session, agent_id: str, related_agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Tracks the lineage of an agent across environments.
        This allows for identifying related agents in different environments.
        """
        try:
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError(f"Agent not found with ID: {agent_id}")
            
            # Initialize configuration if needed
            if not agent.configuration:
                agent.configuration = {}
            
            # Update lineage information
            if "lineage" not in agent.configuration:
                agent.configuration["lineage"] = {}
            
            # Add related agents to lineage
            for related_agent in related_agents:
                env = related_agent.get("environment")
                if env and env != agent.environment:
                    agent.configuration["lineage"][env] = {
                        "agentId": related_agent.get("agentId"),
                        "lastUpdated": datetime.utcnow().isoformat()
                    }
            
            agent.updated_at = datetime.utcnow()
            db.commit()
            
            return {
                "agentId": agent.id,
                "agentFamilyId": agent.agent_family_id,
                "lineage": agent.configuration.get("lineage", {})
            }
            
        except Exception as e:
            db.rollback()
            print(f"Error tracking agent lineage: {str(e)}")
            raise
    
    async def get_agent_family(self, db: Session, agent_family_id: str) -> List[Agent]:
        """
        Gets all agents in a specific family.
        This allows for viewing all versions of an agent.
        """
        try:
            agents = db.query(Agent).filter(Agent.agent_family_id == agent_family_id).all()
            return agents
            
        except Exception as e:
            print(f"Error getting agent family: {str(e)}")
            raise
