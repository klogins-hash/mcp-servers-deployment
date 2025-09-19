#!/bin/bash
# Connect to MCP Management System via SSH

APP_URL="mcp-servers-lnjzg.ondigitalocean.app"
SSH_PORT="2222"
SSH_USER="mcpmanager"

echo "🔐 Connecting to MCPMaster Management System..."
echo "URL: $APP_URL"
echo "Port: $SSH_PORT"
echo "User: $SSH_USER"
echo ""

# Check if deployment is ready
echo "🔍 Checking if SSH is ready..."
if nc -z $APP_URL $SSH_PORT 2>/dev/null; then
    echo "✅ SSH port is open!"
    echo "🚀 Connecting..."
    ssh -p $SSH_PORT $SSH_USER@$APP_URL
else
    echo "⏳ SSH not ready yet. Deployment may still be in progress."
    echo "💡 Try again in a few minutes, or check deployment status with:"
    echo "   ./check-deployment.sh"
    echo ""
    echo "🔗 Once ready, connect with:"
    echo "   ssh -p $SSH_PORT $SSH_USER@$APP_URL"
fi
