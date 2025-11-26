FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir aws-opentelemetry-distro==0.10.1

# Environment variables
ENV AWS_REGION=us-west-2
ENV AWS_DEFAULT_REGION=us-west-2

# Non-root user for security
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

# Expose ports
EXPOSE 8080 8000

# Copy agent code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ping || exit 1

# Start with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "-m", "agent"]
