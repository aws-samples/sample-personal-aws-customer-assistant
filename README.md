# Personal AWS customer assistant

An AI-powered customer support agent that serves as an alternative to traditional account managers, built with Strands Agent and deployed on AgentCore Runtime.

## Features

- **Knowledge Integration**: Searches repository documentation from GitHub
- **Serverless Deployment**: Runs on AgentCore Runtime with auto-scaling
- **One-Click Deployment**: Deploy via CloudFormation with custom knowledge sources

## Quick Start

### One-Click Deployment

Deploy the Personal AWS customer assistant with a single click using AWS CloudFormation:

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=PersonalSupportAgentStack&templateURL=https://aws-ml-jp.s3.ap-northeast-1.amazonaws.com/asset-deployments/agents/PersonalSupportAgentDeploymentStack.yaml)

#### Parameters

* **NotificationEmailAddress** (Required)
  * Email address for deployment notifications
  * You will receive deployment start and completion notifications

* **RepositoryUrl** (Default: `https://github.com/aws-samples/sample-personal-aws-customer-assistant`)
  * Git repository URL containing knowledge documents
  * Customize to use your own knowledge base

* **KnowledgeDirectory** (Default: `docs`)
  * Directory path within repository containing documents
  * Agent will search files in this directory

* **DeploymentRegion** (Default: `us-west-2`)
  * AWS region for agent deployment and Bedrock API
  * Options: us-east-1, us-west-2, ap-northeast-1, eu-west-1

#### Deployment Process

1. Click the Launch Stack button above
2. Configure parameters (or use defaults)
3. Acknowledge IAM resource creation
4. Click "Create stack"
5. Wait for email notification (~10-15 minutes)
6. Use the Runtime ARN from the email to invoke your agent

### Manual Deployment with CDK

For advanced users who want more control over the deployment:

#### Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.11+ with `uv` package manager
- Docker (for container builds)
- Node.js 20+ (for CDK)

#### Deploy with CDK

1. **Bootstrap CDK** (first time only):
   ```bash
   cd cdk
   cdk bootstrap aws://ACCOUNT-ID/REGION
   ```

2. **Deploy Stack**:
   ```bash
   cdk deploy
   ```

3. **Get Runtime ARN**:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name SupportAgentStack \
     --query 'Stacks[0].Outputs[?OutputKey==`AgentRuntimeArn`].OutputValue' \
     --output text
   ```

### Local Development

1. **Setup Environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   cd agent
   uv pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   uv run pytest tests/
   uv run ruff check
   ```

## Architecture

- **SupportAgent**: Strands Agent with search/retrieve logic for all knowledge sources
- **WikiKnowledgeSource**: File I/O operations for GitHub repository
- **AgentCore Memory**: Conversation history (STM) and customer fact extraction (LTM)
- **Amazon Bedrock**: Claude Sonnet 4 via Converse API with prompt caching
- **AgentCore Runtime**: Serverless container orchestration with auto-scaling

## Project Structure

```
├── agent/              # Agent implementation
│   ├── __main__.py    # AgentCore entrypoint
│   ├── support_agent.py
│   ├── tools.py
│   ├── prompts.py
│   ├── knowledge/     # Knowledge source classes
│   └── Dockerfile
├── cdk/               # CDK infrastructure
│   ├── app.py
│   └── support_agent_stack.py
├── tests/             # Unit and integration tests
└── docs/              # Documentation : This directory is referred by an agent
```
d
## GenU Integration

This agent is designed to integrate with [GenU](https://github.com/aws-samples/generative-ai-use-cases) through the [one-click deployment process](https://github.com/aws-samples/sample-one-click-generative-ai-solutions).

The CDK stack is automatically tagged with `Integration:GenU`, which enables:
- **Automatic Discovery**: The one-click deployment process discovers this stack by the tag
- **Agent Registration**: The deployed agent is automatically registered as an available agent in GenU
- **Seamless Integration**: No manual configuration needed for GenU integration

To deploy with GenU integration, simply deploy this stack using CDK and the one-click deployment process will automatically detect and register it.

## Support

For issues or questions:

1. Check the [GitHub Issues](https://github.com/icoxfog417/personal-aws-customer-assistant/issues)
2. Review the [Design Document](spec/design.md)
3. Review the [Requirements Document](spec/requirements.md)

## License

This project is licensed under the MIT-0 License.
