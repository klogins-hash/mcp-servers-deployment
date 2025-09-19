#!/usr/bin/env python3
"""
Health Check Service - Provides health endpoints for DigitalOcean App Platform
"""
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks and basic management API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/health':
            self.send_health_response()
        elif parsed_path.path == '/status':
            self.send_status_response()
        elif parsed_path.path == '/servers':
            self.send_servers_response()
        else:
            self.send_404()
    
    def send_health_response(self):
        """Send health check response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "service": "mcp-manager",
            "version": "1.0.0"
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def send_status_response(self):
        """Send system status response"""
        try:
            with open('/app/config/deployed-servers.json', 'r') as f:
                deployed_servers = json.load(f)
        except FileNotFoundError:
            deployed_servers = {}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "total_deployed": len(deployed_servers),
            "servers": list(deployed_servers.keys()),
            "estimated_cost": len(deployed_servers) * 5
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def send_servers_response(self):
        """Send list of available servers"""
        # Import here to avoid issues during startup
        import sys
        sys.path.append('/app/management')
        from server_registry import MCPServerRegistry
        
        registry = MCPServerRegistry()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        servers = {}
        for name, server in registry.servers.items():
            servers[name] = {
                "name": server.name,
                "description": server.description,
                "capabilities": server.capabilities,
                "official": server.official
            }
        
        self.wfile.write(json.dumps(servers).encode())
    
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
    """Start the health check server"""
    port = int(os.getenv('PORT', 8000))
    
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"🏥 Health check server running on port {port}")
    print(f"📊 Endpoints: /health, /status, /servers")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down health check server")
        server.shutdown()

if __name__ == "__main__":
    main()
