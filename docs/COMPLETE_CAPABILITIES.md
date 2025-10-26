# Complete System Capabilities - Graive AI

## Overview

Graive AI is now a complete autonomous intelligence platform with comprehensive capabilities across all major domains of data processing, content creation, and analysis. This document provides a complete overview of all system capabilities.

## Core Capabilities Matrix

| Category | Tools | Formats | Operations |
|----------|-------|---------|------------|
| **Documents** | Document Tool | MD, DOCX, PPTX, PDF, HTML, TXT | Create, Read, Convert |
| **Images** | Image Tool | PNG, JPG, GIF, WEBP | Generate, Edit, Analyze, Upscale |
| **Web** | Web Scraping Tool | HTML, PDF, Images | Scrape, Extract, Download, Cite |
| **Data** | Data Analysis Tool | CSV, Excel, JSON, SQL, Parquet | Analyze, Visualize, Transform |
| **Audio** | Media Tool | MP3, WAV, OGG, FLAC, M4A | TTS, STT, Generate, Convert |
| **Video** | Media Tool | MP4, AVI, MOV, WEBM, MKV | Create, Edit, Merge, Extract |

## 1. Image Generation and Processing

### Supported Providers
- **DALL-E 2 & 3** (OpenAI) - Industry-leading image generation
- **Gemini Imagen** (Google) - Multimodal image capabilities  
- **Stability AI** - Stable Diffusion models

### Capabilities

**Image Generation from Text**
```python
result = image_tool.execute({
    "action": "generate",
    "provider": "dalle",
    "prompt": "A futuristic cityscape at sunset",
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid"
})
```

**Image Editing**
```python
result = image_tool.execute({
    "action": "edit",
    "provider": "dalle",
    "image_path": "original.png",
    "prompt": "Add a rainbow in the sky"
})
```

**Image Analysis with Vision Models**
```python
result = image_tool.execute({
    "action": "analyze",
    "provider": "openai",  # or "gemini"
    "image_path": "image.jpg",
    "prompt": "Describe this image in detail"
})
```

**Variation Generation**
```python
result = image_tool.execute({
    "action": "variation",
    "image_path": "original.png",
    "n": 3
})
```

**Image Upscaling**
```python
result = image_tool.execute({
    "action": "upscale",
    "image_path": "low_res.jpg",
    "scale_factor": 2
})
```

### Use Cases
- Marketing material generation
- Product visualization
- Concept art creation
- Image enhancement and editing
- Visual content analysis
- Automated illustration

## 2. Web Scraping and Content Extraction

### Capabilities

**Visit and Extract Metadata**
```python
result = web_tool.execute({
    "action": "visit",
    "url": "https://example.com"
})
```

**Extract Clean Text**
```python
result = web_tool.execute({
    "action": "extract_text",
    "url": "https://example.com",
    "wait_for_js": True  # For JavaScript-rendered pages
})
```

**Targeted Data Extraction with CSS Selectors**
```python
result = web_tool.execute({
    "action": "extract_data",
    "url": "https://example.com",
    "selectors": {
        "title": "h1.main-title",
        "author": "span.author-name",
        "content": "div.article-body p"
    }
})
```

**Download Images**
```python
result = web_tool.execute({
    "action": "download_images",
    "url": "https://example.com",
    "max_images": 10
})
```

**Download and Parse PDFs**
```python
result = web_tool.execute({
    "action": "parse_pdf",
    "url": "https://example.com/document.pdf"
})
```

**Generate Citations**
```python
result = web_tool.execute({
    "action": "generate_citation",
    "url": "https://example.com/article",
    "citation_style": "apa"  # or "mla", "chicago", "ieee"
})
```

**Extract All Links**
```python
result = web_tool.execute({
    "action": "get_links",
    "url": "https://example.com"
})
```

**Take Screenshots**
```python
result = web_tool.execute({
    "action": "screenshot",
    "url": "https://example.com"
})
```

**Search Within Page**
```python
result = web_tool.execute({
    "action": "search_page",
    "url": "https://example.com",
    "search_term": "machine learning"
})
```

### Use Cases
- Research and data collection
- Content aggregation
- Academic citation generation
- Journal article extraction
- Image sourcing and attribution
- Web monitoring and tracking
- Competitive analysis
- Documentation gathering

