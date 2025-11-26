# agent/__main__.py
import os
from bedrock_agentcore import BedrockAgentCoreApp
from agent.support_agent import SupportAgent

app = BedrockAgentCoreApp()

@app.entrypoint
async def entrypoint(payload):
    # Initialize SupportAgent with wiki search tools
    agent = SupportAgent(
        wiki_repo_url="https://github.com/icoxfog417/personal-account-manager",
        wiki_local_path="./data"
    )
    
    message = payload.get("prompt", "")
    stream_messages = agent.stream_async(message)
    async for message in stream_messages:
        if "event" in message:
            yield message

if __name__ == "__main__":
    app.run()
