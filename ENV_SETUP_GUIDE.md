# 🔐 Environment Variables Setup Guide

## 🎯 **Required API Keys for MCP Servers**

### **GitHub Server**
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```
**How to get**: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
**Permissions needed**: `repo`, `read:user`, `read:org`

### **Slack Server**
```bash
SLACK_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
```
**How to get**: https://api.slack.com/apps → Create New App → OAuth & Permissions → Bot User OAuth Token
**Scopes needed**: `chat:write`, `channels:read`, `users:read`

### **Stripe Server**
```bash
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key_here
# OR for testing:
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key_here
```
**How to get**: Stripe Dashboard → Developers → API keys → Secret key

### **PostgreSQL Server**
```bash
POSTGRES_URL=postgresql://username:password@hostname:5432/database_name
```
**Examples**:
- Local: `postgresql://postgres:password@localhost:5432/mydb`
- DigitalOcean: `postgresql://user:pass@db-postgresql-nyc1-12345-do-user-123456-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require`
- AWS RDS: `postgresql://username:password@mydb.abc123.us-east-1.rds.amazonaws.com:5432/mydb`

## 🛠️ **Optional Configuration Variables**

### **General MCP Settings**
```bash
MCP_LOG_LEVEL=info                    # debug, info, warning, error
ROBOTS_TXT_RESPECT=true               # Respect robots.txt for fetch server
FETCH_TIMEOUT=30                      # Timeout for web requests (seconds)
MAX_FILE_SIZE=10485760               # Max file size for uploads (bytes)
```

### **GitHub Specific**
```bash
GITHUB_REPO_ACCESS=public            # public, private, all
GITHUB_DEFAULT_BRANCH=main           # Default branch for operations
```

### **Slack Specific**
```bash
SLACK_WORKSPACE_ID=T1234567890       # Your workspace ID
SLACK_DEFAULT_CHANNEL=#general       # Default channel for messages
```

### **Memory Server**
```bash
MEMORY_PERSIST=true                  # Persist memory between restarts
MEMORY_MAX_SIZE=1000000             # Max memory entries
```

## 🚀 **How to Add Environment Variables**

### **Option 1: DigitalOcean Dashboard**
1. Go to: https://cloud.digitalocean.com/apps
2. Find your `mcpmaster` app
3. Click **Settings** → **Environment Variables**
4. Click **Add Variable**
5. Enter key/value pairs from above
6. Set sensitive keys as **Encrypted**
7. Click **Save**

### **Option 2: Using doctl CLI**
```bash
# Update app with new environment variables
doctl apps update 8d4c802b-f670-44ff-954f-68d0e06f33d6 --spec app-with-env-vars.yaml
```

### **Option 3: Bulk Environment File**
Create a `.env` file locally (for reference):
```bash
# Copy this template and fill in your actual values
GITHUB_TOKEN=ghp_your_token_here
SLACK_TOKEN=xoxb_your_token_here  
STRIPE_SECRET_KEY=sk_live_your_key_here
POSTGRES_URL=postgresql://user:pass@host:5432/db
ROBOTS_TXT_RESPECT=true
MCP_LOG_LEVEL=info
```

## 🔒 **Security Best Practices**

### **✅ DO:**
- Use encrypted/secret variables for API keys
- Use environment-specific keys (test vs production)
- Rotate keys regularly
- Use least-privilege permissions

### **❌ DON'T:**
- Commit API keys to Git
- Use production keys in development
- Share keys in plain text
- Use overly broad permissions

## 🧪 **Testing Your Setup**

Once you've added the environment variables:

1. **Visit your dashboard**: https://mcp-servers-lnjzg.ondigitalocean.app
2. **Deploy a server**: Click "🐙 Deploy GitHub"
3. **Check logs**: Monitor for authentication errors
4. **Test functionality**: Try the server features

## 📋 **Quick Setup Checklist**

- [ ] GitHub Personal Access Token created
- [ ] Slack Bot Token obtained  
- [ ] Stripe API key ready
- [ ] PostgreSQL connection string prepared
- [ ] Environment variables added to DigitalOcean
- [ ] App redeployed with new variables
- [ ] Servers tested and working

## 🆘 **Common Issues**

**Problem**: "Authentication failed"
**Solution**: Check API key format and permissions

**Problem**: "Connection refused" 
**Solution**: Verify database URL format and network access

**Problem**: "Rate limited"
**Solution**: Check API key quotas and usage limits

Need help getting any specific API keys? Let me know which service you want to set up first!