## 3. Data Analysis and Visualization

### Supported Formats
- CSV files
- Excel spreadsheets (.xlsx, .xls)
- JSON data
- SQL databases
- Parquet files

### Capabilities

**Load and Analyze Data**
```python
result = data_tool.execute({
    "action": "analyze",
    "data_source": "sales_data.csv",
    "format": "csv"
})
```

**Calculate Detailed Statistics**
```python
result = data_tool.execute({
    "action": "statistics",
    "data_source": "data.xlsx",
    "format": "excel",
    "columns": ["revenue", "profit", "growth"]
})
```

**Create Visualizations**
```python
# Line chart
result = data_tool.execute({
    "action": "visualize",
    "data_source": "data.csv",
    "chart_type": "line",
    "columns": ["sales", "revenue"]
})

# Correlation heatmap
result = data_tool.execute({
    "action": "visualize",
    "data_source": "data.csv",
    "chart_type": "heatmap"
})

# Scatter plot
result = data_tool.execute({
    "action": "visualize",
    "data_source": "data.csv",
    "chart_type": "scatter",
    "columns": ["price", "demand"]
})
```

**Transform Data**
```python
# Normalize data
result = data_tool.execute({
    "action": "transform",
    "data_source": "data.csv",
    "transformation": "normalize",
    "columns": ["feature1", "feature2"]
})

# Standardize data
result = data_tool.execute({
    "action": "transform",
    "data_source": "data.csv",
    "transformation": "standardize"
})
```

**Filter Data**
```python
result = data_tool.execute({
    "action": "filter",
    "data_source": "data.csv",
    "conditions": {
        "sales": {"operator": ">", "value": 1000},
        "region": {"operator": "==", "value": "North"}
    }
})
```

**Group and Aggregate**
```python
result = data_tool.execute({
    "action": "group_by",
    "data_source": "data.csv",
    "group_by": ["region", "product"],
    "aggregations": {"sales": "sum", "quantity": "mean"}
})
```

**Create Pivot Tables**
```python
result = data_tool.execute({
    "action": "pivot",
    "data_source": "data.csv",
    "index": "region",
    "pivot_columns": "product",
    "values": "sales",
    "aggfunc": "sum"
})
```

**Merge Datasets**
```python
result = data_tool.execute({
    "action": "merge",
    "sources": ["data1.csv", "data2.csv"],
    "merge_on": "id",
    "how": "inner"
})
```

**Calculate Correlations**
```python
result = data_tool.execute({
    "action": "correlation",
    "data_source": "data.csv"
})
```

**Export in Multiple Formats**
```python
result = data_tool.execute({
    "action": "export",
    "data_source": "data.csv",
    "export_format": "excel",  # or "json", "html"
    "filename": "output_data"
})
```

### Visualization Types
- Line charts
- Bar charts
- Scatter plots
- Histograms
- Box plots
- Violin plots
- Heatmaps
- Pie charts
- Area charts
- Correlation matrices

### Use Cases
- Business intelligence
- Financial analysis
- Sales reporting
- Market research
- Scientific data analysis
- Statistical modeling
- Trend identification
- Performance tracking
- Predictive analytics

## 4. Audio and Video Processing

### Audio Capabilities

**Text-to-Speech (TTS)**
```python
result = media_tool.execute({
    "action": "text_to_speech",
    "text": "Hello, I am Graive AI",
    "voice": "alloy",  # alloy, echo, fable, onyx, nova, shimmer
    "model": "tts-1-hd"
})
```

**Speech-to-Text (STT)**
```python
result = media_tool.execute({
    "action": "speech_to_text",
    "audio_path": "recording.mp3",
    "language": "en"
})
```

**Audio Format Conversion**
```python
result = media_tool.execute({
    "action": "convert_format",
    "input_path": "audio.wav",
    "output_format": "mp3",
    "media_type": "audio"
})
```

### Video Capabilities

**Create Video from Images**
```python
result = media_tool.execute({
    "action": "create_video",
    "images": ["img1.jpg", "img2.jpg", "img3.jpg"],
    "audio_path": "narration.mp3",
    "duration_per_image": 3,
    "fps": 24
})
```

