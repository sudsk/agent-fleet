# AgentFleet.io

AgentFleet.io is a comprehensive management platform for AI agents deployed on Google Cloud's Vertex AI Agent Engine. It provides enterprise-grade monitoring, governance, and lifecycle management across development, testing, and production environments.

## Overview

AgentFleet serves as the management plane for AI agents created with the [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack), providing:

- **Multi-environment Tracking**: Monitor agents across Development, UAT, and Production (via separate instances)
- **Agent Lineage**: Track relationships between agent versions across environments
- **Deployment Management**: Streamlined deployment workflows with proper governance
- **Local Testing**: Playground functionality to test agents before deployment
- **Performance Analytics**: Comprehensive metrics on agent usage and performance
- **Template Management**: Browse and deploy from a catalog of agent templates

## Architecture

AgentFleet.io is designed to integrate with the Agent Starter Pack, providing management capabilities while letting the Agent Starter Pack handle development concerns.

![AgentFleet.io and Agent Starter Pack Integration Architecture](https://example.com/architecture.png)

## Integration with Agent Starter Pack

AgentFleet.io complements the Agent Starter Pack by providing:

1. **Registry for Agents**: Track all agents created with Agent Starter Pack
2. **Deployment Tracking**: Monitor the deployment status and history of agents
3. **Environment Promotion**: Facilitate the movement of agents from development to production
4. **Metrics Collection**: Gather and visualize performance data for agents

## Environment-Specific Instances

For production deployments, we recommend separate instances of AgentFleet for each environment:

- **AgentFleet-Dev**: For tracking development agents
- **AgentFleet-UAT**: For user acceptance testing agents
- **AgentFleet-Prod**: For production agents

This separation ensures proper security boundaries and operational isolation while maintaining agent lineage across environments.

## Features

- **Agent Registry**: Central catalog of all AI agents across environments
- **Deployment Tracking**: Monitor deployment status and history
- **Local Playground**: Test agents before deployment
- **Performance Analytics**: Track usage, response times, and other metrics
- **Cost Management**: Monitor and optimize spending
- **Governance Controls**: Approval workflows and compliance tracking
- **Template Gallery**: Browse and deploy from pre-built agent templates

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- Docker and Docker Compose (recommended for local development)
- A Google Cloud account with Vertex AI API enabled
- Service account with appropriate permissions for Vertex AI Agent Engine

### Installation

#### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/sudsk/agent-fleet.git
cd agent-fleet

# Create .env files from examples
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Add your Google Cloud service account key
cp /path/to/your/service-account-key.json ./service-account-key.json

# Start the services
docker-compose up -d
```

#### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/sudsk/agent-fleet.git
cd agent-fleet

# Set up the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# Set up the database
alembic upgrade head

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

# In a new terminal, set up the frontend
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration

# Start the frontend
npm start
```

### Configuration

#### Backend Configuration

Create a `.env` file in the backend directory with your Google Cloud configuration:

```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agentfleet
AGENTFLEET_ENVIRONMENT=DEVELOPMENT
VERTEX_REGION=us-central1
```

#### Frontend Configuration

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=DEVELOPMENT
```

### Accessing the Application

After starting the services, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Documentation**: http://localhost:5000/docs

## Development

### Database Migrations

To create a new migration after changing the database models:

```bash
cd backend
python create_migration.py
alembic upgrade head
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## CI/CD Integration

AgentFleet provides integration points for CI/CD pipelines:

### GitHub Actions

Add the following to your Agent Starter Pack project's GitHub Actions workflow:

```yaml
- name: Register with AgentFleet
  run: |
    curl -X POST $AGENTFLEET_URL/api/agents/register \
      -H "Content-Type: application/json" \
      -d '{
        "name": "${{ github.repository }}",
        "repositoryUrl": "https://github.com/${{ github.repository }}",
        "sourceHash": "${{ github.sha }}",
        "environment": "${{ env.ENVIRONMENT }}",
        "framework": "CUSTOM"
      }'
```

### CLI Integration

AgentFleet provides a CLI tool that can be added to your CI/CD pipeline:

```bash
# Install the CLI
pip install agentfleet-cli

# Register an agent
agentfleet register --name "My Agent" --repo-url "https://github.com/user/repo" --environment "DEVELOPMENT"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
