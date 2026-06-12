"""
Configuration module for loading and validating environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Singleton configuration class for application settings."""
    
    _instance: Optional['Settings'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize and validate required environment variables."""
        self.GROK_API_KEY = self._get_env_var("GROK_API_KEY")
        self.DB_HOST = self._get_env_var("DB_HOST")
        self.DB_USER = self._get_env_var("DB_USER")
        self.DB_PASSWORD = self._get_env_var("DB_PASSWORD")
        self.DB_NAME = self._get_env_var("DB_NAME")
        self.DB_PORT = int(os.getenv("DB_PORT", "3306"))
        
        # Groq API configuration
        self.GROK_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    @staticmethod
    def _get_env_var(key: str) -> str:
        """
        Retrieve and validate an environment variable.
        
        Args:
            key: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If required environment variable is missing
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value


# Create singleton instance
settings = Settings()