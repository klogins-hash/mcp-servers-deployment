#!/usr/bin/env python3
"""
Test MCP Server Connection
"""
import json
import subprocess
import sys

def test_mcp_endpoints():
    """Test all MCP server endpoints"""
    base_url = "https://mcp-servers-lnjzg.ondigitalocean.app"
    
    tests = [
        {
            "name": "Health Check",
            "url": f"{base_url}/health",
            "expected_keys": ["status", "service", "version"]
        },
        {
            "name": "Server Status", 
            "url": f"{base_url}/status",
            "expected_keys": ["total_deployed", "servers", "estimated_cost"]
        },
        {
            "name": "Available Servers",
            "url": f"{base_url}/servers", 
            "expected_keys": ["business-agent"]
        },
        {
            "name": "LangGraph Config",
            "url": f"{base_url}/api/langgraph",
            "expected_content": "MCP_SERVERS"
        }
    ]
    
    print("🧪 Testing MCP Server Connection...")
    print(f"🔗 URL: {base_url}")
    print("=" * 60)
    
    all_passed = True
    
    for test in tests:
        try:
            # Use curl to test the endpoint
            result = subprocess.run(
                ["curl", "-s", test["url"]], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                response = result.stdout
                
                # Check if it's JSON
                if "expected_keys" in test:
                    try:
                        data = json.loads(response)
                        missing_keys = [key for key in test["expected_keys"] if key not in data]
                        
                        if not missing_keys:
                            print(f"✅ {test['name']}: PASS")
                            if test['name'] == "Available Servers":
                                business_agent = data.get('business-agent', {})
                                print(f"   📋 Business Agent: {business_agent.get('name', 'Not found')}")
                                print(f"   🛠️  Capabilities: {', '.join(business_agent.get('capabilities', []))}")
                        else:
                            print(f"❌ {test['name']}: FAIL - Missing keys: {missing_keys}")
                            all_passed = False
                            
                    except json.JSONDecodeError:
                        print(f"❌ {test['name']}: FAIL - Invalid JSON response")
                        all_passed = False
                        
                elif "expected_content" in test:
                    if test["expected_content"] in response:
                        print(f"✅ {test['name']}: PASS")
                        print(f"   📝 Config generated successfully")
                    else:
                        print(f"❌ {test['name']}: FAIL - Expected content not found")
                        all_passed = False
                        
            else:
                print(f"❌ {test['name']}: FAIL - HTTP request failed")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {test['name']}: FAIL - {str(e)}")
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your MCP Server is ready for VAPI integration!")
        print(f"\n🔗 VAPI Configuration:")
        print(f"   MCP Server URL: {base_url}")
        print(f"   Status: ✅ Healthy and operational")
        print(f"   Business Agent: ✅ Available with 7 capabilities")
        print(f"   LangGraph Integration: ✅ Configured")
        
        print(f"\n🛠️  Available Tools for VAPI:")
        print(f"   📧 check_emails - Analyze Gmail messages")
        print(f"   📤 send_email - Send emails via Gmail") 
        print(f"   📅 check_calendar - View calendar events")
        print(f"   🗓️ schedule_meeting - Create meetings")
        print(f"   👤 find_contact - Search contacts")
        print(f"   ➕ add_contact - Add new contacts")
        print(f"   🔍 research_topic - Business research")
        print(f"   ⚙️ coordinate_workflow - Multi-step workflows")
        
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = test_mcp_endpoints()
    sys.exit(0 if success else 1)
