# AgentFleet CLI

A command-line interface for integrating with AgentFleet.io, enabling seamless registration and management of AI agents within the AgentFleet platform.

## Installation

```bash
pip install agentfleet-cli
```

## Usage

### Environment Configuration

You can configure the CLI using environment variables:

```bash
export AGENTFLEET_API_URL=https://your-agentfleet-instance.com/api
export AGENTFLEET_API_KEY=your_api_key_here
```

Or use command-line arguments for each command.

### Register an Agent

```bash
# Basic registration with minimum required parameters
agentfleet register --name "My Agent" --project-id "my-gcp-project" --region "us-central1"

# Full registration with all options
agentfleet register \
  --name "My Agent" \
  --description "This is my awesome agent" \
  --framework LANGCHAIN \
  --repo-url "https://github.com/user/repo" \
  --commit "abc123" \
  --environment DEVELOPMENT \
  --project-id "my-gcp-project" \
  --region "us-central1" \
  --deployment-type AGENT_ENGINE \
  --version "1.0.0" \
  --resource-name "my-agent-resource" \
  --endpoint-url "https://my-agent-url.com" \
  --api-url "https://agentfleet.example.com/api" \
  --api-key "your_api_key_here"

# Auto-detect framework from current directory
agentfleet register --name "My Agent" --project-id "my-gcp-project" --detect-framework
```

### Register a Deployment

```bash
agentfleet deployment create \
  --agent-id "agent-123" \
  --deployment-type AGENT_ENGINE \
  --version "1.0.0" \
  --project-id "my-gcp-project" \
  --region "us-central1" \
  --resource-name "my-agent-resource" \
  --endpoint-url "https://my-agent-url.com"
```

### List Agents

```bash
agentfleet agents list
```

### List Deployments

```bash
agentfleet deployments list --agent-id "agent-123"
```

## CI/CD Integration

This CLI is designed to be easily integrated with CI/CD pipelines. Example for Cloud Build:

```yaml
steps:
  # Build and deploy steps...
  
  # Register with AgentFleet
  - name: "python:3.11-slim"
    id: register-with-agentfleet
    entrypoint: /bin/bash
    args:
      - "-c"
      - |
        pip install agentfleet-cli
        
        agentfleet register \
          --name "my-agent" \
          --project-id ${_PROJECT_ID} \
          --region ${_REGION} \
          --environment DEVELOPMENT \
          --endpoint-url ${_ENDPOINT_URL} \
          --api-url ${_AGENTFLEET_API_URL} \
          --api-key ${_AGENTFLEET_API_KEY}
```

## License

MIT License
