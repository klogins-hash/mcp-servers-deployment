#!/bin/bash
# Create a minimal SSH-enabled droplet for MCP management

echo "🚀 Creating SSH-enabled MCP management droplet..."

# Create a small droplet with your SSH key
doctl compute droplet create mcpmaster-ssh \
  --image ubuntu-22-04-x64 \
  --size s-1vcpu-1gb \
  --region nyc1 \
  --ssh-keys $(doctl compute ssh-key list --format ID --no-header | head -1) \
  --wait

# Get the droplet IP
DROPLET_IP=$(doctl compute droplet list mcpmaster-ssh --format PublicIPv4 --no-header)

echo "✅ Droplet created with IP: $DROPLET_IP"
echo "🔧 Setting up MCP management tools..."

# Wait for SSH to be ready
sleep 30

# Install MCP management tools
ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'EOF'
# Update system
apt update && apt upgrade -y

# Install Python and required tools
apt install -y python3 python3-pip git curl

# Install uv for Python package management
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Clone the MCP management repository
git clone https://github.com/klogins-hash/mcp-servers-deployment.git /opt/mcp-manager
cd /opt/mcp-manager

# Install dependencies
pip3 install -r requirements.txt

# Make MCP manager globally available
cp management/mcp_manager.py /usr/local/bin/mcp
chmod +x /usr/local/bin/mcp

# Create welcome message
echo '
🚀 MCPMaster SSH Management Ready!

Available commands:
  mcp status              - Show system status
  mcp list               - List deployed servers  
  mcp list available     - List all available servers
  mcp add <server>       - Add/deploy an MCP server
  mcp remove <server>    - Remove an MCP server
  mcp search <query>     - Search for servers
  mcp config langgraph   - Generate LangGraph config

Examples:
  mcp add github
  mcp add postgres
  add slack mcp server
' > /etc/motd

echo "✅ MCP management tools installed!"
EOF

echo ""
echo "🎉 SSH-enabled MCP management droplet ready!"
echo "🔗 Connect with: ssh root@$DROPLET_IP"
echo "💰 Cost: ~$6/month for SSH access"
