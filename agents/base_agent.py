"""
Base Agent Module
Handles Google GenAI SDK integration with gemini-2.5-flash and provides a unified standard interface for all agents.
"""

import os
import json
import logging
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, DEFAULT_MODEL

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all Student Travel Agents using google-genai SDK."""
    
    def __init__(self, agent_name: str, role_description: str):
        self.agent_name = agent_name
        self.role_description = role_description
        self.api_key = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)
        self.model_name = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
        
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI client: {e}")
                self.client = None

    def has_active_client(self) -> bool:
        """Check if Gemini API Client is ready."""
        return self.client is not None

    def generate_response(self, prompt: str, system_instruction: str = "", response_schema: type = None) -> str:
        """
        Sends a prompt to Gemini 2.5 Flash via google-genai SDK.
        Returns text response or structured JSON string if schema provided.
        """
        if not self.has_active_client():
            raise RuntimeError("Gemini API Client is not configured (missing GEMINI_API_KEY).")

        config_args = {}
        if system_instruction:
            config_args["system_instruction"] = f"You are {self.agent_name}. {self.role_description}\n{system_instruction}"
        else:
            config_args["system_instruction"] = f"You are {self.agent_name}. {self.role_description}"

        if response_schema:
            config_args["response_mime_type"] = "application/json"
            config_args["response_schema"] = response_schema

        config = types.GenerateContentConfig(**config_args)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API in agent {self.agent_name}: {e}")
            raise e
