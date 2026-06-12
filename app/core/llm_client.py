# LLM Client Module
# Manages interactions with Language Model APIs
# FILE: app/core/llm_client.py
"""
Grok API client for LLM interactions.
"""

from typing import Optional
import requests
import json

from app.core.config import settings
from app.core.logger import logger


class GrokClient:
    """Client for interacting with Grok API."""
    
    def __init__(self):
        """Initialize Grok API client."""
        self.api_key = settings.GROK_API_KEY
        self.api_url = settings.GROK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def send_prompt(self, prompt: str, temperature: float = 0.1) -> str:
        """
        Send a prompt to Grok API and return the response.
        
        Args:
            prompt: The prompt text to send
            temperature: Sampling temperature (lower = more deterministic)
            
        Returns:
            LLM response text
            
        Raises:
            Exception: If API request fails
        """
        try:
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant specialized in SQL query generation and explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "llama-3.3-70b-versatile",
                "temperature": temperature
            }
            
            logger.info("Sending request to Grok API")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json()
            message_content = result["choices"][0]["message"]["content"]
            
            logger.info("Received response from Grok API")
            return message_content.strip()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Grok API request error: {e}")
            raise Exception(f"Failed to get response from Grok API: {e}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Error parsing Grok API response: {e}")
            raise Exception(f"Failed to parse Grok API response: {e}")