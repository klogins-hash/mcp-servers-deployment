#!/bin/bash
# Setup SSH access and install MCP manager

echo "🔐 Setting up SSH access for MCP management..."

# Create SSH user (if not exists)
if ! id "mcpmanager" &>/dev/null; then
    useradd -m -s /bin/bash mcpmanager
    echo "✅ Created mcpmanager user"
fi

# Setup SSH directory
mkdir -p /home/mcpmanager/.ssh
chmod 700 /home/mcpmanager/.ssh

# Add your public key (replace with your actual key)
echo "ssh-rsa YOUR_PUBLIC_KEY_HERE your-email@example.com" >> /home/mcpmanager/.ssh/authorized_keys
chmod 600 /home/mcpmanager/.ssh/authorized_keys
chown -R mcpmanager:mcpmanager /home/mcpmanager/.ssh

# Install MCP manager globally
cp /app/management/mcp_manager.py /usr/local/bin/mcp
chmod +x /usr/local/bin/mcp

# Create symlinks for convenience
ln -sf /usr/local/bin/mcp /usr/local/bin/add-mcp
ln -sf /usr/local/bin/mcp /usr/local/bin/remove-mcp
ln -sf /usr/local/bin/mcp /usr/local/bin/list-mcp

# Setup bash aliases for mcpmanager user
cat >> /home/mcpmanager/.bashrc << 'EOF'
# MCP Management Aliases
alias mcp-add='mcp add'
alias mcp-remove='mcp remove' 
alias mcp-list='mcp list'
alias mcp-status='mcp status'
alias mcp-search='mcp search'

# Welcome message
echo "🚀 MCP Manager Ready!"
echo "Commands: mcp add <server>, mcp remove <server>, mcp list, mcp status"
echo "Quick: add xyz mcp server, remove xyz mcp server"
EOF

echo "✅ SSH setup complete!"
echo "🔑 You can now SSH with: ssh mcpmanager@your-app-domain.com"
