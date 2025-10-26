"""
LLM Provider Manager

This module provides a factory and management system for different LLM providers,
enabling seamless switching between OpenAI, DeepSeek, Gemini, and other providers
based on configuration or runtime requirements.
"""

from typing import Dict, Type, Optional
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.llm.base_provider import BaseLLMProvider
from src.llm.openai_provider import OpenAIProvider
from src.llm.deepseek_provider import DeepSeekProvider
from src.llm.gemini_provider import GeminiProvider


class LLMProviderFactory:
    """
    Factory class for creating LLM provider instances.
    
    This factory pattern allows the Graive agent to work with multiple LLM backends
    transparently, selecting the appropriate provider based on configuration while
    maintaining a consistent interface through the BaseLLMProvider abstraction.
    """
    
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "gemini": GeminiProvider,
    }
    
    @classmethod
    def register_provider(
        cls,
        name: str,
        provider_class: Type[BaseLLMProvider]
    ) -> None:
        """
        Register a new LLM provider.
        
        This allows extending the system with custom provider implementations
        without modifying the core factory code.
        
        Args:
            name: Unique identifier for the provider
            provider_class: Provider implementation class
        """
        cls._providers[name] = provider_class
    
    @classmethod
    def create_provider(
        cls,
        provider_name: str,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> BaseLLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_name: Name of the provider (openai, deepseek, gemini)
            api_key: API key for authentication (if None, reads from environment)
            model_name: Specific model to use (if None, uses provider default)
            **kwargs: Additional provider-specific configuration
            
        Returns:
            Configured LLM provider instance
            
        Raises:
            ValueError: If provider name is not registered
            RuntimeError: If API key is missing
        """
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider '{provider_name}'. "
                f"Available providers: {available}"
            )
        
        # Get API key from environment if not provided
        if api_key is None:
            env_var_map = {
                "openai": "OPENAI_API_KEY",
                "deepseek": "DEEPSEEK_API_KEY",
                "gemini": "GEMINI_API_KEY",
            }
            env_var = env_var_map.get(provider_name, f"{provider_name.upper()}_API_KEY")
            api_key = os.getenv(env_var)
            
            if api_key is None:
                raise RuntimeError(
                    f"API key not provided and {env_var} environment variable not set"
                )
        
        # Get default model names
        default_models = {
            "openai": "gpt-4-turbo-preview",
            "deepseek": "deepseek-chat",
            "gemini": "gemini-pro",
        }
        
        if model_name is None:
            model_name = default_models.get(provider_name, "default")
        
        # Create provider instance
        provider_class = cls._providers[provider_name]
        return provider_class(api_key=api_key, model_name=model_name, **kwargs)
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """
        Get list of registered provider names.
        
        Returns:
            List of available provider identifiers
        """
        return list(cls._providers.keys())
