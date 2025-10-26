"""
LangChain Integration Module

Modern LangChain technology integration for Graive AI, providing:
- Advanced prompt engineering and templates
- Chain-of-thought reasoning chains
- Memory management (buffer, summary, vector store)
- ReAct and structured chat agents
- RAG (Retrieval Augmented Generation) systems
- Multi-agent collaboration
- Document processing and text splitting
"""

from src.langchain_integration.langchain_core import (
    LangChainLLMManager,
    PromptTemplateManager,
    LangChainMemoryManager,
    DocumentProcessor,
    RAGSystem,
    ChainBuilder,
    ManusCallbackHandler
)

from src.langchain_integration.langchain_agents import (
    ManusToolAdapter,
    ReActAgent,
    DocumentGenerationAgent,
    MultiAgentOrchestrator,
    LangChainAgentFactory
)

__all__ = [
    # Core Components
    "LangChainLLMManager",
    "PromptTemplateManager",
    "LangChainMemoryManager",
    "DocumentProcessor",
    "RAGSystem",
    "ChainBuilder",
    "ManusCallbackHandler",
    
    # Agent Components
    "ManusToolAdapter",
    "ReActAgent",
    "DocumentGenerationAgent",
    "MultiAgentOrchestrator",
    "LangChainAgentFactory"
]
