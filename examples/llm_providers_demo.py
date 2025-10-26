"""
Example demonstrating multi-provider LLM usage with Graive AI.

This example shows how to configure and use different LLM providers
(OpenAI, DeepSeek, Gemini) with the Graive agent system.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llm import LLMProviderFactory, LLMMessage


def demonstrate_openai():
    """Demonstrate OpenAI provider usage."""
    print("\n=== OpenAI Provider Demo ===")
    
    try:
        # Create OpenAI provider (reads OPENAI_API_KEY from environment)
        provider = LLMProviderFactory.create_provider(
            provider_name="openai",
            model_name="gpt-4-turbo-preview"
        )
        
        # Validate credentials
        if provider.validate_credentials():
            print("✓ OpenAI credentials validated")
        
        # Create a simple conversation
        messages = [
            LLMMessage(role="system", content="You are a helpful AI assistant."),
            LLMMessage(role="user", content="What is the Graive AI agent?")
        ]
        
        # Generate response
        response = provider.generate(messages, temperature=0.7)
        
        print(f"Model: {response.model}")
        print(f"Response: {response.content[:200]}...")
        print(f"Tokens used: {response.tokens_used}")
        
    except Exception as e:
        print(f"✗ OpenAI error: {str(e)}")


def demonstrate_deepseek():
    """Demonstrate DeepSeek provider usage."""
    print("\n=== DeepSeek Provider Demo ===")
    
    try:
        # Create DeepSeek provider (reads DEEPSEEK_API_KEY from environment)
        provider = LLMProviderFactory.create_provider(
            provider_name="deepseek",
            model_name="deepseek-chat"
        )
        
        # Validate credentials
        if provider.validate_credentials():
            print("✓ DeepSeek credentials validated")
        
        # Create a simple conversation
        messages = [
            LLMMessage(role="system", content="You are a coding expert."),
            LLMMessage(role="user", content="Explain what an agent loop is.")
        ]
        
        # Generate response
        response = provider.generate(messages, temperature=0.7)
        
        print(f"Model: {response.model}")
        print(f"Response: {response.content[:200]}...")
        print(f"Tokens used: {response.tokens_used}")
        
    except Exception as e:
        print(f"✗ DeepSeek error: {str(e)}")


def demonstrate_gemini():
    """Demonstrate Gemini provider usage."""
    print("\n=== Gemini Provider Demo ===")
    
    try:
        # Create Gemini provider (reads GEMINI_API_KEY from environment)
        provider = LLMProviderFactory.create_provider(
            provider_name="gemini",
            model_name="gemini-pro"
        )
        
        # Validate credentials
        if provider.validate_credentials():
            print("✓ Gemini credentials validated")
        
        # Create a simple conversation
        messages = [
            LLMMessage(role="system", content="You are an AI architecture expert."),
            LLMMessage(role="user", content="What is a tool orchestrator?")
        ]
        
        # Generate response
        response = provider.generate(messages, temperature=0.7)
        
        print(f"Model: {response.model}")
        print(f"Response: {response.content[:200]}...")
        print(f"Tokens used: {response.tokens_used}")
        
    except Exception as e:
        print(f"✗ Gemini error: {str(e)}")


def main():
    """Run LLM provider demonstrations."""
    print("Graive AI - Multi-Provider LLM Demo")
    print("=" * 50)
    
    # List available providers
    providers = LLMProviderFactory.get_available_providers()
    print(f"\nAvailable providers: {', '.join(providers)}")
    
    # Demonstrate each provider
    demonstrate_openai()
    demonstrate_deepseek()
    demonstrate_gemini()
    
    print("\n" + "=" * 50)
    print("Note: Set environment variables for API keys:")
    print("  - OPENAI_API_KEY for OpenAI")
    print("  - DEEPSEEK_API_KEY for DeepSeek")
    print("  - GEMINI_API_KEY for Google Gemini")


if __name__ == "__main__":
    main()
