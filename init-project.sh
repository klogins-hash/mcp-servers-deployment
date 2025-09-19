#!/bin/bash
# Initialize MCP Servers Deployment Project

echo "🚀 Initializing MCP Servers Deployment Project..."

# Check if we're in the right directory
if [ ! -f "app.yaml" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Get user input
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your GitHub repository name (default: mcp-servers-deployment): " GITHUB_REPO
GITHUB_REPO=${GITHUB_REPO:-mcp-servers-deployment}

read -p "Enter your SSH public key (or press Enter to skip): " SSH_PUBLIC_KEY

echo ""
echo "🔧 Configuring project..."

# Update app.yaml with GitHub username
sed -i.bak "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" app.yaml
echo "✅ Updated app.yaml with GitHub username"

# Update SSH key if provided
if [ ! -z "$SSH_PUBLIC_KEY" ]; then
    sed -i.bak "s/ssh-rsa YOUR_PUBLIC_KEY_HERE your-email@example.com/$SSH_PUBLIC_KEY/g" scripts/setup-ssh.sh
    echo "✅ Updated SSH public key"
fi

# Initialize git repository
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: MCP Servers Deployment System"
    echo "✅ Initialized git repository"
fi

# Add GitHub remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$GITHUB_REPO.git" 2>/dev/null || true
echo "✅ Added GitHub remote"

echo ""
echo "🎉 Project initialized successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create a GitHub repository: https://github.com/new"
echo "2. Set environment variables:"
echo "   export DIGITALOCEAN_TOKEN='your_do_token'"
echo "   export GITHUB_TOKEN='your_github_token'"
echo "   export GITHUB_REPO='$GITHUB_USERNAME/$GITHUB_REPO'"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. Deploy to DigitalOcean:"
echo "   python deploy/auto-deploy.py"
echo ""
echo "5. SSH into your app and start managing MCP servers:"
echo "   ssh mcpmanager@your-app-domain.com"
echo "   mcp add github"
echo ""
echo "💡 See README.md for detailed instructions!"
