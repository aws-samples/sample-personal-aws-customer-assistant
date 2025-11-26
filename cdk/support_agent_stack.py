from aws_cdk import (
    Stack,
    CfnParameter,
    CfnOutput,
    aws_ecr_assets as ecr_assets,
    aws_iam as iam,
    aws_bedrockagentcore as bedrockagentcore,
)
from constructs import Construct


class SupportAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get agent configuration from context
        agent_config = self.node.try_get_context("agent_config") or {}

        # Parameters
        agent_name = CfnParameter(
            self,
            "AgentName",
            type="String",
            default="SupportAgent",
            description="Name for the agent runtime",
        )

        network_mode = CfnParameter(
            self,
            "NetworkMode",
            type="String",
            default="PUBLIC",
            description="Network mode for AgentCore resources",
            allowed_values=["PUBLIC", "PRIVATE"],
        )

        # Docker image asset - automatically builds and pushes to ECR
        docker_image = ecr_assets.DockerImageAsset(
            self,
            "AgentImage",
            directory="../agent",
            platform=ecr_assets.Platform.LINUX_ARM64,
        )

        # Create IAM role for AgentCore Runtime
        agent_role = iam.Role(
            self,
            "AgentRole",
            assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
            inline_policies={
                "AgentCorePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            sid="ECRImageAccess",
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "ecr:BatchGetImage",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchCheckLayerAvailability",
                            ],
                            resources=[f"arn:aws:ecr:{self.region}:{self.account}:repository/*"],
                        ),
                        iam.PolicyStatement(
                            sid="ECRTokenAccess",
                            effect=iam.Effect.ALLOW,
                            actions=["ecr:GetAuthorizationToken"],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "logs:DescribeLogStreams",
                                "logs:CreateLogGroup",
                                "logs:DescribeLogGroups",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            resources=[
                                f"arn:aws:logs:{self.region}:{self.account}:log-group:/aws/bedrock-agentcore/runtimes/*"
                            ],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "xray:PutTraceSegments",
                                "xray:PutTelemetryRecords",
                                "xray:GetSamplingRules",
                                "xray:GetSamplingTargets",
                            ],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=["cloudwatch:PutMetricData"],
                            resources=["*"],
                            conditions={
                                "StringEquals": {"cloudwatch:namespace": "bedrock-agentcore"}
                            },
                        ),
                        iam.PolicyStatement(
                            sid="BedrockModelInvocation",
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeModel",
                                "bedrock:InvokeModelWithResponseStream",
                            ],
                            resources=[
                                "arn:aws:bedrock:*::foundation-model/*",
                                f"arn:aws:bedrock:{self.region}:{self.account}:*",
                            ],
                        ),
                    ]
                )
            },
        )

        # Build environment variables from agent config
        env_vars = {
            "AWS_DEFAULT_REGION": self.region,
            "AGENT_REPO_URL": agent_config.get("repo_url", ""),
            "AGENT_KNOWLEDGE_DIR": agent_config.get("knowledge_dir", "docs"),
            "AGENT_LOCAL_PATH": agent_config.get("local_path", "./repo_data"),
        }

        # Add system prompt if provided
        if agent_config.get("system_prompt"):
            env_vars["AGENT_SYSTEM_PROMPT"] = agent_config["system_prompt"]

        # AgentCore Runtime
        agent_runtime = bedrockagentcore.CfnRuntime(
            self,
            "AgentRuntime",
            agent_runtime_name=f"{self.stack_name}_{agent_name.value_as_string}",
            agent_runtime_artifact=bedrockagentcore.CfnRuntime.AgentRuntimeArtifactProperty(
                container_configuration=bedrockagentcore.CfnRuntime.ContainerConfigurationProperty(
                    container_uri=docker_image.image_uri
                )
            ),
            network_configuration=bedrockagentcore.CfnRuntime.NetworkConfigurationProperty(
                network_mode=network_mode.value_as_string
            ),
            protocol_configuration="HTTP",
            role_arn=agent_role.role_arn,
            description=f"Support agent runtime for {self.stack_name}",
            environment_variables=env_vars,
        )

        # Outputs
        CfnOutput(
            self,
            "AgentRuntimeId",
            description="ID of the created agent runtime",
            value=agent_runtime.attr_agent_runtime_id,
        )

        CfnOutput(
            self,
            "AgentRuntimeArn",
            description="ARN of the created agent runtime",
            value=agent_runtime.attr_agent_runtime_arn,
        )

        CfnOutput(
            self,
            "AgentRoleArn",
            description="ARN of the agent execution role",
            value=agent_role.role_arn,
        )

        CfnOutput(
            self,
            "ImageUri",
            description="Docker image URI in ECR",
            value=docker_image.image_uri,
        )
