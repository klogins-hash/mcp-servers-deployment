#!/usr/bin/env python3
"""
Test script for Business Agent MCP Server
"""
import asyncio
import json
import sys
import os

# Add the custom directory to path
sys.path.append('custom')

async def test_mcp_server():
    """Test the MCP server functionality"""
    print("🧪 Testing Business Agent MCP Server...")
    
    try:
        # Import the MCP server
        from custom.mcp_server_config import server
        
        print("✅ MCP server imported successfully")
        
        # Test listing tools
        print("\n📋 Testing list_tools...")
        tools_result = await server._list_tools_handler()
        print(f"✅ Found {len(tools_result.tools)} tools:")
        for tool in tools_result.tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Test listing resources
        print("\n📦 Testing list_resources...")
        resources_result = await server._list_resources_handler()
        print(f"✅ Found {len(resources_result.resources)} resources:")
        for resource in resources_result.resources:
            print(f"   - {resource.name}: {resource.description}")
        
        # Test listing prompts
        print("\n💬 Testing list_prompts...")
        prompts_result = await server._list_prompts_handler()
        print(f"✅ Found {len(prompts_result.prompts)} prompts:")
        for prompt in prompts_result.prompts:
            print(f"   - {prompt.name}: {prompt.description}")
        
        print("\n🎉 All MCP server tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

async def test_langgraph_connection():
    """Test connection to LangGraph"""
    print("\n🔗 Testing LangGraph connection...")
    
    try:
        import httpx
        
        # Test the LangGraph URL
        langgraph_url = "https://fa6899b6-24c8-425e-ba2a-f6efda16a7da.us.langgraph.app"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try a simple health check or info endpoint
            response = await client.get(f"{langgraph_url}/")
            
            if response.status_code == 200:
                print("✅ LangGraph endpoint is reachable")
                return True
            else:
                print(f"⚠️ LangGraph returned status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error connecting to LangGraph: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting MCP Server Tests...\n")
    
    # Test MCP server functionality
    mcp_test = await test_mcp_server()
    
    # Test LangGraph connection
    langgraph_test = await test_langgraph_connection()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print(f"   MCP Server: {'✅ PASS' if mcp_test else '❌ FAIL'}")
    print(f"   LangGraph:  {'✅ PASS' if langgraph_test else '❌ FAIL'}")
    
    if mcp_test and langgraph_test:
        print("\n🎉 All tests passed! Your MCP server is ready for VAPI integration.")
        print("\n🔗 VAPI Configuration:")
        print("   MCP Server URL: https://mcp-servers-lnjzg.ondigitalocean.app")
        print("   Status: Ready for voice AI integration")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
