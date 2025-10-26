"""
DeepSeek LLM Provider

This module implements the DeepSeek API integration, supporting DeepSeek's language
models. DeepSeek provides high-performance models with competitive pricing and
capabilities comparable to leading commercial alternatives.
"""

from typing import List, Optional, Dict, Any
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.llm.base_provider import BaseLLMProvider, LLMMessage, LLMResponse


class DeepSeekProvider(BaseLLMProvider):
    """
    DeepSeek API provider implementation.
    
    DeepSeek uses an OpenAI-compatible API, making integration straightforward
    while offering competitive performance and pricing. This provider supports
    all DeepSeek models including DeepSeek-Chat and DeepSeek-Coder variants.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com/v1",
        **kwargs
    ):
        """
        Initialize DeepSeek provider.
        
        Args:
            api_key: DeepSeek API key
            model_name: Model identifier (default: deepseek-chat)
            base_url: DeepSeek API base URL
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model_name, **kwargs)
        self.base_url = base_url
        self._client = None
        
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "deepseek"
    
    @property
    def supports_function_calling(self) -> bool:
        """DeepSeek supports function calling via OpenAI-compatible API."""
        return True
    
    def _get_client(self):
        """Lazy initialization of DeepSeek client using OpenAI SDK."""
        if self._client is None:
            try:
                import openai
                self._client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError(
                    "OpenAI package required for DeepSeek. Install with: pip install openai"
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
        Generate a response using DeepSeek's API.
        
        Args:
            messages: Conversation history
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse with generated content
        """
        client = self._get_client()
        
        # Convert messages to API format
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
            raise RuntimeError(f"DeepSeek API error: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """
        Validate DeepSeek API credentials.
        
        Returns:
            True if credentials are valid
        """
        try:
            client = self._get_client()
            # Test with minimal request
            client.models.list()
            return True
        except Exception:
            return False
