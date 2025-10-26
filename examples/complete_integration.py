"""
Integration example showing complete Graive AI workflow.

This example demonstrates how all components work together: LLM providers,
document tools, agent loop, and context management.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import AgentLoop
from src.orchestrator import ToolOrchestrator
from src.context import ContextManager
from src.tools.document.document_tool import DocumentTool
from src.tools.shell.shell_tool import ShellTool
from src.tools.file.file_tool import FileTool
from src.llm import LLMProviderFactory, LLMMessage


def create_research_report():
    """
    Demonstrate creating a comprehensive research report using Graive.
    
    This showcases the document tool's capabilities with structured content
    in multiple formats.
    """
    print("\n" + "=" * 70)
    print("Graive AI - Complete Integration Demo")
    print("Creating a Multi-Format Research Report")
    print("=" * 70)
    
    # Initialize document tool
    doc_tool = DocumentTool()
    
    # Define comprehensive report content
    report_content = {
        "title": "Graive AI: A Comprehensive Technical Analysis",
        "sections": [
            {
                "heading": "Executive Summary",
                "level": 2,
                "content": (
                    "Graive represents a significant advancement in autonomous AI agent "
                    "architecture. By implementing a unified agent loop that dynamically "
                    "leverages specialized tools rather than employing multiple sub-agents, "
                    "the system achieves exceptional efficiency and maintainability. The "
                    "architecture supports seamless integration with multiple LLM providers "
                    "including OpenAI, DeepSeek, and Google Gemini, offering organizations "
                    "flexibility in deployment strategies and cost optimization."
                )
            },
            {
                "heading": "Architectural Overview",
                "level": 2,
                "content": (
                    "The Graive architecture consists of five primary components that work "
                    "in concert to deliver autonomous problem-solving capabilities. The Agent "
                    "Loop serves as the central reasoning engine, implementing a continuous "
                    "cycle of analysis, thinking, tool selection, execution, and observation. "
                    "This iterative approach ensures adaptive behavior and resilience when "
                    "confronting complex, open-ended objectives."
                )
            },
            {
                "heading": "LLM Provider Integration",
                "level": 2,
                "content": (
                    "The multi-provider architecture represents a critical design decision "
                    "that distinguishes Graive from competing systems. Through a unified "
                    "interface abstraction, the system can leverage different LLM backends "
                    "without requiring modifications to core logic. OpenAI provides industry-"
                    "leading performance with GPT-4 and GPT-4 Turbo variants. DeepSeek offers "
                    "competitive capabilities with cost advantages for high-volume deployments. "
                    "Google Gemini delivers multimodal capabilities and competitive performance "
                    "for diverse use cases."
                )
            },
            {
                "heading": "Document Processing Capabilities",
                "level": 2,
                "content": (
                    "The document tool implements comprehensive support for multiple file "
                    "formats including Markdown for technical documentation, Microsoft Word "
                    "for professional reports, PowerPoint for presentations, PDF for universal "
                    "distribution, HTML for web content, and plain text for data interchange. "
                    "Each format handler maintains proper structure, formatting, and metadata, "
                    "with bidirectional conversion capabilities that preserve content integrity "
                    "across format transformations."
                )
            },
            {
                "heading": "Tool Orchestration Pattern",
                "level": 2,
                "content": (
                    "The Tool Orchestrator implements a sophisticated management layer that "
                    "translates high-level agent decisions into concrete tool executions. "
                    "Rather than maintaining separate agent instances for different capabilities, "
                    "the orchestrator provides a registry of available tools, validates "
                    "parameters, manages execution flow, and maintains comprehensive audit "
                    "logs. This pattern significantly reduces system complexity while enabling "
                    "straightforward extension through new tool implementations."
                )
            },
            {
                "heading": "Context Management System",
                "level": 2,
                "content": (
                    "The Context Manager maintains the persistent knowledge base required "
                    "for effective reasoning across extended interactions. It preserves the "
                    "complete conversation history, tracks task progress through structured "
                    "plans, records tool observations with timestamps, and manages the system "
                    "prompt that defines agent behavior. This comprehensive state management "
                    "enables the agent to maintain coherent behavior across complex, multi-step "
                    "operations."
                )
            },
            {
                "heading": "Conclusion",
                "level": 2,
                "content": (
                    "Graive demonstrates that autonomous AI agents can achieve sophisticated "
                    "capabilities through well-designed architectural patterns rather than "
                    "complex multi-agent systems. The unified agent loop, flexible LLM "
                    "integration, comprehensive tool suite, and robust state management "
                    "combine to deliver a powerful platform for autonomous task execution. "
                    "Organizations seeking to deploy AI agents will find Graive offers an "
                    "excellent balance of capability, maintainability, and operational flexibility."
                )
            }
        ]
    }
    
    # Create Markdown version
    print("\n1. Creating Markdown report...")
    md_result = doc_tool.execute({
        "action": "create",
        "format": "markdown",
        "filename": "graive_technical_analysis.md",
        "content": report_content
    })
    print(f"   {'✓' if md_result['success'] else '✗'} {md_result.get('message', md_result.get('error'))}")
    
    # Create Word version
    print("\n2. Creating Word document...")
    word_result = doc_tool.execute({
        "action": "create",
        "format": "word",
        "filename": "graive_technical_analysis.docx",
        "content": report_content
    })
    print(f"   {'✓' if word_result['success'] else '✗'} {word_result.get('message', word_result.get('error'))}")
    
    # Create PDF version
    print("\n3. Creating PDF document...")
    pdf_result = doc_tool.execute({
        "action": "create",
        "format": "pdf",
        "filename": "graive_technical_analysis.pdf",
        "content": report_content
    })
    print(f"   {'✓' if pdf_result['success'] else '✗'} {pdf_result.get('message', pdf_result.get('error'))}")
    
    # Create presentation
    print("\n4. Creating PowerPoint presentation...")
    ppt_content = {
        "slides": [
            {
                "type": "title",
                "title": "Graive AI Technical Analysis",
                "subtitle": "Autonomous General Intelligence Platform"
            },
            {
                "type": "content",
                "title": "Architecture Components",
                "points": [
                    "Unified Agent Loop - Central reasoning engine",
                    "Multi-Provider LLM Support - OpenAI, DeepSeek, Gemini",
                    "Tool Orchestrator - Dynamic tool management",
                    "Context Manager - Persistent state and memory",
                    "Document Tools - Comprehensive format support"
                ]
            },
            {
                "type": "content",
                "title": "Key Advantages",
                "points": [
                    "Simplified architecture vs multi-agent systems",
                    "Flexible LLM backend selection",
                    "Extensive document processing capabilities",
                    "Robust state management and audit trails",
                    "Extensible tool-based design"
                ]
            }
        ]
    }
    
    ppt_result = doc_tool.execute({
        "action": "create",
        "format": "powerpoint",
        "filename": "graive_technical_analysis.pptx",
        "content": ppt_content
    })
    print(f"   {'✓' if ppt_result['success'] else '✗'} {ppt_result.get('message', ppt_result.get('error'))}")
    
    # Read back the Markdown file
    print("\n5. Reading Markdown document...")
    read_result = doc_tool.execute({
        "action": "read",
        "format": "markdown",
        "filename": "graive_technical_analysis.md"
    })
    
    if read_result['success']:
        print("   ✓ Document read successfully")
        content = read_result['content']
        print(f"   Content length: {len(content)} characters")
        print(f"   Preview: {content[:150]}...")
    else:
        print(f"   ✗ {read_result.get('error')}")
    
    print("\n" + "=" * 70)
    print("Integration Demo Complete")
    print("\nGenerated files:")
    print("  • graive_technical_analysis.md (Markdown)")
    print("  • graive_technical_analysis.docx (Word)")
    print("  • graive_technical_analysis.pdf (PDF)")
    print("  • graive_technical_analysis.pptx (PowerPoint)")
    print("=" * 70)


def demonstrate_llm_integration():
    """
    Demonstrate LLM provider integration.
    
    Shows how to configure and use different providers.
    """
    print("\n" + "=" * 70)
    print("LLM Provider Integration")
    print("=" * 70)
    
    providers = LLMProviderFactory.get_available_providers()
    print(f"\nRegistered providers: {', '.join(providers)}")
    
    print("\nConfiguration:")
    print("  Set environment variables for API keys:")
    print("    OPENAI_API_KEY - For OpenAI GPT models")
    print("    DEEPSEEK_API_KEY - For DeepSeek models")
    print("    GEMINI_API_KEY - For Google Gemini models")
    
    print("\n" + "=" * 70)


def main():
    """Run the complete integration demonstration."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "GRAIVE AI INTEGRATION DEMO" + " " * 23 + "║")
    print("║" + " " * 14 + "Autonomous General Intelligence Platform" + " " * 14 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Demonstrate document creation
    create_research_report()
    
    # Demonstrate LLM integration
    demonstrate_llm_integration()
    
    print("\nFor more examples, see:")
    print("  • examples/llm_providers_demo.py - LLM provider usage")
    print("  • examples/document_demo.py - Document tool capabilities")
    print("  • examples/basic_usage.py - Basic agent setup")
    print()


if __name__ == "__main__":
    main()
