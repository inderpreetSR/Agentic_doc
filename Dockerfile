# Build stage
FROM python:3.11.8-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY dsaa_agents_streamlit/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11.8-slim

# Labels for maintainability
LABEL maintainer="inderpreetSR"
LABEL version="1.0.0"
LABEL description="DSAA Agents Streamlit Application"
LABEL org.opencontainers.image.source="https://github.com/inderpreetSR/Agentic_doc"

WORKDIR /app

# Create non-root user (CRITICAL SECURITY FIX)
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit && \
    mkdir -p /app/dsaa_agents_streamlit/data /app/dsaa_agents_streamlit/logs && \
    chown -R streamlit:streamlit /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder --chown=streamlit:streamlit /root/.local /home/streamlit/.local

# Copy application code
COPY --chown=streamlit:streamlit dsaa_agents_streamlit/ ./dsaa_agents_streamlit/

# Switch to non-root user
USER streamlit

# Update PATH for user-installed packages
ENV PATH=/home/streamlit/.local/bin:$PATH

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "dsaa_agents_streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
