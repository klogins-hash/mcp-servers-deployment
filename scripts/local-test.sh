#!/bin/bash
# Local testing script for MCP manager

echo "🧪 Testing MCP Manager locally..."

# Set up test environment
export PYTHONPATH="/Users/franksimpson/CascadeProjects/mcp-servers-deployment:$PYTHONPATH"

# Test server registry
echo "📦 Testing server registry..."
python3 -c "
import sys
sys.path.append('management')
from server_registry import MCPServerRegistry

registry = MCPServerRegistry()
print(f'✅ Registry loaded with {len(registry.servers)} servers')

# Test search
results = registry.search_servers('github')
print(f'🔍 Search for \"github\" found {len(results)} results')

# Test get server
server = registry.get_server('fetch')
if server:
    print(f'✅ Found server: {server.name}')
else:
    print('❌ Server not found')
"

# Test MCP manager
echo "🎛️  Testing MCP manager..."
cd management
python3 mcp_manager.py status
python3 mcp_manager.py list available

echo "✅ Local tests completed!"
