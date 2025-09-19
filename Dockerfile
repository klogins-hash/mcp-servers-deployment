FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    openssh-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python package management
RUN pip install uv

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x scripts/*.sh
RUN chmod +x management/mcp_manager.py

# Setup SSH
RUN mkdir -p /var/run/sshd
RUN echo 'Port 2222' >> /etc/ssh/sshd_config
RUN echo 'PermitRootLogin no' >> /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config
RUN echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
RUN echo 'AllowUsers mcpmanager' >> /etc/ssh/sshd_config

# Create config directory
RUN mkdir -p /app/config

# Expose ports
EXPOSE 8000 2222

# Create startup script
RUN echo '#!/bin/bash\n\
# Start SSH daemon\n\
service ssh start\n\
# Run setup scripts\n\
/app/scripts/install-manager.sh\n\
/app/scripts/setup-ssh.sh\n\
# Start health check server\n\
python /app/scripts/health-check.py' > /app/start.sh

RUN chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]
