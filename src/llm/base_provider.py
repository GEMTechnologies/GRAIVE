"""
Base LLM Provider Interface

This module defines the abstract interface that all LLM providers must implement,
ensuring consistent interaction patterns across different AI model APIs including
OpenAI, DeepSeek, Gemini, and other providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class LLMMessage:
    """Represents a message in the conversation."""
    role: str  # 'system', 'user', 'assistant'
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert message to dictionary format."""
        return {"role": self.role, "content": self.content}


@dataclass
class LLMResponse:
    """Represents a response from the LLM."""
    content: str
    model: str
    tokens_used: int
    finish_reason: str
    raw_response: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    
    This interface ensures that the Graive agent can seamlessly work with multiple
    LLM backends without requiring changes to the core agent loop logic. Each
    provider implementation handles the specifics of API authentication, request
    formatting, and response parsing for its respective service.
    """
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: Authentication key for the API
            model_name: Specific model identifier to use
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.model_name = model_name
        self.config = kwargs
        
    @abstractmethod
    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            messages: Conversation history as list of messages
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            LLMResponse containing the generated content and metadata
        """
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate that the API credentials are correct and functional.
        
        Returns:
            True if credentials are valid, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the provider (e.g., 'openai', 'deepseek', 'gemini')."""
        pass
    
    @property
    @abstractmethod
    def supports_function_calling(self) -> bool:
        """Return whether this provider supports function calling."""
        pass
    
    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for given text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        # Basic estimation: ~4 characters per token
        return len(text) // 4
