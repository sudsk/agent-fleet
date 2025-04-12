import json
import os
from typing import Dict, List, Any, Optional
import httpx
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request

class VertexAIService:
    """Service for interacting with Vertex AI API."""
    
    def __init__(self):
        # Load credentials either from service account key file or application default credentials
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path and os.path.exists(credentials_path):
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        else:
            # Use application default credentials
            self.credentials, self.project_id = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        
        # Initialize token request adapter
        self.request = Request()
    
    async def _get_auth_header(self) -> Dict[str, str]:
        """Gets authorization header with valid token."""
        # Refresh token if expired
        if not self.credentials.valid:
            self.credentials.refresh(self.request)
            
        return {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json"
        }
    
    async def list_agents(self, project_id: str, region: str) -> List[Dict[str, Any]]:
        """Lists all agents in a project using Vertex AI API."""
        try:
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/reasoningEngines",
                    headers=headers
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                data = response.json()
                return data.get("reasoningEngines", [])
                
        except Exception as e:
            print(f"Error listing agents: {str(e)}")
            raise
    
    async def get_agent(self, project_id: str, region: str, agent_id: str) -> Dict[str, Any]:
        """Gets a specific agent using Vertex AI API."""
        try:
            # Format the resource name if not already formatted
            agent_name = agent_id
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{agent_id}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://{region}-aiplatform.googleapis.com/v1/{agent_name}",
                    headers=headers
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                return response.json()
                
        except Exception as e:
            print(f"Error getting agent: {str(e)}")
            raise
    
    async def create_agent(self, project_id: str, region: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new agent using Vertex AI API."""
        try:
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/reasoningEngines",
                    headers=headers,
                    json=agent_data
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                return response.json()
                
        except Exception as e:
            print(f"Error creating agent: {str(e)}")
            raise
    
    async def update_agent(self, project_id: str, region: str, agent_id: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing agent using Vertex AI API."""
        try:
            # Format the resource name if not already formatted
            agent_name = agent_id
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{agent_id}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"https://{region}-aiplatform.googleapis.com/v1/{agent_name}",
                    headers=headers,
                    json=agent_data
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                return response.json()
                
        except Exception as e:
            print(f"Error updating agent: {str(e)}")
            raise
    
    async def delete_agent(self, project_id: str, region: str, agent_id: str) -> Dict[str, Any]:
        """Deletes an agent using Vertex AI API."""
        try:
            # Format the resource name if not already formatted
            agent_name = agent_id
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{agent_id}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"https://{region}-aiplatform.googleapis.com/v1/{agent_name}",
                    headers=headers
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response (might be empty for delete operations)
                if response.content:
                    return response.json()
                else:
                    return {"status": "success"}
                
        except Exception as e:
            print(f"Error deleting agent: {str(e)}")
            raise
    
    async def deploy_agent(self, agent_id: str, project_id: str, region: str) -> Dict[str, Any]:
        """Deploys an agent using Vertex AI API."""
        try:
            # Format the resource name if not already formatted
            agent_name = agent_id
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{agent_id}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{region}-aiplatform.googleapis.com/v1/{agent_name}:deploy",
                    headers=headers
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                if response.content:
                    return response.json()
                else:
                    return {
                        "resourceName": agent_name,
                        "status": "deploying"
                    }
                
        except Exception as e:
            print(f"Error deploying agent: {str(e)}")
            raise
    
    async def query_agent(self, project_id: str, region: str, resource_name: str, query: str) -> Dict[str, Any]:
        """Queries an agent using Vertex AI API."""
        try:
            # Format the resource name if not already formatted
            agent_name = resource_name
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{resource_name}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Prepare request body
            request_body = {
                "query": query,
                "maxResponseItems": 10
            }
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{region}-aiplatform.googleapis.com/v1/{agent_name}:query",
                    headers=headers,
                    json=request_body
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse response
                return response.json()
                
        except Exception as e:
            print(f"Error querying agent: {str(e)}")
            raise

    async def get_agent_metrics(self, project_id: str, region: str, agent_id: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """Gets metrics for an agent using Cloud Monitoring API."""
        try:
            # Format the resource name if not already formatted
            agent_name = agent_id
            if not agent_name.startswith("projects/"):
                agent_name = f"projects/{project_id}/locations/{region}/reasoningEngines/{agent_id}"
                
            # Get auth header
            headers = await self._get_auth_header()
            
            # Prepare request body for Cloud Monitoring API
            request_body = {
                "name": f"projects/{project_id}",
                "filter": f'resource.type="aiplatform.googleapis.com/Agent" AND resource.labels.agent_id="{agent_id}"',
                "interval": {
                    "startTime": start_time,
                    "endTime": end_time
                },
                "aggregation": {
                    "alignmentPeriod": "3600s",  # 1 hour
                    "perSeriesAligner": "ALIGN_SUM"
                },
                "view": "FULL"
            }
            
            # Make API request to Cloud Monitoring
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://monitoring.googleapis.com/v3/projects/{project_id}/timeSeries:query",
                    headers=headers,
                    json=request_body
                )
                
                # Raise exception for error responses
                response.raise_for_status()
                
                # Parse and process the metrics
                metrics_data = response.json()
                
                # Process the metrics into a more usable format
                # This is a simplified version - in a real implementation, 
                # you would process the specific metrics you're interested in
                processed_metrics = {
                    "agent_id": agent_id,
                    "time_range": {
                        "start": start_time,
                        "end": end_time
                    },
                    "metrics": metrics_data.get("timeSeries", [])
                }
                
                return processed_metrics
                
        except Exception as e:
            print(f"Error getting agent metrics: {str(e)}")
            raise
