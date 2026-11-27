"""
Streamlit application for MCP Learning Path Generator.

This application provides a user-friendly interface for generating personalized
learning paths using the Model Context Protocol with YouTube, Google Drive, and Notion integrations.
"""

import streamlit as st
from typing import Optional
import re

from config import Config
from utils import run_agent_sync

# Page configuration
st.set_page_config(
    page_title="MCP Learning Path Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Model Context Protocol (MCP) - Learning Path Generator")
st.markdown("---")

# Initialize session state for progress and results
def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        'current_step': "",
        'progress': 0,
        'last_section': "",
        'is_generating': False,
        'result': None,
        'error_message': None,
        'generation_history': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Sidebar for API and URL configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input with validation
    st.subheader("API Keys")
    google_api_key = st.text_input(
        "Google API Key",
        type="password",
        help="Enter your Google AI Studio API key",
        value=st.session_state.get('saved_api_key', '') or Config.get_google_api_key() or ''
    )
    
    # Save API key option
    if google_api_key:
        if st.button("💾 Save API Key"):
            st.session_state.saved_api_key = google_api_key
            st.success("API key saved!")
            st.rerun()
    
    st.markdown("---")
    
    # Pipedream URLs
    st.subheader("🔗 Pipedream URLs")
    
    youtube_pipedream_url = st.text_input(
        "YouTube URL (Required)",
        placeholder="https://your-pipedream-url.com",
        help="Pipedream URL for YouTube integration",
        value=st.session_state.get('saved_youtube_url', '') or Config.get_youtube_url() or ''
    )
    
    # Secondary tool selection
    st.markdown("---")
    st.subheader("📁 Secondary Tool")
    secondary_tool = st.radio(
        "Select Secondary Tool:",
        ["Drive", "Notion"],
        help="Choose between Google Drive or Notion for document storage"
    )
    
    # Secondary tool URL input
    if secondary_tool == "Drive":
        drive_pipedream_url = st.text_input(
            "Drive URL",
            placeholder="https://your-pipedream-url.com",
            help="Pipedream URL for Google Drive integration",
            value=st.session_state.get('saved_drive_url', '') or Config.get_drive_url() or ''
        )
        notion_pipedream_url = None
    else:
        notion_pipedream_url = st.text_input(
            "Notion URL",
            placeholder="https://your-pipedream-url.com",
            help="Pipedream URL for Notion integration",
            value=st.session_state.get('saved_notion_url', '') or Config.get_notion_url() or ''
        )
        drive_pipedream_url = None
    
    st.markdown("---")
    
    # Clear session button
    if st.button("🗑️ Clear All Data"):
        for key in list(st.session_state.keys()):
            if key not in ['saved_api_key', 'saved_youtube_url', 'saved_drive_url', 'saved_notion_url']:
                del st.session_state[key]
        st.rerun()

# Helper functions for validation
def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not url:
        return False
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url.strip()))

def validate_api_key(api_key: str) -> bool:
    """Basic validation for API key format."""
    if not api_key or len(api_key.strip()) < 10:
        return False
    return True

# Quick guide before goal input
with st.expander("📖 Quick Guide", expanded=True):
    st.markdown("""
    **Getting Started:**
    1. ✅ Enter your Google API key and YouTube URL (required)
    2. ✅ Select and configure your secondary tool (Drive or Notion)
    3. ✅ Enter a clear learning goal
    
    **Example Learning Goals:**
    - "I want to learn Python basics in 3 days"
    - "I want to learn data science fundamentals in 10 days"
    - "Create a 7-day web development bootcamp"
    
    **Tips:**
    - Be specific about your learning objectives
    - Include a timeframe if you have one
    - The system will create a structured path with YouTube videos and documents
    """)

# Main content area
st.header("🎯 Enter Your Learning Goal")

user_goal = st.text_area(
    "Describe what you want to learn:",
    height=100,
    help="Describe what you want to learn, and we'll generate a structured path using YouTube content and your selected tool.",
    placeholder="Example: I want to learn Python programming basics in 5 days, focusing on data structures and algorithms."
)

# Show character count
if user_goal:
    char_count = len(user_goal)
    st.caption(f"Character count: {char_count}")

# Progress area
progress_container = st.container()
progress_bar = st.empty()
status_text = st.empty()

