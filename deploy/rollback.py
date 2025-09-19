#!/usr/bin/env python3
"""
Rollback functionality for MCP server deployments
"""
import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List

class RollbackManager:
    """Manages rollback operations for MCP deployments"""
    
    def __init__(self):
        self.backup_dir = '/app/backups'
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, description: str = None) -> str:
        """Create a backup of current deployment state"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_id = f"backup_{timestamp}"
        
        backup_data = {
            "id": backup_id,
            "timestamp": timestamp,
            "description": description or "Automatic backup",
            "app_yaml": self._read_app_yaml(),
            "deployed_servers": self._read_deployed_servers()
        }
        
        backup_file = os.path.join(self.backup_dir, f"{backup_id}.json")
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✅ Backup created: {backup_id}")
        return backup_id
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.json'):
                backup_file = os.path.join(self.backup_dir, filename)
                try:
                    with open(backup_file, 'r') as f:
                        backup_data = json.load(f)
                        backups.append({
                            "id": backup_data["id"],
                            "timestamp": backup_data["timestamp"], 
                            "description": backup_data["description"]
                        })
                except Exception as e:
                    print(f"⚠️  Error reading backup {filename}: {e}")
        
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
    
    def rollback_to_backup(self, backup_id: str) -> bool:
        """Rollback to a specific backup"""
        backup_file = os.path.join(self.backup_dir, f"{backup_id}.json")
        
        if not os.path.exists(backup_file):
            print(f"❌ Backup {backup_id} not found")
            return False
        
        try:
            # Create backup of current state first
            current_backup = self.create_backup("Pre-rollback backup")
            
            # Load backup data
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            # Restore app.yaml
            with open('/app/app.yaml', 'w') as f:
                f.write(backup_data["app_yaml"])
            
            # Restore deployed servers
            os.makedirs('/app/config', exist_ok=True)
            with open('/app/config/deployed-servers.json', 'w') as f:
                json.dump(backup_data["deployed_servers"], f, indent=2)
            
            # Commit and push changes
            self._commit_and_push(f"Rollback to {backup_id}")
            
            print(f"✅ Successfully rolled back to {backup_id}")
            print(f"💾 Current state backed up as: {current_backup}")
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False
    
    def _read_app_yaml(self) -> str:
        """Read current app.yaml content"""
        try:
            with open('/app/app.yaml', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def _read_deployed_servers(self) -> Dict:
        """Read current deployed servers"""
        try:
            with open('/app/config/deployed-servers.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _commit_and_push(self, message: str):
        """Commit and push changes to GitHub"""
        subprocess.run(['git', 'add', '.'], cwd='/app', check=True)
        subprocess.run(['git', 'commit', '-m', message], cwd='/app', check=True)
        subprocess.run(['git', 'push'], cwd='/app', check=True)

def main():
    """Main rollback CLI"""
    import sys
    
    manager = RollbackManager()
    
    if len(sys.argv) < 2:
        print("Usage: python rollback.py <command> [args]")
        print("Commands:")
        print("  backup [description]  - Create a backup")
        print("  list                  - List all backups")
        print("  rollback <backup_id>  - Rollback to a backup")
        return
    
    command = sys.argv[1]
    
    if command == "backup":
        description = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        backup_id = manager.create_backup(description)
        print(f"Backup ID: {backup_id}")
        
    elif command == "list":
        backups = manager.list_backups()
        if not backups:
            print("📭 No backups found")
        else:
            print("📋 Available Backups:")
            print("=" * 50)
            for backup in backups:
                print(f"ID: {backup['id']}")
                print(f"Time: {backup['timestamp']}")
                print(f"Description: {backup['description']}")
                print()
                
    elif command == "rollback" and len(sys.argv) > 2:
        backup_id = sys.argv[2]
        manager.rollback_to_backup(backup_id)
        
    else:
        print("❌ Invalid command or missing arguments")

if __name__ == "__main__":
    main()
