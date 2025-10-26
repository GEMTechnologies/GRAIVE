# Graive AI - Quick Reference Guide

## Installation (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run interactive demo
python examples/interactive_agent_demo.py
```

## Human-in-the-Loop Commands

```python
from src.core.interactive_loop import InteractiveAgentLoop, InteractionMode
from src.context.enhanced_context_manager import EnhancedContextManager

# Initialize with infinite memory
context = EnhancedContextManager("You are Graive", enable_infinite_memory=True)
agent = InteractiveAgentLoop(orchestrator, context, InteractionMode.INTERRUPTIBLE)

# Run with interrupts enabled
result = agent.run("Your task here", enable_interrupts=True)

# During execution, user can type:
# - "pause" - Pause the agent
# - "continue" - Resume execution
# - "stop" - Stop gracefully
# - "modify <new goal>" - Change direction
# - "feedback <message>" - Provide input
# - Any other text - Add as context
```

## Infinite Memory

```python
# Memory automatically manages unlimited context
stats = context.get_memory_statistics()
print(f"Total messages: {stats['total_messages']}")
print(f"Compressions: {stats['compression_count']}")

# Search across entire history
results = context.search_context("machine learning", max_results=5)

# Force compression
context.compress_memory_now()

# Save checkpoint
context.save_checkpoint("important_point")
```

## All Tools Quick Reference

### Image Generation & Analysis
```python
from src.tools.image.image_tool import ImageTool
tool = ImageTool()

# Generate image with DALL-E
tool.execute({
    "action": "generate",
    "provider": "dalle",
    "prompt": "A futuristic cityscape",
    "size": "1024x1024",
    "quality": "hd"
})

# Analyze image
tool.execute({
    "action": "analyze",
    "provider": "openai",
    "image_path": "image.jpg",
    "prompt": "Describe this image"
})
```

### Web Scraping
```python
from src.tools.web.web_scraping_tool import WebScrapingTool
tool = WebScrapingTool()

# Extract text
tool.execute({
    "action": "extract_text",
    "url": "https://example.com"
})

# Download images
tool.execute({
    "action": "download_images",
    "url": "https://example.com",
    "max_images": 5
})

# Generate citation
tool.execute({
    "action": "generate_citation",
    "url": "https://example.com",
    "citation_style": "apa"
})
```

### Data Analysis
```python
from src.tools.data.data_analysis_tool import DataAnalysisTool
tool = DataAnalysisTool()

# Analyze data
tool.execute({
    "action": "analyze",
    "data_source": "data.csv",
    "format": "csv"
})

# Create visualization
tool.execute({
    "action": "visualize",
    "data_source": "data.csv",
    "chart_type": "line",
    "columns": ["sales", "revenue"]
})

# Calculate statistics
tool.execute({
    "action": "statistics",
    "data_source": "data.xlsx",
    "format": "excel",
    "columns": ["price", "quantity"]
})
```

### Audio & Video
```python
from src.tools.media.media_tool import MediaTool
tool = MediaTool()

# Text to speech
tool.execute({
    "action": "text_to_speech",
    "text": "Hello world",
    "voice": "alloy"
})

# Speech to text
tool.execute({
    "action": "speech_to_text",
    "audio_path": "audio.mp3"
})

# Create video from images
tool.execute({
    "action": "create_video",
    "images": ["img1.jpg", "img2.jpg"],
    "audio_path": "narration.mp3"
})
```

## LLM Provider Usage

### OpenAI
```python
from src.llm import LLMProviderFactory, LLMMessage

provider = LLMProviderFactory.create_provider("openai")
messages = [LLMMessage(role="user", content="Hello!")]
response = provider.generate(messages)
```

### DeepSeek
```python
provider = LLMProviderFactory.create_provider("deepseek")
```

### Gemini
```python
provider = LLMProviderFactory.create_provider("gemini")
```

## Document Creation

### Markdown
```python
from src.tools.document.document_tool import DocumentTool

