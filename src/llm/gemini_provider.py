"""
Google Gemini LLM Provider

This module implements the Google Gemini API integration, supporting Google's
advanced language models including Gemini Pro, Gemini Pro Vision, and other
variants. The Gemini API offers multimodal capabilities and competitive performance.
"""

from typing import List, Optional, Dict, Any
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.llm.base_provider import BaseLLMProvider, LLMMessage, LLMResponse


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini API provider implementation.
    
    This provider supports Google's Gemini models through the official Google
    Generative AI SDK. It handles the specific message formatting and API
    patterns required by the Gemini platform.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-pro",
        **kwargs
    ):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key with Gemini access
            model_name: Model identifier (default: gemini-pro)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model_name, **kwargs)
        self._client = None
        
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "gemini"
    
    @property
    def supports_function_calling(self) -> bool:
        """Gemini supports function calling."""
        return True
    
    def _get_client(self):
        """Lazy initialization of Gemini client."""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model_name)
            except ImportError:
                raise ImportError(
                    "Google Generative AI package not installed. "
                    "Install with: pip install google-generativeai"
                )
        return self._client
    
    def _convert_messages_to_gemini_format(
        self, 
        messages: List[LLMMessage]
    ) -> tuple[Optional[str], List[Dict[str, str]]]:
        """
        Convert standard messages to Gemini format.
        
        Gemini separates system instructions from conversation history.
        
        Args:
            messages: Standard message list
            
        Returns:
            Tuple of (system_instruction, conversation_parts)
        """
        system_instruction = None
        conversation_parts = []
        
        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            elif msg.role == "user":
                conversation_parts.append({
                    "role": "user",
                    "parts": [msg.content]
                })
            elif msg.role == "assistant":
                conversation_parts.append({
                    "role": "model",
                    "parts": [msg.content]
                })
                
        return system_instruction, conversation_parts
    
    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response using Google Gemini API.
        
        Args:
            messages: Conversation history
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Gemini-specific parameters
            
        Returns:
            LLMResponse with generated content
        """
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError(
                "Google Generative AI package required. "
                "Install with: pip install google-generativeai"
            )
        
        genai.configure(api_key=self.api_key)
        
        # Convert messages to Gemini format
        system_instruction, conversation = self._convert_messages_to_gemini_format(messages)
        
        # Configure generation parameters
        generation_config = {
            "temperature": temperature,
        }
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
            
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            
            # Build conversation history
            chat = model.start_chat(history=conversation[:-1] if len(conversation) > 1 else [])
            
            # Get the last user message
            last_message = conversation[-1]["parts"][0] if conversation else ""
            
            response = chat.send_message(
                last_message,
                generation_config=generation_config
            )
            
            # Estimate token usage (Gemini doesn't always provide this)
            total_tokens = self.get_token_count(
                str(messages) + response.text
            )
            
            return LLMResponse(
                content=response.text,
                model=self.model_name,
                tokens_used=total_tokens,
                finish_reason="stop",
                raw_response={"response": response.text}
            )
            
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """
        Validate Gemini API credentials.
        
        Returns:
            True if credentials are valid
        """
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            # List available models to validate credentials
            list(genai.list_models())
            return True
        except Exception:
            return False
