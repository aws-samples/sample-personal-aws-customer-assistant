# AWS Customer Support Agent

An AI-powered AWS customer support agent that serves as an alternative to traditional account managers, providing personalized assistance to thousands of AWS customers through intelligent conversation and knowledge retrieval.

## 🎯 Objectives

- **Remove obstacles** for every AWS customer
- **Provide efficient and exciting** onboarding experiences
- **Reduce opportunity loss** from lack of dedicated account manager support
- **Free account managers** from repetitive tasks to focus on strategic initiatives

## 💡 Benefits

### For Customers
- **24/7 Availability**: Get AWS support anytime without waiting for account manager availability
- **Personalized Assistance**: Agent remembers your AWS environment, preferences, and past issues
- **Instant Answers**: Quick responses to common questions about billing, credits, and AWS services
- **Consistent Experience**: Access to curated knowledge base maintained by AWS experts

### For Organizations
- **Scalability**: Support thousands of customers with a single agent deployment
- **Cost Efficiency**: Reduce repetitive support tasks while maintaining quality
- **Knowledge Sharing**: Centralized wiki ensures consistent, up-to-date information
- **Multi-User Support**: Single memory resource serves entire IT department with user isolation

## 🏗️ Architecture

Built on AWS managed services for reliability and scalability:

- **Strands Agent**: Agent orchestration and tool management
- **AgentCore Runtime**: Serverless container hosting with auto-scaling
- **AgentCore Memory**: Conversation history and semantic knowledge extraction
- **Amazon Bedrock**: Claude Sonnet 4 with Converse API and prompt caching
- **GitHub Wiki**: Centralized knowledge base for AWS best practices

### Memory Strategy

**Multi-User Architecture**:
- Single shared Memory resource for entire IT department
- Per-user isolation via Actor ID (e.g., `user-{employee-id}`)
- Per-conversation tracking via Session ID (auto-generated UUID)

**Dual-Namespace Approach**:
- **User-Specific**: `support/facts/{actorId}`, `support/preferences/{actorId}`
- **Company-Wide**: `company/aws-environment`, `company/policies`

## 🚀 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- Python 3.9+
- Docker (for local development)
- Git

### One-Click Deployment

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?stackName=aws-support-agent&templateURL=https://your-bucket.s3.amazonaws.com/deployment-stack.yaml)

Click the button above to deploy the agent to your AWS account. The CloudFormation stack will:

1. Create AgentCore Runtime environment
2. Provision AgentCore Memory with semantic strategies
3. Build and deploy Docker container
4. Clone GitHub wiki repository
5. Send completion notification to your email

**Parameters**:
- `NotificationEmailAddress`: Email for deployment notifications
- `Environment`: dev/staging/prod
- `WikiRepoUrl`: GitHub wiki repository URL (default: aws-samples wiki)

### Manual Deployment

```bash
# Clone repository
git clone https://github.com/your-org/personal-account-manager.git
cd personal-account-manager

# Install dependencies
pip install -r requirements.txt

# Configure AgentCore
agentcore configure --entrypoint src/agent/support_agent.py

# Deploy to AgentCore Runtime
agentcore launch

# Get endpoint URL
agentcore status
```

## 📖 Usage

### Via External Chat UI

The agent is designed to be integrated with external chat applications via AgentCore Runtime HTTP/WebSocket endpoints.

**Example Integration**:
```bash
# Invoke agent with user context
curl -X POST https://your-agent-endpoint.amazonaws.com/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I set up billing alerts?",
    "actor_id": "user-alice",
    "session_id": "session-123"
  }'
```

### Via AgentCore CLI (Testing)

```bash
# Start conversation
agentcore invoke '{"message": "What are AWS credits?"}' \
  --actor-id user-alice \
  --session-id session-123

# Continue conversation (session persisted)
agentcore invoke '{"message": "How do I apply for them?"}'

# New user, new session
agentcore invoke '{"message": "Explain VPC setup"}' \
  --actor-id user-bob \
  --session-id session-456
```

## 🔧 Configuration

### Environment Variables

```bash
# AgentCore Memory
BEDROCK_AGENTCORE_MEMORY_ID=mem-xxxxx
AWS_REGION=us-west-2

# GitHub Wiki
WIKI_REPO_URL=https://github.com/aws-samples/sample-one-click-generative-ai-solutions.wiki.git
WIKI_LOCAL_PATH=/tmp/wiki

# Bedrock Model
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-20250514-v1:0
```

### AgentCore Configuration

Edit `.bedrock_agentcore.yaml`:

```yaml
runtime:
  memory: 2048
  timeout: 300
  
memory:
  memory_id: ${BEDROCK_AGENTCORE_MEMORY_ID}
  strategies:
    - type: semantic
      namespaces:
        - support/facts/{actorId}
        - support/preferences/{actorId}
        - company/aws-environment
        - company/policies
```

## 📁 Project Structure

```
personal-account-manager/
├── src/
│   ├── agent/
│   │   ├── support_agent.py    # Main agent implementation
│   │   └── tools.py            # Tool definitions
│   ├── knowledge/
│   │   └── wiki_source.py      # Wiki file operations
│   └── config/
│       └── settings.py         # Configuration management
├── infrastructure/
│   ├── cloudformation/
│   │   └── deployment-stack.yaml
│   └── scripts/
│       └── deploy.sh
├── tests/
│   ├── unit/
│   └── integration/
├── spec/
│   ├── requirements.md
│   └── design.md
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=src tests/
```

## 📊 Monitoring

### CloudWatch Metrics

- Response latency (p50, p95, p99)
- Memory retrieval accuracy
- Wiki search relevance
- Error rates

### X-Ray Tracing

AgentCore Runtime automatically instruments your agent with X-Ray for distributed tracing.

Access traces in AWS Console:
```
CloudWatch → X-Ray → Traces → Transaction Search
```

## 🔐 Security

- **IAM Roles**: Least-privilege access for AgentCore Runtime
- **Memory Isolation**: User data isolated by Actor ID
- **Audit Logs**: All interactions logged to CloudWatch
- **Encryption**: Data encrypted at rest and in transit

## 💰 Cost Optimization

- **Pay-per-request**: No idle costs with AgentCore Runtime
- **Prompt Caching**: Reduces Bedrock token costs by ~90%
- **Semantic Search**: No vector database infrastructure costs
- **Auto-scaling**: Resources scale with demand

**Estimated Cost**: $0.05-0.10 per interaction

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ GitHub wiki integration
- ✅ Conversation memory (STM + LTM)
- ✅ Basic Q&A with context retrieval
- ✅ One-click CloudFormation deployment

### Phase 2 (Planned)
- 📧 Email interface (SES integration)
- 🔧 Command execution (billing alerts, credits)
- 📁 Google Drive integration
- 🔐 AgentCore Identity (OAuth)
- 🌐 Multi-language support

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

- **Documentation**: See `spec/` directory for detailed design and requirements
- **Issues**: Report bugs via GitHub Issues
- **Questions**: Contact your AWS account team

## 🙏 Acknowledgments

- Built with [Strands Agent](https://github.com/awslabs/strands-agents)
- Powered by [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- Knowledge base from [AWS Samples](https://github.com/aws-samples/)

---

**Note**: This agent provides the backend implementation only. Chat UI is provided by external applications that integrate via AgentCore Runtime endpoints.
