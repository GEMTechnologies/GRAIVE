# Getting Started with Graive AI

## Overview

Graive AI is an autonomous general intelligence platform that combines a unified agent loop architecture with multi-provider LLM support and comprehensive document handling capabilities. This guide provides step-by-step instructions for installation, configuration, and initial usage.

## Prerequisites

Before beginning installation, ensure your system meets the following requirements:

- Python 3.9 or higher installed and available in your PATH
- pip package manager (included with Python)
- Git for version control (optional but recommended)
- API keys for at least one LLM provider (OpenAI, DeepSeek, or Gemini)

## Installation

### Step 1: Clone the Repository

Clone the Graive repository to your local machine:

```bash
git clone <repository-url>
cd GRAIVE
```

### Step 2: Create Virtual Environment

Create and activate a Python virtual environment to isolate dependencies:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages using the requirements file:

```bash
pip install -r requirements.txt
```

This installs all necessary dependencies including LLM provider SDKs and document handling libraries.

## Configuration

### Environment Variables

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# DeepSeek Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

You only need to configure the providers you plan to use.

## Project Structure

```
GRAIVE/
├── src/                    # Source code
│   ├── core/              # Core agent loop and AI reasoning
│   │   ├── __init__.py
│   │   └── agent_loop.py
│   ├── tools/             # Tool implementations
│   │   ├── __init__.py
│   │   ├── base_tool.py
│   │   ├── shell/
│   │   └── file/
│   ├── orchestrator/      # Tool orchestration layer
│   │   ├── __init__.py
│   │   └── tool_orchestrator.py
│   ├── context/           # Context and knowledge base
│   │   ├── __init__.py
│   │   └── context_manager.py
│   └── __init__.py
├── config/                # Configuration files
│   └── config.yaml
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_agent_loop.py
│   └── test_context_manager.py
├── docs/                  # Documentation
│   └── ARCHITECTURE.md
├── examples/              # Example use cases
│   ├── __init__.py
│   └── basic_usage.py
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## Running Examples

### Complete Integration Demo

Run the comprehensive integration example that demonstrates document creation in multiple formats:

```bash
python examples/complete_integration.py
```

This example creates Markdown, Word, PowerPoint, and PDF documents showcasing the document tool's capabilities.

### LLM Provider Demo

Test your LLM provider configuration:

```bash
python examples/llm_providers_demo.py
```

This validates your API credentials and demonstrates basic LLM interactions.

### Document Tool Demo

Explore document creation and reading capabilities:

```bash
python examples/document_demo.py
```

### Basic Usage

See the fundamental agent setup:

```bash
python examples/basic_usage.py
```

## Running Tests

Execute the test suite to verify your installation:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent_loop.py
```

## Key Concepts

### Agent Loop

The Agent Loop represents the core reasoning engine that operates in a continuous cycle of analysis, thinking, tool selection, execution, and observation. This iterative pattern enables adaptive behavior when confronting complex tasks.

### LLM Providers

Graive supports multiple LLM backends through a unified interface. You can configure different providers for different use cases or switch providers without modifying application code. Refer to the [LLM Providers Guide](LLM_PROVIDERS.md) for detailed configuration instructions.

### Document Tool

The document tool enables creation and reading of multiple file formats including Markdown, Word, PowerPoint, PDF, HTML, and plain text. This capability allows the agent to generate professional documentation autonomously. See the [Document Tool Guide](DOCUMENT_TOOL.md) for comprehensive examples.

### Tool Orchestrator

The orchestrator manages tool registration, parameter validation, execution, and audit logging. It provides a clean separation between high-level agent decisions and low-level tool implementations.

### Context Manager

The context manager maintains conversation history, task plans, tool observations, and system state. This persistent memory enables coherent behavior across extended interactions.

## Next Steps

After completing the initial setup, explore these resources:

1. Review the [Architecture Documentation](ARCHITECTURE.md) to understand system design
2. Study the [LLM Providers Guide](LLM_PROVIDERS.md) for provider-specific configuration
3. Explore the [Document Tool Guide](DOCUMENT_TOOL.md) for document handling patterns
4. Examine example files in the `examples/` directory for usage patterns
5. Implement custom tools by extending the `BaseTool` interface

## Development

This foundational structure supports extensive customization and extension:

### Adding Custom LLM Providers

Implement the `BaseLLMProvider` interface to add new LLM backends:

```python
from src.llm.base_provider import BaseLLMProvider

class CustomProvider(BaseLLMProvider):
    # Implementation details
    pass

# Register with factory
from src.llm import LLMProviderFactory
LLMProviderFactory.register_provider("custom", CustomProvider)
```

### Creating Custom Tools

Extend the `BaseTool` class to implement new capabilities:

```python
from src.tools.base_tool import BaseTool

class CustomTool(BaseTool):
    @property
    def name(self) -> str:
        return "custom"
    
    def execute(self, parameters):
        # Implementation
        pass
```

### API Integration

Build REST or GraphQL APIs to expose Graive capabilities to external applications. The modular architecture facilitates clean API design with clear separation of concerns.

### User Interface Development

Create web or CLI interfaces for end users. The agent loop can be integrated into various frontend frameworks while maintaining consistent backend behavior.

## Troubleshooting

### API Key Issues

If you encounter authentication errors, verify that your API keys are correctly set in the `.env` file and that the environment variables are loaded properly. Use `python-dotenv` to load variables automatically.

### Import Errors

Ensure all dependencies are installed and your virtual environment is activated. Run `pip install -r requirements.txt` to reinstall dependencies if needed.

### Document Generation Errors

Verify that document handling libraries are installed correctly. Some platforms may require additional system dependencies for PDF or image processing.

## Support and Resources

For additional assistance, refer to the comprehensive documentation in the `docs/` directory or examine the example implementations in `examples/`.
