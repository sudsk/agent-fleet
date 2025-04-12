from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
import os
from datetime import datetime

from app.database import get_db
from app.models.agent import EnvironmentType

router = APIRouter()

# Get current environment from environment variable or default to DEV
CURRENT_ENVIRONMENT = os.getenv("AGENTFLEET_ENVIRONMENT", EnvironmentType.DEV.value)

# Store environment configurations
ENVIRONMENT_CONFIG = {
    "name": CURRENT_ENVIRONMENT,
    "settings": {},
    "connections": {}
}

@router.get("/environment")
async def get_environment() -> Dict:
    """Gets information about the current environment."""
    try:
        return {
            "environment": CURRENT_ENVIRONMENT,
            "settings": ENVIRONMENT_CONFIG.get("settings", {}),
            "connections": ENVIRONMENT_CONFIG.get("connections", {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting environment: {str(e)}")

@router.post("/environment/settings")
async def update_environment_settings(
    settings: Dict[str, Any] = Body(...)
) -> Dict:
    """Updates environment-specific settings."""
    try:
        # Update settings
        ENVIRONMENT_CONFIG["settings"].update(settings)
        ENVIRONMENT_CONFIG["lastUpdated"] = datetime.utcnow().isoformat()
        
        return {
            "environment": CURRENT_ENVIRONMENT,
            "settings": ENVIRONMENT_CONFIG.get("settings", {}),
            "message": "Environment settings updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating environment settings: {str(e)}")

@router.post("/environment/connections")
async def register_environment_connection(
    connection: Dict[str, Any] = Body(...)
) -> Dict:
    """
    Registers a connection to another environment's AgentFleet instance.
    This allows for cross-environment coordination between separate instances.
    """
    try:
        environment_name = connection.get("environment")
        if not environment_name:
            raise HTTPException(status_code=400, detail="Environment name is required")
            
        endpoint_url = connection.get("endpointUrl")
        if not endpoint_url:
            raise HTTPException(status_code=400, detail="Endpoint URL is required")
            
        # Add or update connection
        ENVIRONMENT_CONFIG["connections"][environment_name] = {
            "endpointUrl": endpoint_url,
            "apiKey": connection.get("apiKey"),
            "registeredAt": datetime.utcnow().isoformat()
        }
        
        return {
            "environment": CURRENT_ENVIRONMENT,
            "connections": {
                env: {
                    "endpointUrl": conn["endpointUrl"],
                    "registeredAt": conn["registeredAt"]
                } for env, conn in ENVIRONMENT_CONFIG.get("connections", {}).items()
            },
            "message": f"Connection to {environment_name} environment registered successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering environment connection: {str(e)}")

@router.delete("/environment/connections/{environment_name}")
async def delete_environment_connection(
    environment_name: str
) -> Dict:
    """Removes a connection to another environment."""
    try:
        if environment_name not in ENVIRONMENT_CONFIG.get("connections", {}):
            raise HTTPException(status_code=404, detail=f"Connection to {environment_name} not found")
            
        # Remove connection
        del ENVIRONMENT_CONFIG["connections"][environment_name]
        
        return {
            "environment": CURRENT_ENVIRONMENT,
            "connections": {
                env: {
                    "endpointUrl": conn["endpointUrl"],
                    "registeredAt": conn["registeredAt"]
                } for env, conn in ENVIRONMENT_CONFIG.get("connections", {}).items()
            },
            "message": f"Connection to {environment_name} environment removed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing environment connection: {str(e)}")

@router.post("/environment/promote-agent")
async def promote_agent(
    promotion_data: Dict[str, Any] = Body(...)
) -> Dict:
    """
    Initiates the promotion of an agent from this environment to another environment.
    This involves:
    1. Creating a snapshot of the agent configuration
    2. Sending the configuration to the target environment's AgentFleet instance
    3. Tracking the promotion process
    """
    try:
        agent_id = promotion_data.get("agentId")
        if not agent_id:
            raise HTTPException(status_code=400, detail="Agent ID is required")
            
        target_environment = promotion_data.get("targetEnvironment")
        if not target_environment:
            raise HTTPException(status_code=400, detail="Target environment is required")
            
        # Check if we have a connection to the target environment
        if target_environment not in ENVIRONMENT_CONFIG.get("connections", {}):
            raise HTTPException(
                status_code=400, 
                detail=f"No connection registered for {target_environment} environment"
            )
        
        # Get agent from database
        db = next(get_db())
        agent = db.query(db.Agent).filter(db.Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
            
        # In a real implementation, this would:
        # 1. Package the agent configuration 
        # 2. Send a request to the target environment's API
        # 3. Track the promotion status
        
        # For now, we'll provide a mock implementation
        promotion_id = str(uuid.uuid4())
        
        return {
            "promotionId": promotion_id,
            "agentId": agent_id,
            "sourceEnvironment": CURRENT_ENVIRONMENT,
            "targetEnvironment": target_environment,
            "status": "INITIATED",
            "message": f"Agent promotion to {target_environment} initiated successfully",
            "nextSteps": [
                "The target environment will create a new agent based on this configuration",
                "The agent ID will be preserved across environments for lineage tracking",
                "You can check the status of this promotion using the promotion ID"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error promoting agent: {str(e)}")

@router.get("/environment/promotions/{promotion_id}")
async def get_promotion_status(
    promotion_id: str
) -> Dict:
    """
    Gets the status of an agent promotion process.
    This is a mock implementation for demonstration purposes.
    """
    try:
        # In a real implementation, this would query a promotion tracking system
        return {
            "promotionId": promotion_id,
            "status": "COMPLETED",
            "message": "Agent promotion completed successfully",
            "sourceEnvironment": CURRENT_ENVIRONMENT,
            "targetEnvironment": "UAT",
            "sourceAgentId": "sample-agent-id",
            "targetAgentId": "sample-agent-id",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting promotion status: {str(e)}")
