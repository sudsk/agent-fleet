"""
Deployment management commands for AgentFleet CLI
"""

import json
from agentfleet_cli.commands.utils import (
    make_api_request, format_table,
    print_success, print_error, print_warning, print_info, print_verbose
)

def create_deployment(args):
    """Create a new deployment for an agent"""
    
    # Required parameters check
    if not args.get("agent_id"):
        print_error("Agent ID is required")
        return 1
    
    if not args.get("project_id"):
        print_error("Google Cloud project ID is required")
        return 1
    
    if not args.get("resource_name"):
        print_error("Resource name is required")
        return 1
    
    if not args.get("endpoint_url"):
        print_error("Endpoint URL is required")
        return 1
    
    # Get API URL and key
    api_url = args.get("api_url")
    api_key = args.get("api_key")
    
    if not api_url:
        print_error("API URL is required (set AGENTFLEET_API_URL environment variable or use --api-url)")
        return 1
    
    # Prepare the payload for deployment creation
    payload = {
        "agentId": args.get("agent_id"),
        "deploymentType": args.get("deployment_type", "AGENT_ENGINE"),
        "version": args.get("version", "1.0.0"),
        "projectId": args.get("project_id"),
        "region": args.get("region", "us-central1"),
        "resourceName": args.get("resource_name"),
        "status": args.get("status", "SUCCESSFUL"),
        "endpointUrl": args.get("endpoint_url"),
        "deployedBy": args.get("deployed_by")
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    # Print payload if verbose
    print_verbose(f"Deployment payload: {json.dumps(payload, indent=2)}", args.get("verbose"))
    
    # Send deployment request
    print_info(f"Creating deployment for agent {args.get('agent_id')}...")
    response = make_api_request("POST", "deployments", data=payload, api_url=api_url, api_key=api_key)
    
    if not response:
        print_error("Failed to create deployment")
        return 1
    
    print_success(f"Deployment successfully created!")
    print_info(f"Deployment ID: {response.get('id')}")
    
    if args.get("verbose") and isinstance(response, dict):
        print_info("Deployment details:")
        print(json.dumps(response, indent=2))
    
    return 0

def list_deployments(args):
    """List deployments"""
    
    # Get API URL and key
    api_url = args.get("api_url")
    api_key = args.get("api_key")
    
    if not api_url:
        print_error("API URL is required (set AGENTFLEET_API_URL environment variable or use --api-url)")
        return 1
    
    # Prepare query parameters
    params = {}
    if args.get("agent_id"):
        params["agent_id"] = args.get("agent_id")
    if args.get("status"):
        params["status"] = args.get("status")
    if args.get("environment"):
        params["environment"] = args.get("environment")
    
    # Send request to list deployments
    print_info("Fetching deployments...")
    response = make_api_request("GET", "deployments", params=params, api_url=api_url, api_key=api_key)
    
    if not response:
        print_error("Failed to list deployments")
        return 1
    
    if not response or (isinstance(response, list) and len(response) == 0):
        print_info("No deployments found")
        return 0
    
    # Format as a table
    headers = ["ID", "Agent ID", "Type", "Status", "Environment", "Deployed At"]
    data = []
    
    for deployment in response:
        data.append({
            "ID": deployment.get("id", ""),
            "Agent ID": deployment.get("agentId", ""),
            "Type": deployment.get("deploymentType", ""),
            "Status": deployment.get("status", ""),
            "Environment": deployment.get("environment", ""),
            "Deployed At": deployment.get("deployedAt", "")
        })
    
    print(format_table(data, headers))
    print_info(f"Total deployments: {len(response)}")
    
    return 0
