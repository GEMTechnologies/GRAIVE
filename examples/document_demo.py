"""
Example demonstrating document creation and reading capabilities.

This example shows how to create and read various document formats including
Markdown, Word, PowerPoint, PDF, HTML, and plain text files.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.document.document_tool import DocumentTool


def create_markdown_example():
    """Create a sample Markdown document."""
    print("\n=== Creating Markdown Document ===")
    
    tool = DocumentTool()
    
    content = {
        "title": "Graive AI Architecture Overview",
        "sections": [
            {
                "heading": "Introduction",
                "level": 2,
                "content": "Graive is an autonomous general AI agent built on a robust, "
                          "iterative Agent Loop model that governs the flow of information "
                          "and decision-making within a secure, sandboxed environment."
            },
            {
                "heading": "Core Components",
                "level": 2,
                "content": "The system consists of the Agent Loop, Tool Orchestrator, "
                          "Context Manager, and various specialized tools."
            },
            {
                "heading": "Agent Loop",
                "level": 3,
                "content": "The Agent Loop operates in a continuous cycle: Analyze → Think → "
                          "Select Tool → Execute → Observe."
            }
        ]
    }
    
    result = tool.execute({
        "action": "create",
        "format": "markdown",
        "filename": "graive_architecture.md",
        "content": content
    })
    
    if result["success"]:
        print(f"✓ {result['message']}")
    else:
        print(f"✗ Error: {result.get('error')}")


def create_word_example():
    """Create a sample Word document."""
    print("\n=== Creating Word Document ===")
    
    tool = DocumentTool()
    
    content = {
        "title": "Graive AI Technical Specification",
        "sections": [
            {
                "heading": "System Architecture",
                "level": 1,
                "content": "Graive employs a unified, single-loop architecture that dynamically "
                          "leverages a comprehensive set of tools to execute tasks. The core "
                          "components work together to provide autonomous problem-solving capabilities."
            },
            {
                "heading": "LLM Integration",
                "level": 1,
                "content": "The system supports multiple LLM providers including OpenAI, DeepSeek, "
                          "and Google Gemini, allowing flexible deployment across different "
                          "infrastructure requirements and cost considerations."
            }
        ]
    }
    
    result = tool.execute({
        "action": "create",
        "format": "word",
        "filename": "graive_spec.docx",
        "content": content
    })
    
    if result["success"]:
        print(f"✓ {result['message']}")
    else:
        print(f"✗ Error: {result.get('error')}")


def create_powerpoint_example():
    """Create a sample PowerPoint presentation."""
    print("\n=== Creating PowerPoint Presentation ===")
    
    tool = DocumentTool()
    
    content = {
        "slides": [
            {
                "type": "title",
                "title": "Graive AI Agent System",
                "subtitle": "Autonomous General Intelligence Platform"
            },
            {
                "type": "content",
                "title": "Key Features",
                "points": [
                    "Multi-provider LLM support (OpenAI, DeepSeek, Gemini)",
                    "Comprehensive document handling (MD, DOCX, PPTX, PDF)",
                    "Tool-based execution in sandboxed environment",
                    "Iterative agent loop with continuous reasoning",
                    "Extensible architecture for custom tools"
                ]
            },
            {
                "type": "content",
                "title": "Architecture Components",
                "points": [
                    "Agent Loop - Core reasoning engine",
                    "Tool Orchestrator - Manages tool execution",
                    "Context Manager - Maintains conversation state",
                    "LLM Providers - Flexible AI backend support",
                    "Document Tools - Multi-format file operations"
                ]
            }
        ]
    }
    
    result = tool.execute({
        "action": "create",
        "format": "powerpoint",
        "filename": "graive_presentation.pptx",
        "content": content
    })
    
    if result["success"]:
        print(f"✓ {result['message']}")
    else:
        print(f"✗ Error: {result.get('error')}")


def create_pdf_example():
    """Create a sample PDF document."""
    print("\n=== Creating PDF Document ===")
    
    tool = DocumentTool()
    
    content = {
        "title": "Graive AI User Guide",
        "sections": [
            {
                "heading": "Getting Started",
                "content": "Graive AI is designed to assist users by translating complex requests "
                          "into actionable, iterative steps. This guide provides an overview of "
                          "the system's capabilities and usage patterns."
            },
            {
                "heading": "Configuration",
                "content": "Set up API keys for your preferred LLM provider. Supported providers "
                          "include OpenAI (GPT-4), DeepSeek, and Google Gemini. Configure the "
                          "system through environment variables or configuration files."
            }
        ]
    }
    
    result = tool.execute({
        "action": "create",
        "format": "pdf",
        "filename": "graive_guide.pdf",
        "content": content
    })
    
    if result["success"]:
        print(f"✓ {result['message']}")
    else:
        print(f"✗ Error: {result.get('error')}")


def read_document_example():
    """Read a previously created document."""
    print("\n=== Reading Markdown Document ===")
    
    tool = DocumentTool()
    
    result = tool.execute({
        "action": "read",
        "format": "markdown",
        "filename": "graive_architecture.md"
    })
    
    if result["success"]:
        print("✓ Document read successfully")
        print(f"Content preview: {result['content'][:200]}...")
    else:
        print(f"✗ Error: {result.get('error')}")


def main():
    """Run document creation and reading demonstrations."""
    print("Graive AI - Document Tool Demo")
    print("=" * 60)
    
    # Create various document formats
    create_markdown_example()
    create_word_example()
    create_powerpoint_example()
    create_pdf_example()
    
    # Read a document
    read_document_example()
    
    print("\n" + "=" * 60)
    print("Documents created in sandbox directory")
    print("\nNote: Install required packages:")
    print("  pip install python-docx python-pptx fpdf2 PyPDF2")


if __name__ == "__main__":
    main()
