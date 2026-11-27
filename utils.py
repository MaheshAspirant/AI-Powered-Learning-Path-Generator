"""
Utility functions for MCP Learning Path Generator.

This module handles agent setup, tool configuration, and asynchronous execution
for generating personalized learning paths.
"""

import asyncio
import logging
from typing import Optional, Any, Callable, Dict

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI

from prompt import user_goal_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agent configuration
cfg = RunnableConfig(recursion_limit=100)
DEFAULT_MODEL = "gemini-2.5-flash"


def initialize_model(google_api_key: str, model: str = DEFAULT_MODEL) -> ChatGoogleGenerativeAI:
    """
    Initialize and return a ChatGoogleGenerativeAI model instance.
    
    Args:
        google_api_key: Google API key for authentication
        model: Model name to use (default: gemini-2.5-flash)
        
    Returns:
        Initialized ChatGoogleGenerativeAI model
        
    Raises:
        ValueError: If API key is empty or invalid
    """
    if not google_api_key or not google_api_key.strip():
        raise ValueError("Google API key cannot be empty")
    
    try:
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=google_api_key.strip()
        )
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        raise ValueError(f"Failed to initialize model: {str(e)}") from e

def _validate_url(url: str, service_name: str) -> None:
    """
    Validate that a URL is not empty and appears to be a valid URL.
    
    Args:
        url: URL to validate
        service_name: Name of the service for error messages
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url or not url.strip():
        raise ValueError(f"{service_name} URL cannot be empty")
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"{service_name} URL must start with http:// or https://")


def _build_tools_config(
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None
) -> Dict[str, Dict[str, str]]:
    """
    Build tools configuration dictionary from provided URLs.
    
    Args:
        youtube_pipedream_url: YouTube Pipedream URL (required)
        drive_pipedream_url: Google Drive Pipedream URL (optional)
        notion_pipedream_url: Notion Pipedream URL (optional)
        
    Returns:
        Dictionary containing tool configurations
        
    Raises:
        ValueError: If required URLs are invalid
    """
    _validate_url(youtube_pipedream_url, "YouTube")
    
    tools_config = {
        "youtube": {
            "url": youtube_pipedream_url.strip(),
            "transport": "streamable_http"
        }
    }
    
    if drive_pipedream_url:
        _validate_url(drive_pipedream_url, "Google Drive")
        tools_config["drive"] = {
            "url": drive_pipedream_url.strip(),
            "transport": "streamable_http"
        }
    
    if notion_pipedream_url:
        _validate_url(notion_pipedream_url, "Notion")
        tools_config["notion"] = {
            "url": notion_pipedream_url.strip(),
            "transport": "streamable_http"
        }
    
    if drive_pipedream_url and notion_pipedream_url:
        logger.warning("Both Drive and Notion URLs provided. Using both tools.")
    
    return tools_config


async def setup_agent_with_tools(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Any:
    """
    Set up the agent with YouTube (mandatory) and optional Drive or Notion tools.
    
    Args:
        google_api_key: Google API key for authentication
        youtube_pipedream_url: YouTube Pipedream URL (required)
        drive_pipedream_url: Google Drive Pipedream URL (optional)
        notion_pipedream_url: Notion Pipedream URL (optional)
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Configured agent instance
        
    Raises:
        ValueError: If required parameters are invalid
        RuntimeError: If agent setup fails
    """
    try:
        if progress_callback:
            progress_callback("Setting up agent with tools... ✅")
        
        logger.info("Building tools configuration")
        tools_config = _build_tools_config(
            youtube_pipedream_url,
            drive_pipedream_url,
            notion_pipedream_url
        )
        
        # Notify about integrations
        if drive_pipedream_url and progress_callback:
            progress_callback("Added Google Drive integration... ✅")
        
        if notion_pipedream_url and progress_callback:
            progress_callback("Added Notion integration... ✅")
        
        if progress_callback:
            progress_callback("Initializing MCP client... ✅")
        
        logger.info(f"Initializing MCP client with {len(tools_config)} tool(s)")
        mcp_client = MultiServerMCPClient(tools_config)
        
        if progress_callback:
            progress_callback("Getting available tools... ✅")
        
        logger.info("Retrieving available tools from MCP client")
        tools = await mcp_client.get_tools()
        logger.info(f"Retrieved {len(tools)} tool(s)")
        
        if progress_callback:
            progress_callback("Creating AI agent... ✅")
        
        logger.info("Initializing model and creating agent")
        mcp_orch_model = initialize_model(google_api_key)
        agent = create_react_agent(mcp_orch_model, tools)
        
        if progress_callback:
            progress_callback("Setup complete! Starting to generate learning path... ✅")
        
        logger.info("Agent setup completed successfully")
        return agent
        
    except ValueError as e:
        logger.error(f"Validation error in setup_agent_with_tools: {str(e)}")
        if progress_callback:
            progress_callback(f"❌ Error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in setup_agent_with_tools: {str(e)}", exc_info=True)
        if progress_callback:
            progress_callback(f"❌ Setup failed: {str(e)}")
        raise RuntimeError(f"Failed to setup agent: {str(e)}") from e

def run_agent_sync(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    user_goal: str = "",
    progress_callback: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    """
    Synchronous wrapper for running the agent to generate a learning path.
    
    This function creates a new event loop, sets up the agent with tools,
    and invokes it with the user's learning goal.
    
    Args:
        google_api_key: Google API key for authentication
        youtube_pipedream_url: YouTube Pipedream URL (required)
        drive_pipedream_url: Google Drive Pipedream URL (optional)
        notion_pipedream_url: Notion Pipedream URL (optional)
        user_goal: User's learning goal description
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Dictionary containing agent execution results with messages
        
    Raises:
        ValueError: If user_goal is empty or invalid
        RuntimeError: If agent execution fails
    """
    if not user_goal or not user_goal.strip():
        raise ValueError("User goal cannot be empty")
    
    async def _run() -> Dict[str, Any]:
        """Internal async function to run the agent."""
        try:
            logger.info("Starting agent setup")
            agent = await setup_agent_with_tools(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                progress_callback=progress_callback
            )
            
            # Combine user goal with prompt template
            learning_path_prompt = f"User Goal: {user_goal.strip()}\n{user_goal_prompt}"
            
            if progress_callback:
                progress_callback("Generating your learning path... ⏳")
            
            logger.info("Invoking agent with learning path prompt")
            # Run the agent
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content=learning_path_prompt)]},
                config=cfg
            )
            
            if progress_callback:
                progress_callback("Learning path generation complete! ✅")
            
            logger.info("Agent execution completed successfully")
            return result
            
        except ValueError as e:
            logger.error(f"Validation error in agent execution: {str(e)}")
            if progress_callback:
                progress_callback(f"❌ Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in agent execution: {str(e)}", exc_info=True)
            if progress_callback:
                progress_callback(f"❌ Generation failed: {str(e)}")
            raise RuntimeError(f"Failed to generate learning path: {str(e)}") from e

    # Run in new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        logger.info("Starting synchronous agent execution")
        return loop.run_until_complete(_run())
    except KeyboardInterrupt:
        logger.warning("Agent execution interrupted by user")
        if progress_callback:
            progress_callback("❌ Generation interrupted by user")
        raise
    finally:
        try:
            # Cancel any pending tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            # Wait for tasks to complete cancellation
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
        finally:
            loop.close()
            logger.info("Event loop closed")
