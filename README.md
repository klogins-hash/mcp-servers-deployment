# 🚀 MCP Servers Deployment with SSH Management

A comprehensive DigitalOcean App Platform deployment system that allows you to dynamically add/remove MCP (Model Context Protocol) servers with simple SSH commands like `add xyz mcp server`.

## ✨ Features

- **SSH Management Interface**: Manage MCP servers via SSH with natural language commands
- **Official MCP Server Catalog**: Pre-configured support for 8+ official MCP servers
- **Auto-Deployment**: Automatic deployment to DigitalOcean App Platform via GitHub integration
- **LangGraph Integration**: Auto-generated configuration for LangGraph applications
- **Health Monitoring**: Built-in health checks and status monitoring
- **Rollback Support**: Backup and rollback functionality for safe deployments

## 🏗️ Architecture

```
mcp-servers-deployment/
├── management/          # Core management system
│   ├── mcp_manager.py   # Main CLI interface
│   ├── server_registry.py # MCP server catalog
│   ├── deployment_engine.py # Deployment automation
│   └── config_templates.py # Configuration generation
├── scripts/             # Setup and utility scripts
├── config/              # Configuration files
├── deploy/              # Deployment automation
└── app.yaml            # DigitalOcean App Platform config
```

## 🚀 Quick Start

### 1. Setup Repository

```bash
# Clone or create your repository
git clone https://github.com/YOUR_USERNAME/mcp-servers-deployment.git
cd mcp-servers-deployment

# Update app.yaml with your GitHub repo
sed -i 's/YOUR_GITHUB_USERNAME/your-actual-username/g' app.yaml
```

### 2. Deploy to DigitalOcean

```bash
# Set environment variables
export DIGITALOCEAN_TOKEN="your_do_token"
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPO="your-username/mcp-servers-deployment"

# Deploy using the auto-deploy script
python deploy/auto-deploy.py
```

### 3. SSH Access

Once deployed, SSH into your management interface:

```bash
ssh mcpmanager@your-app-domain.ondigitalocean.app
```

## 🎛️ Management Commands

### Add MCP Servers

```bash
# Standard format
mcp add github
mcp add postgres
mcp add slack

# Natural language format
add stripe mcp server
add memory mcp server
```

### Remove MCP Servers

```bash
# Standard format
mcp remove github

# Natural language format
remove postgres mcp server
```

### List and Status

```bash
mcp list                 # List deployed servers
mcp list available      # List all available servers
mcp status              # System status dashboard
mcp search database     # Search for servers
```

### LangGraph Integration

```bash
mcp config langgraph    # Generate LangGraph configuration
```

## 📦 Available MCP Servers

| Server | Description | Capabilities |
|--------|-------------|--------------|
| **fetch** | Web Content Fetch | web_fetch, html_to_markdown |
| **git** | Git Repository Operations | git_read, git_search, git_manipulate |
| **filesystem** | Filesystem Operations | file_read, file_write, directory_ops |
| **memory** | Knowledge Graph Memory | memory_store, memory_retrieve, graph_ops |
| **postgres** | PostgreSQL Database | db_read, db_write, schema_inspect |
| **github** | GitHub Integration | github_repos, github_issues, github_prs |
| **slack** | Slack Integration | slack_channels, slack_messages, slack_users |
| **stripe** | Stripe Payments | payments, customers, subscriptions |

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set these in DigitalOcean:

```bash
# Required
DIGITALOCEAN_TOKEN=your_digitalocean_token
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your-username/mcp-servers-deployment

# Optional MCP Server Configs
GITHUB_TOKEN=your_github_personal_access_token
SLACK_TOKEN=xoxb-your-slack-bot-token
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
POSTGRES_URL=postgresql://user:pass@host:port/db
```

### SSH Public Key

Add your SSH public key to `scripts/setup-ssh.sh`:

```bash
echo "ssh-rsa YOUR_PUBLIC_KEY_HERE your-email@example.com" >> /home/mcpmanager/.ssh/authorized_keys
```

## 🔗 LangGraph Integration

After deploying servers, get your configuration:

```bash
# SSH into your app
ssh mcpmanager@your-app-domain.com

# Generate LangGraph config
mcp config langgraph
```

This outputs:

```python
# Auto-generated LangGraph MCP configuration
MCP_SERVERS = {
    "fetch": "https://mcp-fetch-xyz.ondigitalocean.app",
    "github": "https://mcp-github-xyz.ondigitalocean.app", 
    "postgres": "https://mcp-postgres-xyz.ondigitalocean.app"
}

# Use in your LangGraph application
from langgraph import MCPClient
client = MCPClient(servers=MCP_SERVERS)
```

## 🧪 Local Testing

```bash
# Make test script executable
chmod +x scripts/local-test.sh

# Run local tests
./scripts/local-test.sh
```

## 🔄 Backup & Rollback

```bash
# Create backup
python deploy/rollback.py backup "Before major changes"

# List backups
python deploy/rollback.py list

# Rollback to backup
python deploy/rollback.py rollback backup_20250119_143022
```

## 💰 Cost Estimation

- **Management Interface**: ~$5/month (basic-s instance)
- **Each MCP Server**: ~$5/month (basic-xxs instance)
- **Total for 5 servers**: ~$30/month

## 🛠️ Development

### Project Structure

```
management/
├── server_registry.py    # MCP server catalog and registry
├── mcp_manager.py       # Main CLI interface
├── deployment_engine.py # DigitalOcean deployment automation
└── config_templates.py  # Configuration template generation

scripts/
├── setup-ssh.sh        # SSH access configuration
├── install-manager.sh  # System installation
├── health-check.py     # Health monitoring service
└── local-test.sh       # Local testing utilities
```

### Adding Custom MCP Servers

```python
# In server_registry.py
registry.add_community_server(
    name="custom-server",
    package_name="mcp-server-custom",
    description="My custom MCP server",
    capabilities=["custom_capability"],
    port=8090
)
```

## 🚨 Troubleshooting

### SSH Connection Issues

```bash
# Check SSH service status
ssh mcpmanager@your-app.com "systemctl status ssh"

# Check logs
ssh mcpmanager@your-app.com "tail -f /var/log/auth.log"
```

### Deployment Issues

```bash
# Check app logs in DigitalOcean dashboard
# Or via SSH:
ssh mcpmanager@your-app.com "tail -f /app/logs/deployment.log"
```

### Server Not Starting

```bash
# Check specific server logs
mcp status
# Look for error messages in the output
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your MCP server to the registry
4. Test locally with `./scripts/local-test.sh`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: [MCP Protocol Docs](https://modelcontextprotocol.io)

---

**🎉 Happy MCP Server Management!** 

Deploy once, manage forever with simple SSH commands like `add xyz mcp server`.
