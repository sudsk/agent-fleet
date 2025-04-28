# AgentFleet CLI Integration Guide

This guide explains how to integrate the AgentFleet CLI with the Agent Starter Pack to automatically register and manage your AI agents within the AgentFleet platform.

## Overview

The AgentFleet CLI provides a simple way to register agents and their deployments with the AgentFleet management platform. By integrating this CLI with the Agent Starter Pack's CI/CD pipelines, you can automatically:

1. Register new agents when they're created
2. Track deployments across environments
3. Maintain consistent agent lineage from development to production

## Installation

There are several ways to install the AgentFleet CLI:

### Via pip (recommended)

```bash
pip install agentfleet-cli
```

### From source

```bash
git clone https://github.com/sudsk/agent-fleet.git
cd agent-fleet/agentfleet-cli
pip install -e .
```

### In CI/CD pipelines

For Cloud Build or GitHub Actions, you can install the CLI directly in your pipeline:

```bash
pip install git+https://github.com/sudsk/agent-fleet.git#subdirectory=agentfleet-cli
```

## Basic Usage

### Configuration

Set up your environment variables for easier CLI usage:

```bash
export AGENTFLEET_API_URL=https://your-agentfleet-instance.com/api
export AGENTFLEET_API_KEY=your_api_key
```

### Register an Agent

```bash
# Basic usage
agentfleet register --name "My Agent" --project-id "my-gcp-project"

# With deployment information
agentfleet register \
  --name "My Agent" \
  --project-id "my-gcp-project" \
  --region "us-central1" \
  --deployment-type "AGENT_ENGINE" \
  --resource-name "my-agent" \
  --endpoint-url "https://my-agent-url.com"
```

### Register a Deployment

```bash
agentfleet deployment create \
  --agent-id "agent-123" \
  --project-id "my-gcp-project" \
  --region "us-central1" \
  --resource-name "my-agent" \
  --endpoint-url "https://my-agent-url.com"
```

## Integrating with Agent Starter Pack

### Cloud Build Integration

1. Create a secret in Secret Manager for your AgentFleet API key:

```bash
echo -n "your-api-key" | gcloud secrets create agentfleet-api-key \
  --replication-policy="automatic" \
  --data-file=-
```

2. Create or update your Cloud Build trigger to use the AgentFleet integration:

```bash
gcloud beta builds triggers create cloud-source-repositories \
  --repo=my-agent-repo \
  --branch-pattern=main \
  --build-config=infrastructure/ci-cd/agent-starter-pack-integration/agentfleet-integration.yaml \
  --substitutions=_AGENTFLEET_API_URL=https://your-agentfleet-instance.com/api
```

3. Update your main Cloud Build configuration to include the AgentFleet steps.

### GitHub Actions Integration

1. Add the required secrets to your GitHub repository:
   - `AGENTFLEET_API_URL`
   - `AGENTFLEET_API_KEY`
   - `GCP_PROJECT_ID`
   - `GCP_REGION`
   - `GCP_SA_KEY` (your service account key with necessary permissions)

2. Add the GitHub Actions workflow file to your repository:
   - Create `.github/workflows/agentfleet-integration.yml`
   - Copy the example from `infrastructure/ci-cd/github-actions/agentfleet-integration.yml`

## Terraform Deployment

You can use the provided Terraform module to set up all the infrastructure required for AgentFleet integration:

```hcl
module "agentfleet_integration" {
  source = "github.com/sudsk/agent-fleet//infrastructure/terraform/modules/agentfleet-integration"

  project_id          = "my-project-id"
  region              = "us-central1"
  agentfleet_api_key  = "your-api-key"
  agentfleet_api_url  = "https://your-agentfleet-instance.com/api"
  cloudbuild_sa_email = "cloudbuild@my-project-id.iam.gserviceaccount.com"
  repository_name     = "github_myorg_my-agent-repo"
  staging_project_id  = "my-staging-project-id"
  prod_project_id     = "my-prod-project-id"
  use_github_actions  = true
}
```

## Common Workflows

### Development to Production Promotion

The AgentFleet CLI automatically maintains the lineage of agents across environments. When an agent is registered in multiple environments with the same name and repository, AgentFleet tracks them as related agents.

Example workflow:
1. Register in Development with `--environment DEVELOPMENT`
2. After testing, register in UAT with `--environment UAT`
3. Finally, register in Production with `--environment PRODUCTION`

AgentFleet will maintain the relationship between these environments, allowing you to track an agent's journey from development to production.

## Troubleshooting

### API Connection Issues

If you're having trouble connecting to the AgentFleet API, check:
- Your API URL is correct
- Your API key is valid
- Network connectivity to the AgentFleet instance

Run with the `--verbose` flag for additional debugging information:

```bash
agentfleet register --name "My Agent" --project-id "my-project" --verbose
```

### CI/CD Integration Issues

If the CLI isn't working in your CI/CD pipeline:
- Ensure the CLI is installed correctly
- Check that secrets are properly configured
- Verify service account permissions
- Examine build logs for detailed error messages

## Support

For additional support or questions about the AgentFleet CLI:
- GitHub Issues: [https://github.com/sudsk/agent-fleet/issues](https://github.com/sudsk/agent-fleet/issues)
- Email: support@agentfleet.io
