#!/usr/bin/env python3
"""
Local test of email functionality via direct LangGraph call
"""
import asyncio
import json

async def test_email_summary():
    """Test email summary by calling LangGraph directly"""
    
    print("📧 Testing Email Summary via LangGraph...")
    print("🔗 Connecting to your LangGraph deployment...")
    
    try:
        import httpx
        
        # Your LangGraph configuration
        langgraph_url = "https://fa6899b6-24c8-425e-ba2a-f6efda16a7da.us.langgraph.app"
        rube_session = "G65-NEHYF"
        
        # Prepare the request
        payload = {
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Check my most recent email and provide a summary of it"
                    }
                ]
            },
            "config": {
                "session_id": rube_session,
                "configurable": {
                    "thread_id": f"test-email-summary-{hash('recent_email')}"
                }
            }
        }
        
        print("📤 Sending request to LangGraph...")
        print(f"   URL: {langgraph_url}/invoke")
        print(f"   Session: {rube_session}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{langgraph_url}/invoke",
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            
            print(f"📥 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the response
                if "output" in result and "messages" in result["output"]:
                    messages = result["output"]["messages"]
                    if messages:
                        final_message = messages[-1]
                        content = final_message.get("content", "No content")
                        
                        print("\n" + "="*60)
                        print("📧 EMAIL SUMMARY RESULT:")
                        print("="*60)
                        print(content)
                        print("="*60)
                        
                        return True
                else:
                    print("⚠️ Unexpected response format")
                    print(json.dumps(result, indent=2))
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"Response: {response.text}")
                
    except ImportError:
        print("❌ httpx not available. Install with: pip3 install httpx")
        print("\n💡 Alternative: Test via VAPI instead")
        print("   1. Add MCP URL to VAPI: https://mcp-servers-lnjzg.ondigitalocean.app")
        print("   2. Say: 'Check my most recent email and summarize it'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    return False

if __name__ == "__main__":
    asyncio.run(test_email_summary())
