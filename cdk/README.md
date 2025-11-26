# CDK Deployment for Support Agent

This directory contains AWS CDK infrastructure code to deploy the Support Agent to Amazon Bedrock AgentCore Runtime.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.11+
- Node.js (for CDK CLI)
- Docker (for building container images)
- CDK v2.220.0 or later

## Required AWS Permissions

Your AWS user/role needs:
- `BedrockAgentCoreFullAccess` managed policy
- `AmazonBedrockFullAccess` managed policy
- IAM permissions to create roles
- ECR repository management
- CloudFormation stack operations

## Configuration

Agent configuration is defined in `cdk.json` under the `agent_config` context:

```json
{
  "context": {
    "agent_config": {
      "repo_url": "https://github.com/icoxfog417/personal-account-manager",
      "knowledge_dir": "docs",
      "local_path": "./repo_data",
      "system_prompt": ""
    }
  }
}
```

**Configuration Options:**
- `repo_url`: GitHub repository URL containing knowledge documents
- `knowledge_dir`: Directory within repository containing knowledge files
- `local_path`: Local path in container to store cloned repository
- `system_prompt`: Custom system prompt (optional, uses default if empty)

These values are passed to the agent container as environment variables.

## Setup

```bash
# Install CDK CLI globally
npm install -g aws-cdk

# Create virtual environment
cd cdk
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Bootstrap (First Time Only)

```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
```

## Deploy

```bash
cdk deploy
```

This will:
1. Build the Docker image from `../agent`
2. Push to auto-created ECR repository
3. Create AgentCore Runtime with auto-created IAM role
4. Output the runtime ARN for invocation

## Parameters

You can override default parameters:

```bash
cdk deploy --parameters AgentName=MyAgent --parameters NetworkMode=PRIVATE
```

## Testing

After deployment, test using AWS CLI:

```bash
# Get runtime ARN from outputs
RUNTIME_ARN=$(aws cloudformation describe-stacks \
  --stack-name SupportAgentStack \
  --query 'Stacks[0].Outputs[?OutputKey==`AgentRuntimeArn`].OutputValue' \
  --output text)

# Invoke agent
aws bedrock-agentcore invoke-agent-runtime \
  --agent-runtime-arn $RUNTIME_ARN \
  --qualifier DEFAULT \
  --payload $(echo '{"prompt": "What is AWS Lambda?"}' | base64) \
  response.json

# View response
cat response.json
```

## Cleanup

```bash
cdk destroy
```

## Troubleshooting

### Docker Build Issues
- Ensure Docker daemon is running
- Check Docker has sufficient disk space
- Verify `../agent/Dockerfile` exists

### Permission Issues
- Verify AWS credentials are configured
- Check IAM permissions listed above
- Ensure CDK bootstrap was successful

### Deployment Failures
- Check CloudFormation console for detailed error messages
- Review CloudWatch logs for runtime issues
- Verify Bedrock model access is enabled in your region
