"""
Document Planning and Orchestration System

This package provides sophisticated document generation capabilities for ultra-long
documents (theses, books, comprehensive reports) through intelligent planning,
specialized agent coordination, and smart element placement.

Main Components:
- DocumentPlanner: Creates detailed execution plans from high-level requirements
- SpecializedAgents: Domain-expert agents for different section types
- DocumentAssembler: Intelligent element placement and document assembly
- DocumentOrchestrator: Coordinates entire generation workflow

Key Features:
- Hierarchical planning with dependency tracking
- Parallel execution of independent sections
- Dynamic Python code generation for analysis
- Smart table/figure placement (similar to Overleaf)
- Cross-reference management
- Human-in-the-loop capabilities
"""

from src.planning.document_planner import (
    DocumentPlanner,
    DocumentPlan,
    SectionPlan,
    DocumentElement,
    SectionType,
    AgentSpecialization,
    ElementType
)

from src.planning.specialized_agents import (
    SpecializedAgent,
    ResearchSynthesisAgent,
    DataAnalystAgent,
    MethodologyExpertAgent,
    DiscussionWriterAgent,
    TechnicalWriterAgent,
    AgentExecutionContext,
    SectionOutput
)

from src.planning.document_assembler import (
    DocumentAssembler,
    PlacedElement,
    PlacementStrategy,
    TextReference,
    ElementPlacementOptimizer
)

from src.planning.document_orchestrator import (
    DocumentOrchestrator,
    InteractiveDocumentOrchestrator
)

__all__ = [
    # Planning
    "DocumentPlanner",
    "DocumentPlan",
    "SectionPlan",
    "DocumentElement",
    "SectionType",
    "AgentSpecialization",
    "ElementType",
    
    # Agents
    "SpecializedAgent",
    "ResearchSynthesisAgent",
    "DataAnalystAgent",
    "MethodologyExpertAgent",
    "DiscussionWriterAgent",
    "TechnicalWriterAgent",
    "AgentExecutionContext",
    "SectionOutput",
    
    # Assembly
    "DocumentAssembler",
    "PlacedElement",
    "PlacementStrategy",
    "TextReference",
    "ElementPlacementOptimizer",
    
    # Orchestration
    "DocumentOrchestrator",
    "InteractiveDocumentOrchestrator"
]
