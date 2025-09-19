#!/bin/bash
# Check DigitalOcean App deployment status

APP_ID="8d4c802b-f670-44ff-954f-68d0e06f33d6"

echo "🚀 Checking MCP Servers deployment status..."
echo "App ID: $APP_ID"
echo ""

# Get app status
doctl apps get $APP_ID

echo ""
echo "🔍 Checking for live URL..."

# Try to get the live URL from app info
doctl apps get $APP_ID --output json | jq -r '.live_url // "Not yet available"'

echo ""
echo "📊 Recent deployments:"
doctl apps list-deployments $APP_ID --format ID,Phase,Progress,CreatedAt

echo ""
echo "💡 Once deployment is complete, you can:"
echo "1. Visit your app URL (will be shown above when ready)"
echo "2. SSH into the management interface"
echo "3. Start adding MCP servers with: mcp add github"
