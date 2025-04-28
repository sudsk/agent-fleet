"""
Agent registration command for AgentFleet CLI
"""

import json
import os
from agentfleet_cli.commands.utils import (
    detect_framework, get_git_info, make_api_request,
    print_success, print_error, print_warning, print_info, print_verbose
)

def register_agent(args):
    """Register an agent with AgentFleet"""
    
    # Required parameters check
    if not args.get("name"):
        print_error("Agent name is required")
        return 1
    
    if not args.get("project_id"):
        print_error("Google Cloud project ID is required")
        return 1
    
    # Get API URL and key
    api_url = args.get("api_url")
    api_key = args.get("api_key")
    
    if not api_url:
        print_error("API URL is required (set AGENTFLEET_API_URL environment variable or use --api-url)")
        return 1
    
    # Get git information if not provided
    if not args.get("repo_url") or not args.get("commit"):
        git_info = get_git_info()
        
        if not args.get("repo_url") and git_info.get("repo_url"):
            args["repo_url"] = git_info.get("repo_url")
            print_verbose(f"Using git repository URL: {args['repo_url']}", args.get("verbose"))
        
        if not args.get("commit") and git_info.get("commit"):
            args["commit"] = git_info.get("commit")
            print_verbose(f"Using git commit hash: {args['commit']}", args.get("verbose"))
    
    # Auto-detect framework if requested
    if args.get("detect_framework"):
        detected_framework = detect_framework()
        args["framework"] = detected_framework
        print_verbose(f"Detected framework: {detected_framework}", args.get("verbose"))
    
    # Prepare the payload for registration
    payload = {
        "name": args.get("name"),
        "description": args.get("description"),
        "framework": args.get("framework", "CUSTOM"),
        "repositoryUrl": args.get("repo_url"),
        "sourceHash": args.get("commit"),
        "environment": args.get("environment", "DEVELOPMENT"),
        "projectId": args.get("project_id"),
        "region": args.get("region", "us-central1"),
    }
    
    # Add deployment info if provided
    if any([args.get("deployment_type"), args.get("version"), 
            args.get("resource_name"), args.get("endpoint_url")]):
        deployment_info = {
            "deploymentType": args.get("deployment_type", "AGENT_ENGINE"),
            "version": args.get("version", "1.0.0"),
            "resourceName": args.get("resource_name")
        }
        
        if args.get("endpoint_url"):
            deployment_info["endpointUrl"] = args.get("endpoint_url")
        
        payload["deploymentInfo"] = deployment_info
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    # Print payload if verbose
    print_verbose(f"Registration payload: {json.dumps(payload, indent=2)}", args.get("verbose"))
    
    # Send registration request
    print_info(f"Registering agent '{args.get('name')}' with AgentFleet...")
    response = make_api_request("POST", "agents/register", data=payload, api_url=api_url, api_key=api_key)
    
    if not response:
        print_error("Failed to register agent")
        return 1
    
    print_success(f"Agent '{args.get('name')}' successfully registered with AgentFleet!")
    print_info(f"Agent ID: {response.get('id')}")
    
    if args.get("verbose") and isinstance(response, dict):
        print_info("Agent details:")
        print(json.dumps(response, indent=2))
    
    return 0
