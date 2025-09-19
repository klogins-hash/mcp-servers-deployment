#!/bin/bash
# Install and configure MCP manager on first run

echo "📦 Installing MCP Management System..."

# Install required Python packages
pip install -r /app/requirements.txt

# Setup management directories
mkdir -p /app/config
mkdir -p /app/logs

# Initialize server registry
python3 -c "
from management.server_registry import MCPServerRegistry
registry = MCPServerRegistry()
print('✅ Server registry initialized')
print(f'📦 {len(registry.servers)} official servers available')
"

# Create initial deployed-servers.json
echo '{}' > /app/config/deployed-servers.json

# Setup Git configuration
git config --global user.email "mcp-manager@yourapp.com"
git config --global user.name "MCP Manager"

# Setup GitHub token (if provided)
if [ ! -z "$GITHUB_TOKEN" ]; then
    git remote set-url origin https://$GITHUB_TOKEN@github.com/$GITHUB_REPO.git
    echo "✅ GitHub authentication configured"
fi

echo "🎉 MCP Management System installed!"
echo "Usage: mcp add <server_name>"
echo "Example: mcp add github"
echo "Example: add postgres mcp server"