tool = DocumentTool()
result = tool.execute({
    "action": "create",
    "format": "markdown",
    "filename": "doc.md",
    "content": {
        "title": "Title",
        "sections": [{"heading": "H1", "level": 2, "content": "Text"}]
    }
})
```

### Word Document
```python
result = tool.execute({
    "action": "create",
    "format": "word",
    "filename": "doc.docx",
    "content": { /* same structure */ }
})
```

### PowerPoint
```python
result = tool.execute({
    "action": "create",
    "format": "powerpoint",
    "filename": "presentation.pptx",
    "content": {
        "slides": [
            {"type": "title", "title": "Title", "subtitle": "Subtitle"},
            {"type": "content", "title": "Slide", "points": ["Point 1"]}
        ]
    }
})
```

### PDF
```python
result = tool.execute({
    "action": "create",
    "format": "pdf",
    "filename": "doc.pdf",
    "content": { /* same structure as markdown */ }
})
```

## Document Reading

```python
result = tool.execute({
    "action": "read",
    "format": "markdown",  # or word, pdf, powerpoint, etc.
    "filename": "doc.md"
})

if result["success"]:
    content = result["content"]
```

## Environment Variables

```bash
# Required (pick at least one)
OPENAI_API_KEY=sk-...              # For GPT, DALL-E, Whisper, TTS
DEEPSEEK_API_KEY=sk-...
GEMINI_API_KEY=...

# Optional
STABILITY_API_KEY=...              # For Stability AI images
OPENAI_MODEL=gpt-4-turbo-preview
DEEPSEEK_MODEL=deepseek-chat
GEMINI_MODEL=gemini-pro
```

## Complete Tool List

| Tool | Purpose | Key Actions |
|------|---------|-------------|
| **Document** | Create/read docs | create, read, convert |
| **Image** | Generate/analyze images | generate, edit, analyze, upscale |
| **Web** | Scrape websites | visit, extract, download, cite |
| **Data** | Analyze data | analyze, visualize, statistics |
| **Media** | Audio/video | TTS, STT, create, edit, merge |
| **LLM** | AI generation | OpenAI, DeepSeek, Gemini |
| **Shell** | Run commands | execute |
| **File** | File ops | read, write, append |

## File Structure

```
GRAIVE/
├── src/
│   ├── llm/            # LLM providers (OpenAI, DeepSeek, Gemini)
│   ├── tools/          # Tools (Shell, File, Document)
│   ├── core/           # Agent loop
│   ├── orchestrator/   # Tool orchestration
│   └── context/        # Context management
├── examples/           # Ready-to-run examples
├── docs/              # Comprehensive documentation
└── tests/             # Test suite
```

## Key Documentation

- **Setup**: `docs/GETTING_STARTED.md`
- **LLM Providers**: `docs/LLM_PROVIDERS.md`
- **Documents**: `docs/DOCUMENT_TOOL.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Features**: `docs/FEATURES.md`
- **Implementation**: `IMPLEMENTATION_SUMMARY.md`

## Quick Commands

```bash
# Run all examples
python examples/complete_integration.py
python examples/llm_providers_demo.py
python examples/document_demo.py
python examples/basic_usage.py

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Supported Document Formats

✓ Markdown (.md)
✓ Microsoft Word (.docx)
✓ PowerPoint (.pptx)
✓ PDF (.pdf)
✓ HTML (.html)
✓ Plain Text (.txt)

## Supported LLM Providers

✓ OpenAI (GPT-4, GPT-4 Turbo, GPT-3.5)
✓ DeepSeek (DeepSeek-Chat, DeepSeek-Coder)
✓ Google Gemini (Gemini Pro, Gemini Pro Vision)

## Common Tasks

### Create a Report in All Formats
```python
tool = DocumentTool()
content = {"title": "Report", "sections": [...]}

for fmt in ["markdown", "word", "powerpoint", "pdf"]:
    tool.execute({
        "action": "create",
        "format": fmt,
        "filename": f"report.{fmt}",
        "content": content
    })
```

### Switch LLM Providers
```python
# Just change the provider name
provider = LLMProviderFactory.create_provider("deepseek")  # was "openai"
# Everything else stays the same!
```

### Register Custom Tool
```python
from src.orchestrator import ToolOrchestrator
from src.tools.base_tool import BaseTool

orchestrator = ToolOrchestrator()
orchestrator.register_tool(YourCustomTool())
```

## Troubleshooting

**Import errors?** → Activate virtual environment and reinstall
```bash
pip install -r requirements.txt
```

**API key errors?** → Check `.env` file has correct keys

**Document errors?** → Install missing libraries
```bash
pip install python-docx python-pptx fpdf2 PyPDF2
```

## Next Steps

1. Configure your API keys in `.env`
2. Run `python examples/complete_integration.py`
3. Read `docs/GETTING_STARTED.md` for detailed guide
4. Explore other examples in `examples/` directory
5. Review architecture in `docs/ARCHITECTURE.md`
