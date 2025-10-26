# Document Tool Guide

## Overview

The Graive document tool provides comprehensive capabilities for creating, reading, and converting documents across multiple formats. This tool enables the agent to generate professional-quality documentation, reports, presentations, and other content in formats suitable for various use cases and distribution channels.

## Supported Formats

### Markdown (.md)

Markdown provides lightweight markup for technical documentation, README files, and web content. The tool supports GitHub-flavored Markdown with proper heading hierarchy, paragraphs, and formatting.

**Creation Example:**

```python
from src.tools.document.document_tool import DocumentTool

tool = DocumentTool()

content = {
    "title": "Technical Specification",
    "sections": [
        {
            "heading": "Introduction",
            "level": 2,
            "content": "This document outlines the technical specifications..."
        },
        {
            "heading": "Architecture",
            "level": 2,
            "content": "The system architecture consists of..."
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "markdown",
    "filename": "specification.md",
    "content": content
})
```

**Reading Example:**

```python
result = tool.execute({
    "action": "read",
    "format": "markdown",
    "filename": "specification.md"
})

if result["success"]:
    print(result["content"])
```

### Microsoft Word (.docx)

Word documents are ideal for professional reports, proposals, and formal documentation that requires rich formatting and broad compatibility.

**Creation Example:**

```python
content = {
    "title": "Annual Report",
    "sections": [
        {
            "heading": "Executive Summary",
            "level": 1,
            "content": "The organization achieved significant milestones..."
        },
        {
            "heading": "Financial Performance",
            "level": 1,
            "content": "Revenue increased by 25% year-over-year..."
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "word",
    "filename": "annual_report.docx",
    "content": content
})
```

**Reading Example:**

```python
result = tool.execute({
    "action": "read",
    "format": "word",
    "filename": "annual_report.docx"
})

if result["success"]:
    paragraphs = result["content"]["paragraphs"]
    full_text = result["content"]["full_text"]
```

### PowerPoint (.pptx)

PowerPoint presentations enable creation of slide decks for meetings, training sessions, and presentations with title slides and bullet-point content.

**Creation Example:**

```python
content = {
    "slides": [
        {
            "type": "title",
            "title": "Q4 Business Review",
            "subtitle": "Performance Analysis and Strategic Planning"
        },
        {
            "type": "content",
            "title": "Key Achievements",
            "points": [
                "Launched new product line",
                "Expanded to three new markets",
                "Increased customer satisfaction by 15%"
            ]
        },
        {
            "type": "content",
            "title": "Strategic Priorities",
            "points": [
                "Digital transformation initiatives",
                "Customer experience enhancement",
                "Operational efficiency improvements"
            ]
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "powerpoint",
    "filename": "q4_review.pptx",
    "content": content
})
```

**Reading Example:**

```python
result = tool.execute({
    "action": "read",
    "format": "powerpoint",
    "filename": "q4_review.pptx"
})

if result["success"]:
    slides = result["content"]["slides"]
    slide_count = result["content"]["slide_count"]
```

### PDF Documents (.pdf)

PDF format ensures consistent rendering across platforms and is ideal for final distribution of documents that should not be modified.

**Creation Example:**

```python
content = {
    "title": "User Guide",
    "sections": [
        {
            "heading": "Getting Started",
            "content": "Begin by installing the required dependencies..."
        },
        {
            "heading": "Configuration",
            "content": "Configure the system by setting environment variables..."
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "pdf",
    "filename": "user_guide.pdf",
    "content": content
})
```

**Reading Example:**

```python
result = tool.execute({
    "action": "read",
    "format": "pdf",
    "filename": "user_guide.pdf"
})

if result["success"]:
    pages = result["content"]["pages"]
    full_text = result["content"]["full_text"]
    page_count = result["content"]["page_count"]
```

### HTML Documents (.html)

HTML format enables web-ready content with proper semantic markup suitable for online publication and web applications.

**Creation Example:**

