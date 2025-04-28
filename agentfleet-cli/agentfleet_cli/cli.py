#!/usr/bin/env python3
"""
AgentFleet CLI - Command Line Interface for AgentFleet.io
"""

import sys
import click
import os
from agentfleet_cli.commands.register import register_agent
from agentfleet_cli.commands.deployment import create_deployment, list_deployments

# Define version
__version__ = "0.1.0"

@click.group()
@click.version_option(version=__version__)
def cli():
    """AgentFleet CLI - Manage your AI agents with AgentFleet.io"""
    pass

@cli.command()
@click.option("--name", required=True, help="Name of the agent")
@click.option("--description", default=None, help="Description of the agent")
@click.option("--framework", 
              type=click.Choice(["CUSTOM", "LANGCHAIN", "LLAMAINDEX", "LANGGRAPH", "CREWAI"], case_sensitive=False), 
              default="CUSTOM", 
              help="Agent framework")
@click.option("--repo-url", default=None, help="Repository URL (defaults to git remote origin)")
@click.option("--commit", default=None, help="Commit hash (defaults to current HEAD)")
@click.option("--environment", 
              type=click.Choice(["DEVELOPMENT", "UAT", "PRODUCTION"], case_sensitive=False), 
              default="DEVELOPMENT", 
              help="Deployment environment")
@click.option("--project-id", required=True, help="Google Cloud project ID")
@click.option("--region", default="us-central1", help="Google Cloud region")
@click.option("--deployment-type", default=None, help="Deployment type (e.g., AGENT_ENGINE, CLOUD_RUN)")
@click.option("--version", default=None, help="Agent version")
@click.option("--resource-name", default=None, help="Vertex AI resource name or Cloud Run service name")
@click.option("--endpoint-url", default=None, help="Endpoint URL")
@click.option("--api-url", default=None, help="AgentFleet API URL (defaults to AGENTFLEET_API_URL env var)")
@click.option("--api-key", default=None, help="AgentFleet API key (defaults to AGENTFLEET_API_KEY env var)")
@click.option("--detect-framework", is_flag=True, help="Automatically detect framework from current directory")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def register(name, description, framework, repo_url, commit, environment, project_id, region, 
             deployment_type, version, resource_name, endpoint_url, api_url, api_key, detect_framework, verbose):
    """Register an agent with AgentFleet"""
    exit_code = register_agent({
        "name": name,
        "description": description,
        "framework": framework,
        "repo_url": repo_url,
        "commit": commit,
        "environment": environment,
        "project_id": project_id,
        "region": region,
        "deployment_type": deployment_type,
        "version": version,
        "resource_name": resource_name,
        "endpoint_url": endpoint_url,
        "api_url": api_url or os.environ.get("AGENTFLEET_API_URL"),
        "api_key": api_key or os.environ.get("AGENTFLEET_API_KEY"),
        "detect_framework": detect_framework,
        "verbose": verbose
    })
    sys.exit(exit_code)

@cli.group()
def deployment():
    """Manage agent deployments"""
    pass

@deployment.command("create")
@click.option("--agent-id", required=True, help="ID of the agent to deploy")
@click.option("--deployment-type", default="AGENT_ENGINE", help="Deployment type")
@click.option("--version", default="1.0.0", help="Deployment version")
@click.option("--project-id", required=True, help="Google Cloud project ID")
@click.option("--region", default="us-central1", help="Google Cloud region")
@click.option("--resource-name", required=True, help="Vertex AI resource name or Cloud Run service name")
@click.option("--status", default="SUCCESSFUL", help="Deployment status")
@click.option("--endpoint-url", required=True, help="Endpoint URL")
@click.option("--api-url", default=None, help="AgentFleet API URL (defaults to AGENTFLEET_API_URL env var)")
@click.option("--api-key", default=None, help="AgentFleet API key (defaults to AGENTFLEET_API_KEY env var)")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def create_deployment_command(agent_id, deployment_type, version, project_id, region, resource_name, 
                             status, endpoint_url, api_url, api_key, verbose):
    """Create a new deployment for an agent"""
    exit_code = create_deployment({
        "agent_id": agent_id,
        "deployment_type": deployment_type,
        "version": version,
        "project_id": project_id,
        "region": region,
        "resource_name": resource_name,
        "status": status,
        "endpoint_url": endpoint_url,
        "api_url": api_url or os.environ.get("AGENTFLEET_API_URL"),
        "api_key": api_key or os.environ.get("AGENTFLEET_API_KEY"),
        "verbose": verbose
    })
    sys.exit(exit_code)

@deployment.command("list")
@click.option("--agent-id", default=None, help="Filter by agent ID")
@click.option("--status", default=None, help="Filter by deployment status")
@click.option("--environment", default=None, help="Filter by environment")
@click.option("--api-url", default=None, help="AgentFleet API URL (defaults to AGENTFLEET_API_URL env var)")
@click.option("--api-key", default=None, help="AgentFleet API key (defaults to AGENTFLEET_API_KEY env var)")
def list_deployments_command(agent_id, status, environment, api_url, api_key):
    """List deployments"""
    exit_code = list_deployments({
        "agent_id": agent_id,
        "status": status,
        "environment": environment,
        "api_url": api_url or os.environ.get("AGENTFLEET_API_URL"),
        "api_key": api_key or os.environ.get("AGENTFLEET_API_KEY")
    })
    sys.exit(exit_code)

def main():
    """Main entry point for the CLI"""
    cli()

if __name__ == "__main__":
    main()
