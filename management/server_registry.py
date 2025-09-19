"""
MCP Server Registry - Official catalog of available MCP servers
"""
import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MCPServerInfo:
    name: str
    package_name: str
    description: str
    official: bool
    docker_image: Optional[str]
    uvx_command: str
    default_port: int
    env_vars: Dict[str, str]
    capabilities: List[str]
    github_repo: Optional[str]

class MCPServerRegistry:
    """Registry of available MCP servers"""
    
    def __init__(self):
        self.servers = self._load_official_servers()
    
    def _load_official_servers(self) -> Dict[str, MCPServerInfo]:
        """Load official MCP servers catalog"""
        return {
            "fetch": MCPServerInfo(
                name="Web Content Fetch",
                package_name="mcp-server-fetch",
                description="Fetches and converts web content to markdown",
                official=True,
                docker_image="mcp/fetch",
                uvx_command="uvx mcp-server-fetch",
                default_port=8080,
                env_vars={
                    "ROBOTS_TXT_RESPECT": "true",
                    "USER_AGENT": "MCP-Fetch-Bot/1.0"
                },
                capabilities=["web_fetch", "html_to_markdown"],
                github_repo="modelcontextprotocol/servers"
            ),
            "git": MCPServerInfo(
                name="Git Repository Operations",
                package_name="mcp-server-git", 
                description="Git repository operations and management",
                official=True,
                docker_image="mcp/git",
                uvx_command="uvx mcp-server-git",
                default_port=8081,
                env_vars={
                    "DEFAULT_REPO_PATH": "/tmp/repos",
                    "MAX_REPO_SIZE": "100MB"
                },
                capabilities=["git_read", "git_search", "git_manipulate"],
                github_repo="modelcontextprotocol/servers"
            ),
            "filesystem": MCPServerInfo(
                name="Filesystem Operations",
                package_name="mcp-server-filesystem",
                description="Secure file and directory operations",
                official=True,
                docker_image="mcp/filesystem", 
                uvx_command="uvx mcp-server-filesystem",
                default_port=8082,
                env_vars={
                    "ALLOWED_DIRECTORIES": "/tmp,/workspace",
                    "MAX_FILE_SIZE": "10MB"
                },
                capabilities=["file_read", "file_write", "directory_ops"],
                github_repo="modelcontextprotocol/servers"
            ),
            "memory": MCPServerInfo(
                name="Knowledge Graph Memory",
                package_name="mcp-server-memory",
                description="Persistent memory using knowledge graphs", 
                official=True,
                docker_image="mcp/memory",
                uvx_command="uvx mcp-server-memory",
                default_port=8083,
                env_vars={
                    "MEMORY_BACKEND": "sqlite",
                    "MEMORY_DB_PATH": "/tmp/memory.db"
                },
                capabilities=["memory_store", "memory_retrieve", "graph_ops"],
                github_repo="modelcontextprotocol/servers"
            ),
            "postgres": MCPServerInfo(
                name="PostgreSQL Database",
                package_name="mcp-server-postgres",
                description="PostgreSQL database operations",
                official=True,
                docker_image="mcp/postgres",
                uvx_command="uvx mcp-server-postgres",
                default_port=8084,
                env_vars={
                    "POSTGRES_URL": "postgresql://user:pass@localhost:5432/db",
                    "READ_ONLY": "false"
                },
                capabilities=["db_read", "db_write", "schema_inspect"],
                github_repo="modelcontextprotocol/servers"
            ),
            "github": MCPServerInfo(
                name="GitHub Integration",
                package_name="mcp-server-github",
                description="GitHub repositories, issues, and PRs",
                official=True,
                docker_image="mcp/github",
                uvx_command="uvx mcp-server-github",
                default_port=8085,
                env_vars={
                    "GITHUB_TOKEN": "",
                    "DEFAULT_ORG": ""
                },
                capabilities=["github_repos", "github_issues", "github_prs"],
                github_repo="modelcontextprotocol/servers"
            ),
            "slack": MCPServerInfo(
                name="Slack Integration",
                package_name="mcp-server-slack", 
                description="Slack workspace and channel management",
                official=True,
                docker_image="mcp/slack",
                uvx_command="uvx mcp-server-slack",
                default_port=8086,
                env_vars={
                    "SLACK_TOKEN": "",
                    "SLACK_SIGNING_SECRET": ""
                },
                capabilities=["slack_channels", "slack_messages", "slack_users"],
                github_repo="modelcontextprotocol/servers"
            ),
            "stripe": MCPServerInfo(
                name="Stripe Payments",
                package_name="mcp-server-stripe",
                description="Stripe payment processing and management",
                official=True,
                docker_image="mcp/stripe",
                uvx_command="uvx mcp-server-stripe", 
                default_port=8087,
                env_vars={
                    "STRIPE_SECRET_KEY": "",
                    "STRIPE_WEBHOOK_SECRET": ""
                },
                capabilities=["payments", "customers", "subscriptions"],
                github_repo="modelcontextprotocol/servers"
            )
        }
    
    def get_server(self, name: str) -> Optional[MCPServerInfo]:
        """Get server info by name"""
        return self.servers.get(name.lower())
    
    def list_servers(self) -> List[str]:
        """List all available servers"""
        return list(self.servers.keys())
    
    def search_servers(self, query: str) -> List[MCPServerInfo]:
        """Search servers by name or capability"""
        results = []
        query = query.lower()
        for server in self.servers.values():
            if (query in server.name.lower() or 
                query in server.description.lower() or
                any(query in cap.lower() for cap in server.capabilities)):
                results.append(server)
        return results

    def add_community_server(self, name: str, package_name: str, description: str, 
                           capabilities: List[str], port: int = None) -> bool:
        """Add a community MCP server to registry"""
        if port is None:
            port = 8088 + len([s for s in self.servers.values() if not s.official])
        
        self.servers[name] = MCPServerInfo(
            name=name,
            package_name=package_name,
            description=description,
            official=False,
            docker_image=None,
            uvx_command=f"uvx {package_name}",
            default_port=port,
            env_vars={},
            capabilities=capabilities,
            github_repo=None
        )
        return True
