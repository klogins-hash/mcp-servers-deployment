"""
Deployment Engine - Handles automatic deployment to DigitalOcean App Platform
"""
import os
import json
import subprocess
import requests
from typing import Dict, Any

class DeploymentEngine:
    """Handles MCP server deployments"""
    
    def __init__(self):
        self.do_token = os.getenv('DIGITALOCEAN_TOKEN')
        self.app_id = os.getenv('DIGITALOCEAN_APP_ID')
        self.github_repo = os.getenv('GITHUB_REPO', 'your-username/mcp-servers-deployment')
    
    def deploy_server(self, server_name: str, config: Dict[str, Any]) -> bool:
        """Deploy a new MCP server to App Platform"""
        try:
            # Update app.yaml with new service
            self._update_app_config(server_name, config)
            
            # Commit and push changes
            self._commit_and_push(f"Add {server_name} MCP server")
            
            # DigitalOcean will auto-deploy from GitHub
            print(f"📡 Triggering deployment via GitHub integration...")
            
            # Wait for deployment (in real implementation, check DO API)
            print(f"⏳ Waiting for deployment to complete...")
            
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            return False
    
    def remove_server(self, server_name: str) -> bool:
        """Remove an MCP server from App Platform"""
        try:
            # Remove service from app.yaml
            self._remove_from_app_config(server_name)
            
            # Commit and push changes
            self._commit_and_push(f"Remove {server_name} MCP server")
            
            print(f"📡 Triggering removal via GitHub integration...")
            return True
            
        except Exception as e:
            print(f"❌ Removal failed: {str(e)}")
            return False
    
    def _update_app_config(self, server_name: str, config: Dict[str, Any]):
        """Update app.yaml with new service"""
        app_yaml_path = '/app/app.yaml'
        
        # Load current app.yaml
        with open(app_yaml_path, 'r') as f:
            content = f.read()
        
        # Add new service configuration
        service_config = self._generate_service_yaml(server_name, config)
        
        # Insert before the end of services section
        if 'services:' in content:
            services_end = content.find('\n\n', content.find('services:'))
            if services_end == -1:
                content += f"\n{service_config}"
            else:
                content = content[:services_end] + f"\n{service_config}" + content[services_end:]
        
        # Write updated config
        with open(app_yaml_path, 'w') as f:
            f.write(content)
    
    def _generate_service_yaml(self, server_name: str, config: Dict[str, Any]) -> str:
        """Generate YAML configuration for a service"""
        env_vars = ""
        for key, value in config.get('env_vars', {}).items():
            env_vars += f"""
      - key: {key}
        value: "{value}" """
        
        return f"""
  # {config['name']} Server
  - name: mcp-{server_name}
    source_dir: /
    run_command: {config['uvx_command']} --host 0.0.0.0 --port {config['port']}
    http_port: {config['port']}
    instance_count: 1
    instance_size_slug: basic-xxs
    health_check:
      http_path: /health
    envs:{env_vars}
      - key: MCP_SERVER_TYPE
        value: {server_name}"""
    
    def _remove_from_app_config(self, server_name: str):
        """Remove service from app.yaml"""
        app_yaml_path = '/app/app.yaml'
        
        with open(app_yaml_path, 'r') as f:
            lines = f.readlines()
        
        # Find and remove the service section
        new_lines = []
        skip_until_next_service = False
        
        for line in lines:
            if f"name: mcp-{server_name}" in line:
                skip_until_next_service = True
                continue
            elif skip_until_next_service and line.strip().startswith('- name:'):
                skip_until_next_service = False
                new_lines.append(line)
            elif not skip_until_next_service:
                new_lines.append(line)
        
        with open(app_yaml_path, 'w') as f:
            f.writelines(new_lines)
    
    def _commit_and_push(self, commit_message: str):
        """Commit changes and push to GitHub"""
        try:
            subprocess.run(['git', 'add', '.'], cwd='/app', check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], cwd='/app', check=True)
            subprocess.run(['git', 'push'], cwd='/app', check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git operation failed: {e}")