def update_progress(message: str):
    """Update progress in the Streamlit UI with enhanced status tracking."""
    st.session_state.current_step = message
    st.session_state.generation_history.append(message)
    
    # Determine section and update progress based on message content
    message_lower = message.lower()
    
    if "setting up agent" in message_lower:
        section = "Setup"
        st.session_state.progress = 0.1
    elif "drive integration" in message_lower or "notion integration" in message_lower:
        section = "Integration"
        st.session_state.progress = 0.2
    elif "initializing mcp" in message_lower:
        section = "Initialization"
        st.session_state.progress = 0.3
    elif "getting available tools" in message_lower:
        section = "Tool Discovery"
        st.session_state.progress = 0.4
    elif "creating ai agent" in message_lower:
        section = "Agent Creation"
        st.session_state.progress = 0.5
    elif "generating your learning path" in message_lower or "generating" in message_lower:
        section = "Generation"
        st.session_state.progress = 0.6
    elif "complete" in message_lower and "✅" in message:
        section = "Complete"
        st.session_state.progress = 1.0
        st.session_state.is_generating = False
    elif "error" in message_lower or "❌" in message:
        section = "Error"
        st.session_state.is_generating = False
    else:
        section = st.session_state.last_section or "Progress"
        # Increment progress slightly for other messages
        if st.session_state.progress < 0.9:
            st.session_state.progress = min(st.session_state.progress + 0.05, 0.9)
    
    st.session_state.last_section = section
    
    # Show progress bar with percentage
    progress_percentage = int(st.session_state.progress * 100)
    progress_bar.progress(st.session_state.progress)
    status_text.text(f"Status: {section} ({progress_percentage}%)")
    
    # Update progress container with current status
    with progress_container:
        # Show message with appropriate icon
        if "complete" in message_lower and "✅" in message:
            st.success(f"✅ {message.replace('✅', '').strip()}")
        elif "error" in message_lower or "❌" in message:
            st.error(message)
        elif "⏳" in message:
            st.info(message)
        else:
            prefix = "✓" if st.session_state.progress >= 0.5 else "→"
            st.write(f"{prefix} {message}")

# Validation and error display
validation_errors = []

if not validate_api_key(google_api_key):
    validation_errors.append("❌ Please enter a valid Google API key in the sidebar.")
elif not youtube_pipedream_url:
    validation_errors.append("❌ YouTube URL is required. Please enter your Pipedream YouTube URL.")
elif not validate_url(youtube_pipedream_url):
    validation_errors.append("❌ YouTube URL format is invalid. Please check the URL.")
elif (secondary_tool == "Drive" and not drive_pipedream_url):
    validation_errors.append("❌ Please enter your Pipedream Drive URL in the sidebar.")
elif (secondary_tool == "Drive" and drive_pipedream_url and not validate_url(drive_pipedream_url)):
    validation_errors.append("❌ Drive URL format is invalid. Please check the URL.")
elif (secondary_tool == "Notion" and not notion_pipedream_url):
    validation_errors.append("❌ Please enter your Pipedream Notion URL in the sidebar.")
elif (secondary_tool == "Notion" and notion_pipedream_url and not validate_url(notion_pipedream_url)):
    validation_errors.append("❌ Notion URL format is invalid. Please check the URL.")
elif not user_goal or len(user_goal.strip()) < 10:
    validation_errors.append("⚠️ Please enter a detailed learning goal (at least 10 characters).")

# Display validation errors
if validation_errors:
    for error in validation_errors:
        st.warning(error)

# Generate Learning Path button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🚀 Generate Learning Path",
        type="primary",
        disabled=st.session_state.is_generating or bool(validation_errors),
        use_container_width=True
    )

if generate_button and not validation_errors:
    try:
        # Set generating flag
        st.session_state.is_generating = True
        st.session_state.error_message = None
        
        # Reset progress
        st.session_state.current_step = ""
        st.session_state.progress = 0
        st.session_state.last_section = ""
        st.session_state.generation_history = []
        st.session_state.result = None
        
        # Show progress area
        with st.spinner("Initializing learning path generation..."):
            result = run_agent_sync(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                user_goal=user_goal.strip(),
                progress_callback=update_progress
            )
            
            st.session_state.result = result
        
        # Display results
        st.markdown("---")
        st.header("📚 Your Learning Path")
        
        if result and "messages" in result:
            # Display all messages from the result
            for idx, msg in enumerate(result["messages"], 1):
                with st.expander(f"Message {idx}", expanded=(idx == len(result["messages"]))):
                    st.markdown(msg.content)
            
            # Success message
            st.success("🎉 Learning path generated successfully! Check the messages above for links to your documents and playlists.")
            
            # Show generation history
            with st.expander("📋 Generation Log"):
                for log_entry in st.session_state.generation_history:
                    st.text(log_entry)
        else:
            st.error("No results were generated. Please try again.")
            st.session_state.is_generating = False
            
    except ValueError as e:
        st.error(f"❌ Validation Error: {str(e)}")
        st.info("💡 Please check your inputs and try again.")
        st.session_state.is_generating = False
        st.session_state.error_message = str(e)
        
    except RuntimeError as e:
        st.error(f"❌ Runtime Error: {str(e)}")
        st.info("💡 This might be a temporary issue. Please try again in a moment.")
        st.session_state.is_generating = False
        st.session_state.error_message = str(e)
        
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        st.error("Please check your API keys and URLs, and try again.")
        st.session_state.is_generating = False
        st.session_state.error_message = str(e)
        
        # Show error details in expander
        with st.expander("🔍 Error Details"):
            st.exception(e)

# Display previous results if available
if st.session_state.result and not st.session_state.is_generating:
    st.markdown("---")
    st.subheader("📊 Previous Results")
    if st.session_state.result and "messages" in st.session_state.result:
        for msg in st.session_state.result["messages"]:
            st.markdown(f"📚 {msg.content}")
