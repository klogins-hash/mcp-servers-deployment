"""
Configuration Template Engine - Generates configs for MCP servers
"""
from typing import Dict, Any
from server_registry import MCPServerInfo

class ConfigTemplateEngine:
    """Generates configuration templates for MCP servers"""
    
    def generate_server_config(self, server_info: MCPServerInfo, env_vars: Dict[str, str]) -> Dict[str, Any]:
        """Generate complete configuration for a server"""
        return {
            "name": server_info.name,
            "description": server_info.description,
            "uvx_command": server_info.uvx_command,
            "port": server_info.default_port,
            "env_vars": self._merge_env_vars(server_info.env_vars, env_vars),
            "capabilities": server_info.capabilities,
            "health_check": "/health",
            "official": server_info.official
        }
    
    def _merge_env_vars(self, default_vars: Dict[str, str], custom_vars: Dict[str, str]) -> Dict[str, str]:
        """Merge default and custom environment variables"""
        merged = default_vars.copy()
        merged.update(custom_vars)
        return merged
    
    def generate_langgraph_config(self, deployed_servers: Dict[str, Any]) -> Dict[str, str]:
        """Generate LangGraph configuration for deployed servers"""
        config = {}
        for server_name, details in deployed_servers.items():
            port = details['info']['default_port']
            config[server_name] = f"https://mcp-{server_name}-xyz.ondigitalocean.app"
        return config
