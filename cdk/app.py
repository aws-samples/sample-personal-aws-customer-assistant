#!/usr/bin/env python3
import aws_cdk as cdk
from support_agent_stack import SupportAgentStack

app = cdk.App()
SupportAgentStack(app, "SupportAgentStack")

app.synth()
