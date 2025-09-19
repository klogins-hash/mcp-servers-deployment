#!/usr/bin/env python3
"""
Web Interface for MCP Management - Alternative to SSH
"""
import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
sys.path.append('/app/management')

from server_registry import MCPServerRegistry
from config_templates import ConfigTemplateEngine

class MCPWebHandler(BaseHTTPRequestHandler):
    """Web interface for MCP management"""
    
    def __init__(self, *args, **kwargs):
        self.registry = MCPServerRegistry()
        self.config_engine = ConfigTemplateEngine()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_dashboard()
        elif parsed_path.path == '/health':
            self.send_health()
        elif parsed_path.path == '/status':
            self.send_status()
        elif parsed_path.path == '/servers':
            self.send_servers()
        elif parsed_path.path == '/api/add':
            self.handle_add_server(parsed_path.query)
        elif parsed_path.path == '/api/remove':
            self.handle_remove_server(parsed_path.query)
        else:
            self.send_404()
    
    def send_dashboard(self):
        """Send HTML dashboard"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCPMaster - MCP Server Management</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }
                .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .servers { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
                .server-card { background: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #007acc; }
                .server-card h3 { margin-top: 0; color: #007acc; }
                .btn { background: #007acc; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
                .btn:hover { background: #005a99; }
                .btn-danger { background: #dc3545; }
                .btn-danger:hover { background: #c82333; }
                .commands { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .code { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 MCPMaster - MCP Server Management</h1>
                
                <div class="status">
                    <h2>📊 System Status</h2>
                    <p><strong>Service:</strong> Healthy ✅</p>
                    <p><strong>Deployed Servers:</strong> <span id="server-count">Loading...</span></p>
                    <p><strong>Estimated Cost:</strong> $<span id="cost">Loading...</span>/month</p>
                </div>
                
                <div class="commands">
                    <h2>🎛️ Quick Actions</h2>
                    <button class="btn" onclick="addServer('github')">Add GitHub Server</button>
                    <button class="btn" onclick="addServer('postgres')">Add PostgreSQL Server</button>
                    <button class="btn" onclick="addServer('slack')">Add Slack Server</button>
                    <button class="btn" onclick="addServer('stripe')">Add Stripe Server</button>
                    <button class="btn" onclick="refreshStatus()">Refresh Status</button>
                </div>
                
                <h2>📦 Available MCP Servers</h2>
                <div class="servers" id="servers-grid">
                    Loading servers...
                </div>
                
                <div class="commands">
                    <h2>🔗 LangGraph Integration</h2>
                    <p>Use this configuration in your LangGraph applications:</p>
                    <div class="code" id="langgraph-config">
                        # Configuration will appear here after deploying servers
                    </div>
                </div>
            </div>
            
            <script>
                async function loadStatus() {
                    try {
                        const response = await fetch('/status');
                        const data = await response.json();
                        document.getElementById('server-count').textContent = data.total_deployed;
                        document.getElementById('cost').textContent = data.estimated_cost;
                    } catch (error) {
                        console.error('Error loading status:', error);
                    }
                }
                
                async function loadServers() {
                    try {
                        const response = await fetch('/servers');
                        const servers = await response.json();
                        const grid = document.getElementById('servers-grid');
                        
                        grid.innerHTML = Object.entries(servers).map(([key, server]) => `
                            <div class="server-card">
                                <h3>${server.name}</h3>
                                <p>${server.description}</p>
                                <p><strong>Capabilities:</strong> ${server.capabilities.join(', ')}</p>
                                <button class="btn" onclick="addServer('${key}')">Deploy ${key}</button>
                            </div>
                        `).join('');
                    } catch (error) {
                        console.error('Error loading servers:', error);
                    }
                }
                
                async function addServer(serverName) {
                    try {
                        const response = await fetch(`/api/add?server=${serverName}`);
                        const result = await response.json();
                        alert(result.message);
                        refreshStatus();
                    } catch (error) {
                        alert('Error adding server: ' + error.message);
                    }
                }
                
                function refreshStatus() {
                    loadStatus();
                    loadServers();
                }
                
                // Load initial data
                loadStatus();
                loadServers();
                
                // Refresh every 30 seconds
                setInterval(refreshStatus, 30000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_health(self):
        """Send health check"""
        self.send_json_response({"status": "healthy", "service": "mcp-manager", "version": "1.0.0"})
    
    def send_status(self):
        """Send status"""
        # Load deployed servers (would be from actual storage)
        deployed_servers = {}  # This would load from /app/config/deployed-servers.json
        
        self.send_json_response({
            "total_deployed": len(deployed_servers),
            "servers": list(deployed_servers.keys()),
            "estimated_cost": len(deployed_servers) * 5
        })
    
    def send_servers(self):
        """Send available servers"""
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
        
        # This would integrate with the actual deployment logic
        self.send_json_response({
            "success": True, 
            "message": f"Server {server_name} deployment initiated! (This is a demo - full integration pending)"
        })
    
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
    """Start the web interface"""
    port = int(os.getenv('PORT', 8000))
    
    server = HTTPServer(('0.0.0.0', port), MCPWebHandler)
    print(f"🌐 MCPMaster Web Interface running on port {port}")
    print(f"🔗 Access at: https://mcp-servers-lnjzg.ondigitalocean.app")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down web interface")
        server.shutdown()

if __name__ == "__main__":
    main()
