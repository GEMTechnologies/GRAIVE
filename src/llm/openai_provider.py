"""
OpenAI LLM Provider

This module implements the OpenAI API integration, supporting models such as
GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, and other OpenAI language models. The provider
handles authentication, request formatting, and response parsing specific to the
OpenAI API architecture.
"""

from typing import List, Optional, Dict, Any
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.llm.base_provider import BaseLLMProvider, LLMMessage, LLMResponse


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI API provider implementation.
    
    This provider supports all OpenAI chat models including GPT-4, GPT-4 Turbo,
    GPT-3.5 Turbo, and future models. It implements the standard OpenAI Chat
    Completions API with support for function calling, streaming, and advanced
    parameters.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-4-turbo-preview",
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model_name: Model identifier (default: gpt-4-turbo-preview)
            base_url: Optional custom API base URL
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = base_url or "https://api.openai.com/v1"
        self._client = None
        
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "openai"
    
    @property
    def supports_function_calling(self) -> bool:
        """OpenAI supports function calling."""
        return True
    
    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                import openai
                self._client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError(
                    "OpenAI package not installed. Install with: pip install openai"
                )
        return self._client
    
    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using OpenAI's Chat Completions API.
        
        Args:
            messages: Conversation history
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            LLMResponse with generated content
        """
        client = self._get_client()
        
        # Convert messages to OpenAI format
        formatted_messages = [msg.to_dict() for msg in messages]
        
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
                raw_response=response.model_dump()
            )
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """
        Validate OpenAI API credentials.
        
        Returns:
            True if credentials are valid
        """
        try:
            client = self._get_client()
            # Simple API call to validate credentials
            client.models.list()
            return True
        except Exception:
            return False
