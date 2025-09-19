#!/usr/bin/env python3
"""
Auto-deployment script for MCP servers
"""
import os
import sys
import json
import subprocess
from typing import Dict, Any

def deploy_to_digitalocean():
    """Deploy the MCP management system to DigitalOcean App Platform"""
    
    print("🚀 Starting deployment to DigitalOcean App Platform...")
    
    # Check required environment variables
    required_vars = ['DIGITALOCEAN_TOKEN', 'GITHUB_REPO']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("💡 Please set these variables before deploying.")
        return False
    
    # Initialize git repository if not already done
    if not os.path.exists('.git'):
        print("📦 Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    # Create DigitalOcean app using doctl (if available)
    try:
        print("🌊 Creating DigitalOcean app...")
        result = subprocess.run([
            'doctl', 'apps', 'create', 
            '--spec', 'app.yaml'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ App created successfully!")
            print(f"📋 Output: {result.stdout}")
        else:
            print(f"⚠️  doctl not available or failed: {result.stderr}")
            print("💡 Please create the app manually using the DigitalOcean dashboard")
            print("📄 Use the app.yaml file in this directory")
            
    except FileNotFoundError:
        print("⚠️  doctl CLI not found")
        print("💡 Please install doctl or create the app manually")
        print("📄 Use the app.yaml file in this directory")
    
    print("\n🎉 Deployment setup complete!")
    print("📋 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Configure environment variables in DigitalOcean dashboard")
    print("3. SSH into your app: ssh mcpmanager@your-app-domain.com")
    print("4. Start managing MCP servers: mcp add github")
    
    return True

def setup_github_integration():
    """Setup GitHub integration for auto-deployment"""
    
    github_repo = os.getenv('GITHUB_REPO')
    if not github_repo:
        print("❌ GITHUB_REPO environment variable not set")
        return False
    
    print(f"🐙 Setting up GitHub integration for {github_repo}...")
    
    # Add GitHub remote if not exists
    try:
        subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                      capture_output=True, check=True)
        print("✅ GitHub remote already configured")
    except subprocess.CalledProcessError:
        github_url = f"https://github.com/{github_repo}.git"
        subprocess.run(['git', 'remote', 'add', 'origin', github_url], check=True)
        print(f"✅ Added GitHub remote: {github_url}")
    
    # Push to GitHub
    try:
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ Code pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to push to GitHub: {e}")
        print("💡 Please push manually or check your GitHub token")
    
    return True

def main():
    """Main deployment function"""
    
    if len(sys.argv) > 1 and sys.argv[1] == 'github':
        setup_github_integration()
    else:
        deploy_to_digitalocean()

if __name__ == "__main__":
    main()
