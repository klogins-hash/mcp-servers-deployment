#!/usr/bin/env python3
"""
Enhanced Web Interface for MCP Management - Full dashboard with one-click deployment
"""
import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add management directory to path
sys.path.append('/app/management')
sys.path.append('management')

try:
    from server_registry import MCPServerRegistry
    from config_templates import ConfigTemplateEngine
except ImportError:
    # Fallback for local testing
    MCPServerRegistry = None
    ConfigTemplateEngine = None

class MCPWebHandler(BaseHTTPRequestHandler):
    """Enhanced web interface for MCP management"""
    
    def __init__(self, *args, **kwargs):
        if MCPServerRegistry:
            self.registry = MCPServerRegistry()
            self.config_engine = ConfigTemplateEngine()
        else:
            self.registry = None
            self.config_engine = None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_dashboard()
        elif parsed_path.path == '/health':
            self.send_health_response()
        elif parsed_path.path == '/status':
            self.send_status_response()
        elif parsed_path.path == '/servers':
            self.send_servers_response()
        elif parsed_path.path == '/api/add':
            self.handle_add_server(parsed_path.query)
        elif parsed_path.path == '/api/remove':
            self.handle_remove_server(parsed_path.query)
        elif parsed_path.path == '/api/langgraph':
            self.send_langgraph_config()
        else:
            self.send_404()
    
    def send_dashboard(self):
        """Send enhanced HTML dashboard"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCPMaster - MCP Server Management Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }
                .container { 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    padding: 20px;
                }
                .header {
                    background: rgba(255,255,255,0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .header h1 { 
                    font-size: 2.5em; 
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 10px;
                }
                .header p { color: #666; font-size: 1.1em; }
                
                .status-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .status-card {
                    background: rgba(255,255,255,0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                }
                .status-card:hover { transform: translateY(-5px); }
                .status-card h3 { color: #667eea; margin-bottom: 10px; }
                .status-card .value { font-size: 2em; font-weight: bold; color: #333; }
                .status-card .label { color: #666; font-size: 0.9em; }
                
                .section {
                    background: rgba(255,255,255,0.95);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                }
                .section h2 { 
                    color: #667eea; 
                    margin-bottom: 20px; 
                    font-size: 1.8em;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .servers-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 20px;
                }
                .server-card {
                    background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
                    border-radius: 15px;
                    padding: 25px;
                    border-left: 5px solid #667eea;
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }
                .server-card:hover { 
                    transform: translateY(-3px);
                    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
                }
                .server-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    right: 0;
                    width: 100px;
                    height: 100px;
                    background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), transparent);
                    border-radius: 0 15px 0 100px;
                }
                .server-card h3 { 
                    color: #667eea; 
                    margin-bottom: 10px;
                    font-size: 1.3em;
                }
                .server-card .description { 
                    color: #666; 
                    margin-bottom: 15px;
                    line-height: 1.5;
                }
                .server-card .capabilities {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-bottom: 20px;
                }
                .capability-tag {
                    background: rgba(102, 126, 234, 0.1);
                    color: #667eea;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.85em;
                    font-weight: 500;
                }
                
                .btn {
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 0.95em;
                }
                .btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }
                .btn:active { transform: translateY(0); }
                .btn-success { background: linear-gradient(45deg, #28a745, #20c997); }
                .btn-danger { background: linear-gradient(45deg, #dc3545, #fd7e14); }
                .btn-small { padding: 8px 16px; font-size: 0.85em; }
                
                .quick-actions {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-bottom: 20px;
                }
                
                .code-block {
                    background: #2d3748;
                    color: #e2e8f0;
                    padding: 20px;
                    border-radius: 10px;
                    font-family: 'Monaco', 'Menlo', monospace;
                    font-size: 0.9em;
                    line-height: 1.5;
                    overflow-x: auto;
                    margin: 15px 0;
                }
                
                .loading {
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #667eea;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 15px 25px;
                    border-radius: 10px;
                    color: white;
                    font-weight: 600;
                    z-index: 1000;
                    transform: translateX(400px);
                    transition: transform 0.3s ease;
                }
                .notification.show { transform: translateX(0); }
                .notification.success { background: linear-gradient(45deg, #28a745, #20c997); }
                .notification.error { background: linear-gradient(45deg, #dc3545, #fd7e14); }
                
                @media (max-width: 768px) {
                    .container { padding: 15px; }
                    .header h1 { font-size: 2em; }
                    .servers-grid { grid-template-columns: 1fr; }
                    .status-grid { grid-template-columns: repeat(2, 1fr); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 MCPMaster</h1>
                    <p>Model Context Protocol Server Management Dashboard</p>
                </div>
                
                <div class="status-grid">
                    <div class="status-card">
                        <h3>📊 System Status</h3>
                        <div class="value" id="system-status">✅</div>
                        <div class="label">Healthy</div>
                    </div>
                    <div class="status-card">
                        <h3>🚀 Deployed Servers</h3>
                        <div class="value" id="server-count"><div class="loading"></div></div>
                        <div class="label">Active Instances</div>
                    </div>
                    <div class="status-card">
                        <h3>💰 Monthly Cost</h3>
                        <div class="value">$<span id="cost"><div class="loading"></div></span></div>
                        <div class="label">Estimated</div>
                    </div>
                    <div class="status-card">
                        <h3>⚡ Quick Deploy</h3>
                        <div class="value">🎯</div>
                        <div class="label">One-Click Ready</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🎛️ Quick Actions</h2>
                    <div class="quick-actions">
                        <button class="btn btn-success" onclick="addServer('github')">🐙 Deploy GitHub</button>
                        <button class="btn btn-success" onclick="addServer('postgres')">🐘 Deploy PostgreSQL</button>
                        <button class="btn btn-success" onclick="addServer('slack')">💬 Deploy Slack</button>
                        <button class="btn btn-success" onclick="addServer('stripe')">💳 Deploy Stripe</button>
                        <button class="btn" onclick="refreshStatus()">🔄 Refresh</button>
                        <button class="btn" onclick="showLangGraphConfig()">🔗 LangGraph Config</button>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📦 Available MCP Servers</h2>
                    <div class="servers-grid" id="servers-grid">
                        <div style="text-align: center; padding: 40px;">
                            <div class="loading"></div>
                            <p style="margin-top: 15px; color: #666;">Loading available servers...</p>
                        </div>
                    </div>
                </div>
                
                <div class="section" id="langgraph-section" style="display: none;">
                    <h2>🔗 LangGraph Integration</h2>
                    <p style="margin-bottom: 15px; color: #666;">Copy this configuration into your LangGraph applications:</p>
                    <div class="code-block" id="langgraph-config">
                        # Deploy some servers first to see the configuration
                    </div>
                </div>
            </div>
            
            <div id="notification" class="notification"></div>
            
            <script>
                let deployedServers = [];
                
                async function loadStatus() {
                    try {
                        const response = await fetch('/status');
                        const data = await response.json();
                        document.getElementById('server-count').textContent = data.total_deployed;
                        document.getElementById('cost').textContent = data.estimated_cost;
                        deployedServers = data.servers;
                        
                        if (data.total_deployed > 0) {
                            document.getElementById('langgraph-section').style.display = 'block';
                            loadLangGraphConfig();
                        }
                    } catch (error) {
                        console.error('Error loading status:', error);
                        showNotification('Error loading status', 'error');
                    }
                }
                
                async function loadServers() {
                    try {
                        const response = await fetch('/servers');
                        const servers = await response.json();
                        const grid = document.getElementById('servers-grid');
                        
                        if (Object.keys(servers).length === 0) {
                            grid.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">No servers available</div>';
                            return;
                        }
                        
                        grid.innerHTML = Object.entries(servers).map(([key, server]) => {
                            const isDeployed = deployedServers.includes(key);
                            const statusBadge = isDeployed ? 
                                '<span style="background: #28a745; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 600;">🟢 DEPLOYED</span>' :
                                '<span style="background: #6c757d; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 600;">⚪ AVAILABLE</span>';
                            
                            return `
                                <div class="server-card">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                                        <h3>${server.name}</h3>
                                        ${statusBadge}
                                    </div>
                                    <div class="description">${server.description}</div>
                                    <div class="capabilities">
                                        ${server.capabilities.map(cap => `<span class="capability-tag">${cap}</span>`).join('')}
                                    </div>
                                    <div style="display: flex; gap: 10px;">
                                        ${!isDeployed ? 
                                            `<button class="btn btn-success btn-small" onclick="addServer('${key}')">🚀 Deploy ${key}</button>` :
                                            `<button class="btn btn-danger btn-small" onclick="removeServer('${key}')">🗑️ Remove</button>`
                                        }
                                        <button class="btn btn-small" onclick="showServerDetails('${key}')">ℹ️ Details</button>
                                    </div>
                                </div>
                            `;
                        }).join('');
                    } catch (error) {
                        console.error('Error loading servers:', error);
                        showNotification('Error loading servers', 'error');
                    }
                }
                
                async function addServer(serverName) {
                    showNotification(`Deploying ${serverName}...`, 'success');
                    
                    try {
                        const response = await fetch(`/api/add?server=${serverName}`);
                        const result = await response.json();
                        
                        if (result.success) {
                            showNotification(`✅ ${serverName} deployment initiated!`, 'success');
                        } else {
                            showNotification(`❌ ${result.message}`, 'error');
                        }
                        
                        setTimeout(refreshStatus, 2000);
                    } catch (error) {
                        showNotification(`❌ Error deploying ${serverName}: ${error.message}`, 'error');
                    }
                }
                
                async function removeServer(serverName) {
                    if (!confirm(`Are you sure you want to remove ${serverName}?`)) return;
                    
                    showNotification(`Removing ${serverName}...`, 'success');
                    
                    try {
                        const response = await fetch(`/api/remove?server=${serverName}`);
                        const result = await response.json();
                        
                        if (result.success) {
                            showNotification(`✅ ${serverName} removed successfully!`, 'success');
                        } else {
                            showNotification(`❌ ${result.message}`, 'error');
                        }
                        
                        setTimeout(refreshStatus, 2000);
                    } catch (error) {
                        showNotification(`❌ Error removing ${serverName}: ${error.message}`, 'error');
                    }
                }
                
                async function loadLangGraphConfig() {
                    try {
                        const response = await fetch('/api/langgraph');
                        const config = await response.text();
                        document.getElementById('langgraph-config').textContent = config;
                    } catch (error) {
                        console.error('Error loading LangGraph config:', error);
                    }
                }
                
                function showLangGraphConfig() {
                    document.getElementById('langgraph-section').style.display = 'block';
                    document.getElementById('langgraph-section').scrollIntoView({ behavior: 'smooth' });
                    loadLangGraphConfig();
                }
                
                function showServerDetails(serverName) {
                    showNotification(`Server: ${serverName} - Check console for details`, 'success');
                    console.log(`Server details for: ${serverName}`);
                }
                
                function refreshStatus() {
                    loadStatus();
                    loadServers();
                    showNotification('Status refreshed!', 'success');
                }
                
                function showNotification(message, type = 'success') {
                    const notification = document.getElementById('notification');
                    notification.textContent = message;
                    notification.className = `notification ${type}`;
                    notification.classList.add('show');
                    
                    setTimeout(() => {
                        notification.classList.remove('show');
                    }, 3000);
                }
                
                // Initialize dashboard
                loadStatus();
                loadServers();
                
                // Auto-refresh every 30 seconds
                setInterval(() => {
                    loadStatus();
                    loadServers();
                }, 30000);
                
                // Welcome message
                setTimeout(() => {
                    showNotification('🚀 MCPMaster Dashboard Ready!', 'success');
                }, 1000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_health_response(self):
        """Send health check response"""
        response = {
            "status": "healthy",
            "service": "mcp-manager",
            "version": "1.0.0"
        }
        self.send_json_response(response)
    
    def send_status_response(self):
        """Send system status response"""
        try:
            with open('/app/config/deployed-servers.json', 'r') as f:
                deployed_servers = json.load(f)
        except FileNotFoundError:
            deployed_servers = {}
        
        response = {
            "total_deployed": len(deployed_servers),
            "servers": list(deployed_servers.keys()),
            "estimated_cost": len(deployed_servers) * 5
        }
        self.send_json_response(response)
    
    def send_servers_response(self):
        """Send list of available servers"""
        if not self.registry:
            self.send_json_response({"error": "Server registry not available"})
            return
        
        servers = {}
        for name, server in self.registry.servers.items():
            servers[name] = {
                "name": server.name,
                "description": server.description,
                "capabilities": server.capabilities,
                "official": server.official
            }
        
        self.send_json_response(servers)
    
    def handle_add_server(self, query):
        """Handle add server request"""
        params = parse_qs(query)
        server_name = params.get('server', [''])[0]
        
        if not server_name:
            self.send_json_response({"success": False, "message": "Server name required"})
            return
        
        if not self.registry:
            self.send_json_response({"success": False, "message": "Server registry not available"})
            return
        
        # Check if server exists
        server_info = self.registry.get_server(server_name)
        if not server_info:
            self.send_json_response({
                "success": False, 
                "message": f"Server '{server_name}' not found in registry"
            })
            return
        
        # For now, simulate deployment (full integration would connect to deployment engine)
        try:
            # Load current deployed servers
            try:
                with open('/app/config/deployed-servers.json', 'r') as f:
                    deployed_servers = json.load(f)
            except FileNotFoundError:
                deployed_servers = {}
            
            # Check if already deployed
            if server_name in deployed_servers:
                self.send_json_response({
                    "success": False,
                    "message": f"Server '{server_name}' is already deployed"
                })
                return
            
            # Add to deployed servers (simulation)
            deployed_servers[server_name] = {
                "name": server_info.name,
                "status": "active",
                "deployed_at": "2025-09-19",
                "url": f"https://mcp-{server_name}-xyz.ondigitalocean.app"
            }
            
            # Save deployed servers
            os.makedirs('/app/config', exist_ok=True)
            with open('/app/config/deployed-servers.json', 'w') as f:
                json.dump(deployed_servers, f, indent=2)
            
            self.send_json_response({
                "success": True,
                "message": f"Server '{server_name}' deployment initiated successfully! (Demo mode - full deployment integration pending)"
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Error deploying server: {str(e)}"
            })
    
    def handle_remove_server(self, query):
        """Handle remove server request"""
        params = parse_qs(query)
        server_name = params.get('server', [''])[0]
        
        if not server_name:
            self.send_json_response({"success": False, "message": "Server name required"})
            return
        
        try:
            # Load current deployed servers
            try:
                with open('/app/config/deployed-servers.json', 'r') as f:
                    deployed_servers = json.load(f)
            except FileNotFoundError:
                deployed_servers = {}
            
            # Check if server is deployed
            if server_name not in deployed_servers:
                self.send_json_response({
                    "success": False,
                    "message": f"Server '{server_name}' is not currently deployed"
                })
                return
            
            # Remove from deployed servers
            del deployed_servers[server_name]
            
            # Save updated deployed servers
            os.makedirs('/app/config', exist_ok=True)
            with open('/app/config/deployed-servers.json', 'w') as f:
                json.dump(deployed_servers, f, indent=2)
            
            self.send_json_response({
                "success": True,
                "message": f"Server '{server_name}' removed successfully! (Demo mode)"
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Error removing server: {str(e)}"
            })
    
    def send_langgraph_config(self):
        """Send LangGraph configuration"""
        try:
            with open('/app/config/deployed-servers.json', 'r') as f:
                deployed_servers = json.load(f)
        except FileNotFoundError:
            deployed_servers = {}
        
        if not deployed_servers:
            config = "# No servers deployed yet. Deploy some servers first to see the configuration."
        else:
            config_lines = ["# Auto-generated LangGraph MCP configuration", "MCP_SERVERS = {"]
            for server_name, details in deployed_servers.items():
                url = details.get('url', f"https://mcp-{server_name}-xyz.ondigitalocean.app")
                config_lines.append(f'    "{server_name}": "{url}",')
            config_lines.extend(["}", "", "# Use in your LangGraph application:", "from langgraph import MCPClient", "client = MCPClient(servers=MCP_SERVERS)"])
            config = "\n".join(config_lines)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(config.encode())
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_404(self):
        """Send 404 response"""
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        return

def main():
    """Start the enhanced MCP web interface"""
    port = int(os.getenv('PORT', 8000))
    
    server = HTTPServer(('0.0.0.0', port), MCPWebHandler)
    print(f"🚀 MCPMaster Web Interface running on port {port}")
    print(f"🌐 Dashboard: https://mcp-servers-lnjzg.ondigitalocean.app")
    print(f"📊 Endpoints: /, /health, /status, /servers, /api/add, /api/remove, /api/langgraph")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down MCPMaster web interface")
        server.shutdown()

if __name__ == "__main__":
    main()
