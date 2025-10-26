# Graive AI - Autonomous General Intelligence

Graive is an autonomous general AI agent, a sophisticated digital entity engineered to serve as a versatile and proficient collaborator in a wide array of tasks. Conceived as a Turing-complete problem solver, Graive operates through step-by-step iteration and tool-based execution within a secure, sandboxed environment.

## 🚀 Complete Feature Set

### Human-in-the-Loop Interaction

Advanced interactive system allowing users to interrupt the agent at any time during execution. The system supports real-time pause and resume, dynamic goal modification mid-execution, context injection at any point, user feedback incorporation, and multiple interaction modes (autonomous, collaborative, interruptible, supervised). Users maintain full control and can redirect the agent instantly based on changing requirements.

### Infinite Memory Management

Sophisticated memory system that never loses context regardless of conversation length. The system implements automatic memory compression when approaching token limits, intelligent hierarchical summarization preserving key information, three-tier memory architecture (working, short-term, long-term), complete persistence across sessions, and fast retrieval of relevant historical context. Conversations can span millions of tokens without information loss.

### Multi-Provider LLM Support

Graive seamlessly integrates with multiple LLM providers, ensuring flexibility in deployment and cost optimization. The system supports OpenAI (GPT-4, GPT-4 Turbo, GPT-3.5), DeepSeek (DeepSeek-Chat, DeepSeek-Coder), and Google Gemini (Gemini Pro, Gemini Pro Vision). This multi-provider architecture allows organizations to select the most appropriate model based on performance requirements, budget constraints, and specific use cases.

### Comprehensive Document Handling

The document tool provides extensive capabilities for creating and reading various file formats. Supported formats include Markdown (.md) for technical documentation, Microsoft Word (.docx) for professional reports, PowerPoint (.pptx) for presentations, PDF for universal distribution, HTML for web content, and plain text for simple data. Each format maintains proper structure and formatting, with the ability to convert between formats while preserving content integrity.

### Image Generation and Analysis

Powerful image processing capabilities using DALL-E 2/3, Gemini Imagen, and Stability AI. Generate images from text prompts, edit existing images, create variations, analyze images with GPT-4 Vision and Gemini Vision, and upscale images. Supports all major image formats and professional-quality output.

### Web Scraping and Data Extraction

Comprehensive web scraping toolkit for visiting websites, extracting clean text content, downloading images and PDFs, parsing HTML and PDF documents, generating academic citations (APA, MLA, Chicago, IEEE), handling JavaScript-rendered pages, and extracting structured data with CSS selectors. Perfect for research, content aggregation, and data collection.

### Advanced Data Analysis

Full-featured data analysis and visualization suite supporting CSV, Excel, JSON, SQL, and Parquet formats. Perform statistical analysis, create stunning visualizations (line charts, scatter plots, heatmaps, correlation matrices), transform and normalize data, filter and group datasets, create pivot tables, merge multiple data sources, and export in multiple formats. Powered by pandas, numpy, matplotlib, seaborn, and plotly.

### Audio and Video Processing

Complete multimedia toolkit including text-to-speech with multiple voices (OpenAI TTS), speech-to-text transcription (Whisper), video creation from images, video editing (trim, resize, speed adjustment), audio extraction from video, subtitle generation and addition, video merging and concatenation, and format conversion for audio and video files.

### Tool-Based Architecture

The system employs a unified agent loop that dynamically leverages a comprehensive suite of tools rather than delegating to specialized sub-agents. Available tools include shell execution for system operations, file management for reading and writing files, document creation and parsing for multiple formats, and web interaction capabilities. This architecture ensures efficient resource utilization and simplified maintenance.

## Project Structure

```
GRAIVE/
├── src/
│   ├── core/           # Core agent loop and AI reasoning
│   ├── llm/            # LLM provider implementations (OpenAI, DeepSeek, Gemini)
│   ├── tools/          # Tool implementations (Shell, File, Document)
│   ├── orchestrator/   # Tool orchestration layer
│   ├── context/        # Context and knowledge base
│   └── utils/          # Utility functions
├── config/             # Configuration files
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example use cases
```

## Getting Started

Refer to the [Getting Started Guide](docs/GETTING_STARTED.md) for detailed installation and usage instructions.

## Quick Start

Install dependencies and run example demonstrations:

```bash
pip install -r requirements.txt
python examples/advanced_features_demo.py
```

For LLM provider integration, set your API keys:

```bash
export OPENAI_API_KEY="your-key-here"
export DEEPSEEK_API_KEY="your-key-here"
export GEMINI_API_KEY="your-key-here"
export STABILITY_API_KEY="your-key-here"  # Optional, for Stability AI
```

## 🎯 Key Capabilities

| Category | Capabilities |
|----------|-------------|
| **Documents** | MD, DOCX, PPTX, PDF, HTML, TXT creation/reading/conversion |
| **Images** | DALL-E, Gemini, Stability AI generation, GPT-4 Vision analysis |
| **Web** | Scraping, extraction, citations, PDF parsing, image downloading |
| **Data** | CSV, Excel, JSON, SQL analysis, statistics, 10+ chart types |
| **Audio** | TTS (6 voices), STT (Whisper), format conversion |
| **Video** | Creation, editing, merging, subtitles, audio extraction |
| **LLMs** | OpenAI, DeepSeek, Gemini with unified interface |
