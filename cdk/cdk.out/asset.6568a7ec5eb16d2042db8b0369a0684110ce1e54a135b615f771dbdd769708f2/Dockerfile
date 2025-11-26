FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Install git for GitPython
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir aws-opentelemetry-distro==0.10.1

# Non-root user for security
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

# Expose ports
EXPOSE 8080 8000

# Copy entire agent directory to preserve package structure
COPY . ./agent

# Start with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "-m", "agent"]
