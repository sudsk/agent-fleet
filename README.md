# AgentFleet.io

AgentFleet.io is a comprehensive management platform for AI agents deployed on Google Cloud's Vertex AI Agent Engine. It provides enterprise-grade monitoring, governance, and lifecycle management across development, testing, and production environments.

![AgentFleet.io Architecture](https://example.com/architecture.png)

## Overview

AgentFleet serves as the management plane for AI agents created with the [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack), providing:

- **Multi-environment Tracking**: Monitor agents across Development, UAT, and Production
- **Agent Lineage**: Track relationships between agent versions across environments
- **Deployment Management**: Streamlined deployment workflows with proper governance
- **Local Testing**: Playground functionality to test agents before deployment
- **Performance Analytics**: Comprehensive metrics on agent usage and performance
- **Template Management**: Browse and deploy from a catalog of agent templates

## Architecture

AgentFleet.io is designed to integrate with the Agent Starter Pack, providing management capabilities while letting the Agent Starter Pack handle development concerns:

```
┌─────────────────────────────────────┐      ┌─────────────────────────────┐
│             Frontend                │      │          Backend            │
│  ┌─────────────┐    ┌─────────────┐ │      │  ┌─────────────────────┐   │
│  │  React UI   │◄───┤   API       │ │      │  │  FastAPI            │   │
│  │  Components │    │   Services  │◄┼──────┼──┤  REST API Server    │   │
│  └─────────────┘    └─────────────┘ │      │  └─────────────────────┘   │
│                                     │      │             │               │
│  ┌─────────────┐    ┌─────────────┐ │      │  ┌─────────────────────┐   │
│  │  Dashboard  │    │   State     │ │      │  │  Agent Registry     │   │
│  │  System     │    │   Management│ │      │  │  Service            │   │
│  └─────────────┘    └─────────────┘ │      │  └─────────────────────┘   │
└─────────────────────────────────────┘      │             │               │
                                             │  ┌─────────────────────┐   │
                                             │  │  Vertex AI Agent    │   │
                                             │  │  Engine API Client  │   │
                                             │  └─────────────────────┘   │
                                             └─────────────────────────────┘
                                                          │
                                             ┌─────────────────────────────┐
                                             │    Google Cloud Platform    │
                                             │  ┌─────────────────────┐   │
                                             │  │  Vertex AI          │   │
                                             │  │  Agent Engine       │   │
                                             │  └─────────────────────┘   │
                                             └─────────────────────────────┘
```

## Integration with Agent Starter Pack

AgentFleet.io is designed to complement the Agent Starter Pack by providing:

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
- A Google Cloud account with Vertex AI API enabled
- Service account with appropriate permissions for Vertex AI Agent Engine

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agent-fleet.git
cd agent-fleet

# Set up the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up the frontend
cd ../frontend
npm install
```

### Configuration

Create a `.env` file in the backend directory with your Google Cloud configuration:

```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
VERTEX_REGION=us-central1
```

### Running Locally

```bash
# Start the backend server
cd backend
python -m app.main

# Start the frontend
cd ../frontend
npm start
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