**Edit Video**
```python
# Trim video
result = media_tool.execute({
    "action": "edit_video",
    "video_path": "video.mp4",
    "operation": "trim",
    "start_time": 5,
    "end_time": 30
})

# Resize video
result = media_tool.execute({
    "action": "edit_video",
    "video_path": "video.mp4",
    "operation": "resize",
    "width": 1920,
    "height": 1080
})

# Change speed
result = media_tool.execute({
    "action": "edit_video",
    "video_path": "video.mp4",
    "operation": "speed",
    "speed_factor": 1.5
})
```

**Extract Audio from Video**
```python
result = media_tool.execute({
    "action": "extract_audio",
    "video_path": "video.mp4"
})
```

**Add Subtitles**
```python
result = media_tool.execute({
    "action": "add_subtitles",
    "video_path": "video.mp4",
    "subtitles": [
        {"text": "Hello", "start": 0, "end": 2},
        {"text": "World", "start": 2, "end": 4}
    ]
})
```

**Merge Videos**
```python
result = media_tool.execute({
    "action": "merge_videos",
    "video_paths": ["video1.mp4", "video2.mp4", "video3.mp4"]
})
```

### Use Cases
- Podcast creation
- Video tutorials
- Audiobook generation
- Transcription services
- Video presentations
- Marketing videos
- Educational content
- Accessibility features (subtitles, audio descriptions)

## 5. Complete Workflow Integration

### End-to-End Research Workflow

```python
# 1. Scrape research content
web_result = web_tool.execute({
    "action": "extract_text",
    "url": "https://research-article.com"
})

# 2. Generate citation
citation = web_tool.execute({
    "action": "generate_citation",
    "url": "https://research-article.com",
    "citation_style": "apa"
})

# 3. Create illustration
image = image_tool.execute({
    "action": "generate",
    "prompt": "Illustration of research topic",
    "provider": "dalle"
})

# 4. Create narration
audio = media_tool.execute({
    "action": "text_to_speech",
    "text": web_result["text"][:1000]
})

# 5. Generate presentation
from src.tools.document.document_tool import DocumentTool
doc_tool = DocumentTool()
presentation = doc_tool.execute({
    "action": "create",
    "format": "powerpoint",
    "filename": "research_presentation.pptx",
    "content": {...}
})
```

### Data Analysis Workflow

```python
# 1. Load data from web
web_result = web_tool.execute({
    "action": "download_pdf",
    "url": "https://example.com/data.pdf"
})

# 2. Analyze data
analysis = data_tool.execute({
    "action": "analyze",
    "data_source": "extracted_data.csv"
})

# 3. Create visualizations
viz = data_tool.execute({
    "action": "visualize",
    "chart_type": "correlation_matrix"
})

# 4. Generate report
report = doc_tool.execute({
    "action": "create",
    "format": "word",
    "filename": "analysis_report.docx"
})
```

## System Requirements

### Python Packages

```bash
# Image Processing
pip install openai pillow opencv-python

# Web Scraping
pip install requests beautifulsoup4 selenium lxml

# Data Analysis
pip install pandas numpy scipy scikit-learn matplotlib seaborn plotly openpyxl

# Media Processing
pip install moviepy pydub speech-recognition

# Document Processing
pip install python-docx python-pptx fpdf2 PyPDF2
```

### API Keys Required

```bash
# For image generation and analysis
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
STABILITY_API_KEY=your_stability_key

# Optional for enhanced features
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Performance Considerations

- **Image Generation**: 10-30 seconds per image
- **Web Scraping**: 1-5 seconds per page (depends on size)
- **Data Analysis**: Varies by dataset size (optimized for millions of rows)
- **Video Processing**: Depends on length and operations
- **Audio Processing**: Near real-time for most operations

## Complete System Architecture

The Graive system now includes:

1. **Core Agent Loop** - Unified reasoning engine
2. **LLM Providers** - OpenAI, DeepSeek, Gemini
3. **Document Tools** - 6 formats supported
4. **Image Tools** - 3 AI providers
5. **Web Tools** - Comprehensive scraping
6. **Data Tools** - Full analytics suite
7. **Media Tools** - Audio and video processing
8. **Tool Orchestrator** - Central management
9. **Context Manager** - State persistence

This creates a complete autonomous AI system capable of handling virtually any information processing task.
