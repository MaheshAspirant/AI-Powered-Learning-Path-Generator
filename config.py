"""
Configuration management for MCP Learning Path Generator.

This module handles environment variables and default configuration settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Configuration class for managing application settings."""
    
    # API Keys
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    
    # Pipedream URLs
    YOUTUBE_PIPEDREAM_URL: Optional[str] = os.getenv("YOUTUBE_PIPEDREAM_URL")
    DRIVE_PIPEDREAM_URL: Optional[str] = os.getenv("DRIVE_PIPEDREAM_URL")
    NOTION_PIPEDREAM_URL: Optional[str] = os.getenv("NOTION_PIPEDREAM_URL")
    
    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    RECURSION_LIMIT: int = int(os.getenv("RECURSION_LIMIT", "100"))
    
    # Application Settings
    PAGE_TITLE: str = os.getenv("PAGE_TITLE", "MCP Learning Path Generator")
    PAGE_ICON: str = os.getenv("PAGE_ICON", "🤖")
    
    @classmethod
    def get_google_api_key(cls) -> Optional[str]:
        """Get Google API key from environment or return None."""
        return cls.GOOGLE_API_KEY
    
    @classmethod
    def get_youtube_url(cls) -> Optional[str]:
        """Get YouTube Pipedream URL from environment or return None."""
        return cls.YOUTUBE_PIPEDREAM_URL
    
    @classmethod
    def get_drive_url(cls) -> Optional[str]:
        """Get Drive Pipedream URL from environment or return None."""
        return cls.DRIVE_PIPEDREAM_URL
    
    @classmethod
    def get_notion_url(cls) -> Optional[str]:
        """Get Notion Pipedream URL from environment or return None."""
        return cls.NOTION_PIPEDREAM_URL
    
    @classmethod
    def validate_config(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration settings.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Note: API key and URLs can be provided via UI, so we don't require them here
        # But we can validate format if they exist
        
        if cls.GOOGLE_API_KEY and len(cls.GOOGLE_API_KEY.strip()) < 10:
            errors.append("GOOGLE_API_KEY appears to be invalid (too short)")
        
        return len(errors) == 0, errors



