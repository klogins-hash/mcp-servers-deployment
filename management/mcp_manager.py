#!/usr/bin/env python3
"""
MCP Manager - CLI for managing MCP servers on DigitalOcean App Platform
"""
import os
import json
import sys
import subprocess
import argparse
from typing import Dict, List
from server_registry import MCPServerRegistry, MCPServerInfo
from deployment_engine import DeploymentEngine
from config_templates import ConfigTemplateEngine

class MCPManager:
    """Main MCP management interface"""
    
    def __init__(self):
        self.registry = MCPServerRegistry()
        self.deployment = DeploymentEngine()
        self.config_engine = ConfigTemplateEngine()
        self.current_servers = self._load_current_servers()
    
    def _load_current_servers(self) -> Dict:
        """Load currently deployed servers"""
        try:
            with open('/app/config/deployed-servers.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_current_servers(self):
        """Save current server state"""
        os.makedirs('/app/config', exist_ok=True)
        with open('/app/config/deployed-servers.json', 'w') as f:
            json.dump(self.current_servers, f, indent=2)
    
    def add_server(self, server_name: str, custom_env: Dict = None) -> bool:
        """Add a new MCP server"""
        print(f"🔍 Looking for MCP server: {server_name}")
        
        # Check if server exists in registry
        server_info = self.registry.get_server(server_name)
        if not server_info:
            print(f"❌ Server '{server_name}' not found in registry.")
            print(f"💡 Available servers: {', '.join(self.registry.list_servers())}")
            return False
        
        # Check if already deployed
        if server_name in self.current_servers:
            print(f"⚠️  Server '{server_name}' is already deployed.")
            return False
        
        print(f"✅ Found server: {server_info.name}")
        print(f"📝 Description: {server_info.description}")
        print(f"🔧 Capabilities: {', '.join(server_info.capabilities)}")
        
        # Merge environment variables
        env_vars = server_info.env_vars.copy()
        if custom_env:
            env_vars.update(custom_env)
        
        # Generate configuration
        config = self.config_engine.generate_server_config(server_info, env_vars)
        
        # Deploy server
        print(f"🚀 Deploying {server_name}...")
        success = self.deployment.deploy_server(server_name, config)
        
        if success:
            self.current_servers[server_name] = {
                "info": server_info.__dict__,
                "env_vars": env_vars,
                "deployed_at": "2025-01-xx",  # Would be current timestamp
                "status": "active"
            }
            self._save_current_servers()
            print(f"🎉 Successfully deployed {server_name}!")
            print(f"🌐 Available at: https://mcp-{server_name}-xyz.ondigitalocean.app")
            return True
        else:
            print(f"❌ Failed to deploy {server_name}")
            return False
    
    def remove_server(self, server_name: str) -> bool:
        """Remove an MCP server"""
        if server_name not in self.current_servers:
            print(f"❌ Server '{server_name}' is not currently deployed.")
            return False
        
        print(f"🗑️  Removing {server_name}...")
        success = self.deployment.remove_server(server_name)
        
        if success:
            del self.current_servers[server_name]
            self._save_current_servers()
            print(f"✅ Successfully removed {server_name}")
            return True
        else:
            print(f"❌ Failed to remove {server_name}")
            return False
    
    def list_deployed(self):
        """List currently deployed servers"""
        if not self.current_servers:
            print("📭 No MCP servers currently deployed.")
            return
        
        print("🚀 Currently Deployed MCP Servers:")
        print("=" * 50)
        for name, details in self.current_servers.items():
            info = details['info']
            print(f"• {name}: {info['name']}")
            print(f"  Description: {info['description']}")
            print(f"  Port: {info['default_port']}")
            print(f"  Status: {details['status']}")
            print(f"  URL: https://mcp-{name}-xyz.ondigitalocean.app")
            print()
    
    def list_available(self):
        """List all available servers"""
        print("📦 Available MCP Servers:")
        print("=" * 50)
        for name, server in self.registry.servers.items():
            status = "🟢 DEPLOYED" if name in self.current_servers else "⚪ Available"
            official = "🏢 Official" if server.official else "👥 Community"
            print(f"{status} {official} {name}: {server.name}")
            print(f"   {server.description}")
            print(f"   Capabilities: {', '.join(server.capabilities)}")
            print()
    
    def search(self, query: str):
        """Search for servers"""
        results = self.registry.search_servers(query)
        if not results:
            print(f"🔍 No servers found matching '{query}'")
            return
        
        print(f"🔍 Search results for '{query}':")
        print("=" * 50)
        for server in results:
            status = "🟢 DEPLOYED" if server.name.lower().replace(" ", "") in self.current_servers else "⚪ Available"
            print(f"{status} {server.name}: {server.description}")
            print(f"   Capabilities: {', '.join(server.capabilities)}")
            print()
    
    def status(self):
        """Show overall system status"""
        total_available = len(self.registry.servers)
        total_deployed = len(self.current_servers)
        
        print("📊 MCP Server Status Dashboard")
        print("=" * 50)
        print(f"📦 Total Available: {total_available}")
        print(f"🚀 Currently Deployed: {total_deployed}")
        print(f"💰 Estimated Monthly Cost: ${total_deployed * 5}")
        print()
        
        if self.current_servers:
            print("🟢 Active Servers:")
            for name in self.current_servers.keys():
                print(f"   • {name}")

    def config_langgraph(self):
        """Generate LangGraph configuration"""
        if not self.current_servers:
            print("❌ No servers deployed. Deploy some servers first.")
            return
        
        config = self.config_engine.generate_langgraph_config(self.current_servers)
        
        print("🔗 LangGraph MCP Configuration:")
        print("=" * 50)
        print("MCP_SERVERS = {")
        for server_name, url in config.items():
            print(f'    "{server_name}": "{url}",')
        print("}")
        print()
        print("# Use in your LangGraph application:")
        print("from langgraph import MCPClient")
        print("client = MCPClient(servers=MCP_SERVERS)")

def main():
    """Main CLI entry point"""
    manager = MCPManager()
    
    # Handle direct commands for SSH usage
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "add" and len(sys.argv) >= 3:
            server_name = sys.argv[2]
            # Handle "add xyz mcp server" format
            if len(sys.argv) >= 5 and sys.argv[3] == "mcp" and sys.argv[4] == "server":
                server_name = sys.argv[2]
            manager.add_server(server_name)
            
        elif command == "remove" and len(sys.argv) >= 3:
            server_name = sys.argv[2]
            manager.remove_server(server_name)
            
        elif command == "list":
            if len(sys.argv) > 2 and sys.argv[2] == "available":
                manager.list_available()
            else:
                manager.list_deployed()
                
        elif command == "search" and len(sys.argv) >= 3:
            query = " ".join(sys.argv[2:])
            manager.search(query)
            
        elif command == "status":
            manager.status()
            
        elif command == "config" and len(sys.argv) > 2 and sys.argv[2] == "langgraph":
            manager.config_langgraph()
            
        else:
            print("Usage: mcp <command> [args]")
            print("Commands:")
            print("  add <server_name>     - Add/deploy an MCP server")
            print("  remove <server_name>  - Remove an MCP server") 
            print("  list                  - List deployed servers")
            print("  list available        - List all available servers")
            print("  search <query>        - Search for servers")
            print("  status                - Show system status")
            print("  config langgraph      - Generate LangGraph config")
    else:
        # Interactive mode
        manager.status()

if __name__ == "__main__":
    main()
