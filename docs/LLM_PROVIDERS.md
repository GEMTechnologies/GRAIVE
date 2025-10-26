# LLM Provider Integration Guide

## Overview

Graive AI supports multiple LLM providers through a unified interface architecture. This design allows seamless switching between different providers without modifying core agent logic, enabling organizations to optimize for performance, cost, or specific capabilities based on their requirements.

## Supported Providers

### OpenAI

OpenAI provides industry-leading language models with exceptional reasoning capabilities. The integration supports all chat-based models including GPT-4, GPT-4 Turbo, and GPT-3.5 Turbo variants.

**Configuration:**

```python
from src.llm import LLMProviderFactory

provider = LLMProviderFactory.create_provider(
    provider_name="openai",
    api_key="your-openai-api-key",
    model_name="gpt-4-turbo-preview"
)
```

**Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Preferred model (optional, defaults to gpt-4-turbo-preview)

**Supported Models:**
- gpt-4-turbo-preview
- gpt-4
- gpt-3.5-turbo
- gpt-3.5-turbo-16k

### DeepSeek

DeepSeek offers competitive performance with cost advantages for high-volume deployments. The provider uses an OpenAI-compatible API, making integration straightforward while maintaining excellent capabilities.

**Configuration:**

```python
from src.llm import LLMProviderFactory

provider = LLMProviderFactory.create_provider(
    provider_name="deepseek",
    api_key="your-deepseek-api-key",
    model_name="deepseek-chat"
)
```

**Environment Variables:**
- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `DEEPSEEK_MODEL`: Preferred model (optional, defaults to deepseek-chat)

**Supported Models:**
- deepseek-chat
- deepseek-coder

### Google Gemini

Google Gemini provides advanced capabilities including multimodal understanding. The integration supports Gemini Pro and Gemini Pro Vision models through the official Google Generative AI SDK.

**Configuration:**

```python
from src.llm import LLMProviderFactory

provider = LLMProviderFactory.create_provider(
    provider_name="gemini",
    api_key="your-gemini-api-key",
    model_name="gemini-pro"
)
```

**Environment Variables:**
- `GEMINI_API_KEY`: Your Google API key with Gemini access
- `GEMINI_MODEL`: Preferred model (optional, defaults to gemini-pro)

**Supported Models:**
- gemini-pro
- gemini-pro-vision

## Usage Patterns

### Basic Message Generation

All providers implement the same interface for generating responses:

```python
from src.llm import LLMMessage

messages = [
    LLMMessage(role="system", content="You are a helpful AI assistant."),
    LLMMessage(role="user", content="Explain the agent loop pattern.")
]

response = provider.generate(
    messages=messages,
    temperature=0.7,
    max_tokens=1000
)

print(response.content)
print(f"Tokens used: {response.tokens_used}")
```

### Provider-Specific Parameters

Each provider supports additional parameters through kwargs:

```python
# OpenAI-specific parameters
response = provider.generate(
    messages=messages,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.5,
    presence_penalty=0.5
)

# Gemini-specific parameters
response = provider.generate(
    messages=messages,
    temperature=0.7,
    top_k=40,
    top_p=0.95
)
```

### Credential Validation

Validate API credentials before making requests:

```python
if provider.validate_credentials():
    print("Credentials valid")
else:
    print("Invalid credentials")
```

## Adding Custom Providers

Extend the system with custom LLM providers by implementing the `BaseLLMProvider` interface:

```python
from src.llm.base_provider import BaseLLMProvider, LLMMessage, LLMResponse

class CustomProvider(BaseLLMProvider):
    @property
    def provider_name(self) -> str:
        return "custom"
    
    @property
    def supports_function_calling(self) -> bool:
        return True
    
    def generate(self, messages, temperature=0.7, max_tokens=None, **kwargs):
        # Implementation here
        pass
    
    def validate_credentials(self) -> bool:
        # Implementation here
        pass

# Register the custom provider
from src.llm import LLMProviderFactory

LLMProviderFactory.register_provider("custom", CustomProvider)
```

## Best Practices

### API Key Management

Never hardcode API keys in source code. Use environment variables or secure configuration management:

```python
import os
from dotenv import load_dotenv

load_dotenv()

provider = LLMProviderFactory.create_provider(
    provider_name="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Error Handling

Implement robust error handling for API calls:

```python
try:
    response = provider.generate(messages)
except RuntimeError as e:
    print(f"API error: {e}")
    # Implement fallback logic
```

### Token Management

Monitor token usage to optimize costs:

```python
response = provider.generate(messages, max_tokens=500)
print(f"Tokens used: {response.tokens_used}")

# Estimate before calling
estimated_tokens = provider.get_token_count(str(messages))
print(f"Estimated tokens: {estimated_tokens}")
```

### Provider Selection

Choose providers based on specific requirements:

- **OpenAI**: Best for complex reasoning, highest quality outputs
- **DeepSeek**: Optimal for cost-sensitive, high-volume applications
- **Gemini**: Ideal for multimodal tasks and Google Cloud integration

## Installation Requirements

Install the necessary packages for each provider:

```bash
# For OpenAI
pip install openai

# For DeepSeek (uses OpenAI SDK)
pip install openai

# For Gemini
pip install google-generativeai
```

All requirements are included in the project's `requirements.txt` file.