```python
content = {
    "title": "Web Article",
    "sections": [
        {
            "heading": "Introduction",
            "level": 2,
            "content": "This article explores the latest developments..."
        },
        {
            "heading": "Analysis",
            "level": 2,
            "content": "The data reveals several interesting trends..."
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "html",
    "filename": "article.html",
    "content": content
})
```

### Plain Text (.txt)

Plain text provides simple, universal format for basic documentation and data files without formatting requirements.

**Creation Example:**

```python
content = {
    "title": "Release Notes",
    "sections": [
        {
            "heading": "Version 2.0",
            "content": "New features and improvements in this release..."
        }
    ]
}

result = tool.execute({
    "action": "create",
    "format": "text",
    "filename": "release_notes.txt",
    "content": content
})
```

## Document Conversion

Convert documents between formats while preserving content structure:

```python
result = tool.execute({
    "action": "convert",
    "format": "markdown",
    "filename": "document.md",
    "target_format": "word",
    "target_filename": "document.docx"
})
```

## Content Structure

All document formats use a consistent content structure:

```python
content = {
    "title": "Document Title",           # Main document title
    "sections": [                        # Array of sections
        {
            "heading": "Section Heading", # Section title
            "level": 2,                   # Heading level (1-6)
            "content": "Section text..."  # Section content
        }
    ]
}
```

For PowerPoint presentations, use slide-specific structure:

```python
content = {
    "slides": [
        {
            "type": "title",              # Slide type: title or content
            "title": "Slide Title",       # Main title
            "subtitle": "Subtitle"        # Subtitle (title slides only)
        },
        {
            "type": "content",            # Content slide
            "title": "Slide Title",       # Slide heading
            "points": [                   # Bullet points
                "Point 1",
                "Point 2"
            ]
        }
    ]
}
```

## Error Handling

The tool returns structured results with success indicators:

```python
result = tool.execute(parameters)

if result["success"]:
    print(f"Success: {result['message']}")
    print(f"File path: {result['path']}")
else:
    print(f"Error: {result['error']}")
```

## Installation Requirements

Install the necessary packages for document handling:

```bash
pip install python-docx      # For Word documents
pip install python-pptx      # For PowerPoint presentations
pip install fpdf2            # For PDF creation
pip install PyPDF2           # For PDF reading
pip install markdown         # For Markdown processing
```

All requirements are included in the project's `requirements.txt` file.

## Best Practices

### Professional Formatting

Follow consistent formatting conventions across all document types. Use appropriate heading levels to establish clear document hierarchy, maintain consistent paragraph structure throughout the document, and ensure proper spacing between sections for readability.

### Content Organization

Structure documents logically with clear introduction, body, and conclusion sections. Use descriptive headings that accurately reflect section content, and break long sections into subsections for better comprehension.

### Format Selection

Choose the appropriate format based on the intended use case. Use Markdown for technical documentation and version-controlled content, Word for formal business documents and reports, PowerPoint for presentations and training materials, PDF for final distribution and archival purposes, HTML for web publication and online content, and plain text for configuration files and simple documentation.

### Error Recovery

Implement robust error handling when working with documents:

```python
try:
    result = tool.execute(parameters)
    if not result["success"]:
        print(f"Document operation failed: {result['error']}")
        # Implement fallback strategy
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle exceptional cases
```

## Integration with Agent Loop

The document tool integrates seamlessly with the Graive agent loop, enabling autonomous document generation based on task requirements:

```python
from src.core import AgentLoop
from src.orchestrator import ToolOrchestrator
from src.context import ContextManager
from src.tools.document.document_tool import DocumentTool

# Initialize components
orchestrator = ToolOrchestrator()
orchestrator.register_tool(DocumentTool())

# Agent can now use document tool
# through the orchestrator for autonomous
# document creation and reading
```

This integration allows the agent to dynamically create documentation, reports, and presentations as part of complex task execution workflows.
