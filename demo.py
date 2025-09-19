#!/usr/bin/env python3
"""
Demo script showing MCP Manager functionality
"""
import sys
import os
sys.path.append('management')

from server_registry import MCPServerRegistry
from config_templates import ConfigTemplateEngine

def demo_server_registry():
    """Demonstrate server registry functionality"""
    print("🎭 MCP Server Registry Demo")
    print("=" * 50)
    
    registry = MCPServerRegistry()
    
    print(f"📦 Total servers available: {len(registry.servers)}")
    print(f"🔍 Server names: {', '.join(registry.list_servers())}")
    print()
    
    # Demo search
    print("🔍 Searching for 'git':")
    results = registry.search_servers('git')
    for server in results:
        print(f"  • {server.name}: {server.description}")
    print()
    
    # Demo get server
    print("📋 GitHub server details:")
    github_server = registry.get_server('github')
    if github_server:
        print(f"  Name: {github_server.name}")
        print(f"  Package: {github_server.package_name}")
        print(f"  Port: {github_server.default_port}")
        print(f"  Capabilities: {', '.join(github_server.capabilities)}")
    print()

def demo_config_generation():
    """Demonstrate configuration generation"""
    print("⚙️  Configuration Generation Demo")
    print("=" * 50)
    
    registry = MCPServerRegistry()
    config_engine = ConfigTemplateEngine()
    
    # Get a server and generate config
    server_info = registry.get_server('github')
    custom_env = {"GITHUB_TOKEN": "ghp_example_token"}
    
    config = config_engine.generate_server_config(server_info, custom_env)
    
    print("📋 Generated configuration for GitHub server:")
    for key, value in config.items():
        if key == 'env_vars':
            print(f"  {key}:")
            for env_key, env_value in value.items():
                print(f"    {env_key}: {env_value}")
        else:
            print(f"  {key}: {value}")
    print()

def demo_langgraph_config():
    """Demonstrate LangGraph configuration generation"""
    print("🔗 LangGraph Configuration Demo")
    print("=" * 50)
    
    # Simulate deployed servers
    deployed_servers = {
        "github": {
            "info": {"default_port": 8085},
            "status": "active"
        },
        "postgres": {
            "info": {"default_port": 8084},
            "status": "active"
        },
        "slack": {
            "info": {"default_port": 8086},
            "status": "active"
        }
    }
    
    config_engine = ConfigTemplateEngine()
    langgraph_config = config_engine.generate_langgraph_config(deployed_servers)
    
    print("🐍 Generated LangGraph configuration:")
    print("MCP_SERVERS = {")
    for server_name, url in langgraph_config.items():
        print(f'    "{server_name}": "{url}",')
    print("}")
    print()
    print("# Use in your LangGraph application:")
    print("from langgraph import MCPClient")
    print("client = MCPClient(servers=MCP_SERVERS)")
    print()

def main():
    """Run all demos"""
    print("🎪 MCP Servers Deployment System Demo")
    print("=" * 60)
    print()
    
    demo_server_registry()
    demo_config_generation()
    demo_langgraph_config()
    
    print("🎉 Demo completed!")
    print("💡 Try running: python3 management/mcp_manager.py status")

if __name__ == "__main__":
    main()
