#!/usr/bin/env python3
"""
MCP Server wrapper for LangGraph Business Agent
Exposes the business agent as a proper MCP server for VAPI integration
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server.models import (
    GetPromptResult,
    ListPromptsResult,
    ListResourcesResult,
    ListToolsResult,
    CallToolResult,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("business-agent-mcp")

# Initialize MCP Server
server = Server("business-agent-mcp")

# Your LangGraph deployment URL
LANGGRAPH_URL = "https://fa6899b6-24c8-425e-ba2a-f6efda16a7da.us.langgraph.app"

# Rube MCP session details
RUBE_SESSION_ID = "G65-NEHYF"
RUBE_API_KEY = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJ1c2VyXzAxSzRRSDI5R1pWQURROU1IQVhWWFdZUjZLIiwib3JnSWQiOiJvcmdfMDFLNFFIMlBIUzI2RzJBVkRWRkZNUE0zNjkiLCJpYXQiOjE3NTc0Mzg4MDB9.hYQ-8BeA54VAZ9Z1zNolvJZ8U-VHLNlkq9tZxY_PE2o"

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available business tools"""
    return ListToolsResult(
        tools=[
            types.Tool(
                name="check_emails",
                description="Check and analyze recent emails from Gmail",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Email search query or filter (optional)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of emails to retrieve (default: 10)",
                            "default": 10
                        }
                    }
                }
            ),
            types.Tool(
                name="send_email",
                description="Draft and send an email via Gmail",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address or contact name"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject line"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email content/message"
                        },
                        "cc": {
                            "type": "string",
                            "description": "CC recipients (optional)"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            ),
            types.Tool(
                name="check_calendar",
                description="Check calendar events and availability",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "date_range": {
                            "type": "string",
                            "description": "Date range to check (e.g., 'today', 'this week', 'next week')"
                        },
                        "calendar": {
                            "type": "string",
                            "description": "Specific calendar to check (optional)"
                        }
                    }
                }
            ),
            types.Tool(
                name="schedule_meeting",
                description="Schedule a new meeting or appointment",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Meeting title/subject"
                        },
                        "attendees": {
                            "type": "string",
                            "description": "Meeting attendees (email addresses or names)"
                        },
                        "date_time": {
                            "type": "string",
                            "description": "Preferred date and time for the meeting"
                        },
                        "duration": {
                            "type": "string",
                            "description": "Meeting duration (e.g., '1 hour', '30 minutes')"
                        },
                        "description": {
                            "type": "string",
                            "description": "Meeting description or agenda (optional)"
                        }
                    },
                    "required": ["title", "attendees", "date_time"]
                }
            ),
            types.Tool(
                name="find_contact",
                description="Search for contact information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Contact name to search for"
                        },
                        "company": {
                            "type": "string",
                            "description": "Company name (optional)"
                        }
                    },
                    "required": ["name"]
                }
            ),
            types.Tool(
                name="add_contact",
                description="Add a new contact to Google Contacts",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Contact full name"
                        },
                        "email": {
                            "type": "string",
                            "description": "Contact email address"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Contact phone number (optional)"
                        },
                        "company": {
                            "type": "string",
                            "description": "Company name (optional)"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Additional notes (optional)"
                        }
                    },
                    "required": ["name", "email"]
                }
            ),
            types.Tool(
                name="research_topic",
                description="Research business topics and trends",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Research topic or question"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context or specific focus (optional)"
                        }
                    },
                    "required": ["topic"]
                }
            ),
            types.Tool(
                name="coordinate_workflow",
                description="Coordinate complex multi-step business workflows",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_type": {
                            "type": "string",
                            "description": "Type of workflow (e.g., 'product_launch', 'client_onboarding', 'strategic_planning')"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the workflow requirements"
                        },
                        "stakeholders": {
                            "type": "string",
                            "description": "Key stakeholders involved (optional)"
                        },
                        "timeline": {
                            "type": "string",
                            "description": "Timeline or deadline requirements (optional)"
                        }
                    },
                    "required": ["workflow_type", "description"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Execute business tools via LangGraph agent"""
    try:
        # Import required modules for HTTP requests
        import httpx
        
        # Prepare the request to LangGraph agent
        payload = {
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Execute {name} with parameters: {json.dumps(arguments)}"
                    }
                ]
            },
            "config": {
                "session_id": RUBE_SESSION_ID,
                "configurable": {
                    "thread_id": f"vapi-{name}-{hash(str(arguments))}"
                }
            }
        }
        
        # Call LangGraph deployment
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{LANGGRAPH_URL}/invoke",
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the final message from LangGraph response
                if "output" in result and "messages" in result["output"]:
                    messages = result["output"]["messages"]
                    if messages:
                        final_message = messages[-1]
                        content = final_message.get("content", "Task completed successfully")
                        
                        return CallToolResult(
                            content=[
                                types.TextContent(
                                    type="text",
                                    text=content
                                )
                            ]
                        )
                
                # Fallback response
                return CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Tool {name} executed successfully"
                        )
                    ]
                )
            else:
                logger.error(f"LangGraph request failed: {response.status_code} - {response.text}")
                return CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Error executing {name}: Service temporarily unavailable"
                        )
                    ],
                    isError=True
                )
                
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )
            ],
            isError=True
        )

@server.list_resources()
async def handle_list_resources() -> ListResourcesResult:
    """List available resources"""
    return ListResourcesResult(
        resources=[
            types.Resource(
                uri="business://gmail",
                name="Gmail Integration",
                description="Access to Gmail account dp@thekollektiv.xyz",
                mimeType="application/json"
            ),
            types.Resource(
                uri="business://calendar",
                name="Google Calendar",
                description="Access to multiple Google Calendars",
                mimeType="application/json"
            ),
            types.Resource(
                uri="business://contacts",
                name="Google Contacts",
                description="Contact management and relationship intelligence",
                mimeType="application/json"
            ),
            types.Resource(
                uri="business://tools",
                name="Business Tools",
                description="500+ business applications via Rube MCP",
                mimeType="application/json"
            )
        ]
    )

@server.list_prompts()
async def handle_list_prompts() -> ListPromptsResult:
    """List available prompts"""
    return ListPromptsResult(
        prompts=[
            types.Prompt(
                name="business_assistant",
                description="Executive business assistant prompt",
                arguments=[
                    types.PromptArgument(
                        name="task",
                        description="Business task or question",
                        required=True
                    )
                ]
            )
        ]
    )

async def main():
    """Run the MCP server"""
    logger.info("Starting Business Agent MCP Server...")
    logger.info(f"LangGraph URL: {LANGGRAPH_URL}")
    logger.info(f"Rube Session: {RUBE_SESSION_ID}")
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="business-agent-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
