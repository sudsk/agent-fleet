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
