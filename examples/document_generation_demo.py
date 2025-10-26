"""
Complete Example: Generating a PhD Thesis with Document Orchestration System

This example demonstrates the full workflow for generating an ultra-long document
(200,000+ word thesis) using the document orchestration system with specialized
agents, intelligent element placement, and parallel execution.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.llm_provider_factory import LLMProviderFactory
from src.tools.tool_orchestrator import ToolOrchestrator
from src.planning.document_orchestrator import DocumentOrchestrator, InteractiveDocumentOrchestrator


def example_thesis_generation():
    """
    Example: Generate a complete PhD thesis (200,000 words) on AI and Healthcare.
    
    This demonstrates:
    - Intelligent planning with section decomposition
    - Parallel execution with specialized agents
    - Dynamic code generation for analysis
    - Intelligent element placement
    - Document assembly and export
    """
    print("=" * 80)
    print("EXAMPLE: Generating PhD Thesis with Document Orchestration")
    print("=" * 80)
    
    # Initialize LLM provider
    llm_provider = LLMProviderFactory.create_provider(
        provider_name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
        model="gpt-4"
    )
    
    # Initialize tool orchestrator
    tool_orchestrator = ToolOrchestrator()
    
    # Create sandbox directory
    sandbox_path = os.path.join(os.getcwd(), "thesis_sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    # Initialize orchestrator
    orchestrator = DocumentOrchestrator(
        llm_provider=llm_provider,
        tool_orchestrator=tool_orchestrator,
        base_sandbox_path=sandbox_path
    )
    
    # Define thesis requirements
    requirements = {
        "total_word_count": 200000,  # 200,000 words
        "research_question": "How can artificial intelligence improve diagnostic accuracy and patient outcomes in healthcare?",
        "methodology": "Mixed-methods approach combining systematic literature review, quantitative analysis of clinical data, and case studies of AI implementation in hospitals",
        "key_findings": [
            "AI-assisted diagnosis improves accuracy by 23%",
            "Machine learning models reduce diagnostic time by 40%",
            "Implementation challenges include data quality and clinician trust"
        ],
        "deadline": "2024-12-31",
        "output_format": "markdown",  # or "latex", "docx", "pdf"
        "citation_style": "apa",
        "style_preferences": {
            "line_spacing": 2.0,
            "font_size": 12,
            "heading_numbering": True
        },
        "terminology": {
            "AI": "Artificial Intelligence",
            "ML": "Machine Learning",
            "DL": "Deep Learning",
            "EHR": "Electronic Health Record"
        }
    }
    
    # Generate document with parallel execution
    print("\nStarting thesis generation...")
    print(f"Target: {requirements['total_word_count']:,} words")
    print(f"Research Question: {requirements['research_question']}")
    print(f"Methodology: {requirements['methodology'][:100]}...")
    
    result = orchestrator.generate_document(
        document_type="thesis",
        title="AI-Enhanced Healthcare Diagnostics: Improving Accuracy and Patient Outcomes",
        requirements=requirements,
        parallel_execution=True,
        max_workers=4  # Execute up to 4 sections in parallel
    )
    
    # Display results
    print("\n" + "=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    
    print(f"\nDocument Statistics:")
    print(f"  Total Sections: {result['metadata']['total_sections']}")
    print(f"  Sections Executed: {result['metadata']['sections_executed']}")
    print(f"  Total Word Count: {result['metadata']['total_word_count']:,}")
    print(f"  Execution Mode: {result['metadata']['execution_mode']}")
    print(f"  Output File: {result['file_path']}")
    
    print(f"\nSection Breakdown:")
    for section_output in result['section_outputs']:
        print(f"  - {section_output['section_id'][:8]}... : {section_output['word_count']:,} words")
    
    print(f"\nExecution Log:")
    for log_entry in result['metadata']['execution_log'][:5]:  # Show first 5
        status = "✓" if log_entry['success'] else "✗"
        print(f"  {status} {log_entry['section_title']}: {log_entry.get('execution_time_seconds', 'N/A')}s")
    
    return result


def example_interactive_thesis_generation():
    """
    Example: Interactive thesis generation with human-in-the-loop review.
    
    This demonstrates:
    - Plan review before execution
    - Section-by-section review and revision
    - User feedback integration
    - Modification during execution
    """
    print("=" * 80)
    print("EXAMPLE: Interactive Thesis Generation with Human Review")
    print("=" * 80)
    
    # Initialize components
    llm_provider = LLMProviderFactory.create_provider(
        provider_name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
        model="gpt-4"
    )
    
    tool_orchestrator = ToolOrchestrator()
    sandbox_path = os.path.join(os.getcwd(), "thesis_interactive_sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    # Initialize interactive orchestrator
    orchestrator = InteractiveDocumentOrchestrator(
        llm_provider=llm_provider,
        tool_orchestrator=tool_orchestrator,
        base_sandbox_path=sandbox_path
    )
    
    # Define review callback
    def review_callback(stage: str, data: Any) -> Dict[str, Any]:
        """
        Callback function for user review at different stages.
        
        In a real implementation, this would present UI for review and
        collect user input. Here we simulate approval.
        """
        print(f"\n>>> USER REVIEW POINT: {stage.upper()}")
        
        if stage == "plan":
            print(f"    Plan created with {len(data.sections)} sections")
            print(f"    Total target: {data.total_word_count:,} words")
            print("    Review options: approve, modify")
            
            # Simulate user approval
            return {"action": "approve"}
        
        elif stage == "section":
            print(f"    Section completed: {data['word_count']} words")
            print("    Review options: approve, revise, regenerate")
            
            # Simulate user approval
            return {"action": "approve"}
        
        elif stage == "final":
            word_count = len(data['content'].split())
            print(f"    Final document: {word_count:,} words")
            print("    Review options: approve, revise")
            
            # Simulate user approval
            return {"action": "approve"}
        
        return {"action": "approve"}
    
    # Requirements
    requirements = {
        "total_word_count": 150000,
        "research_question": "What are the ethical implications of AI in medical decision-making?",
        "methodology": "Qualitative analysis of ethical frameworks and case studies",
        "output_format": "markdown",
        "citation_style": "apa"
    }
    
    # Generate with interaction
    result = orchestrator.generate_document_interactive(
        document_type="thesis",
        title="Ethical AI in Medical Decision-Making",
        requirements=requirements,
        review_callback=review_callback
    )
    
    print("\n" + "=" * 80)
    print("INTERACTIVE GENERATION COMPLETE")
    print("=" * 80)
    print(f"User Feedback Points: {len(result['user_feedback'])}")
    print(f"Output File: {result['file_path']}")
    
    return result


def example_research_paper_generation():
    """
    Example: Generate a research paper (8,000 words) with data analysis.
    
    This demonstrates:
    - Shorter document generation
    - Data analysis agent generating Python code
    - Statistical analysis and visualizations
    - Table and figure placement
    """
    print("=" * 80)
    print("EXAMPLE: Generating Research Paper with Data Analysis")
    print("=" * 80)
    
    # Initialize components
    llm_provider = LLMProviderFactory.create_provider(
        provider_name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
        model="gpt-4"
    )
    
    tool_orchestrator = ToolOrchestrator()
    sandbox_path = os.path.join(os.getcwd(), "paper_sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    orchestrator = DocumentOrchestrator(
        llm_provider=llm_provider,
        tool_orchestrator=tool_orchestrator,
        base_sandbox_path=sandbox_path
    )
    
    # Requirements for research paper
    requirements = {
        "total_word_count": 8000,
        "research_question": "Does AI-assisted triage reduce emergency department wait times?",
        "methodology": "Retrospective analysis of ED data before and after AI implementation",
        "key_findings": [
            "Average wait time reduced by 32 minutes (p < 0.001)",
            "Triage accuracy improved by 15%",
            "Patient satisfaction increased by 12 points"
        ],
        "output_format": "latex",
        "citation_style": "ieee"
    }
    
    result = orchestrator.generate_document(
        document_type="paper",
        title="Impact of AI-Assisted Triage on Emergency Department Efficiency",
        requirements=requirements,
        parallel_execution=True,
        max_workers=3
    )
    
    print("\n" + "=" * 80)
    print("PAPER GENERATION COMPLETE")
    print("=" * 80)
    print(f"Total Word Count: {result['metadata']['total_word_count']:,}")
    print(f"Output File: {result['file_path']}")
    
    # Show generated analysis files
    print("\nGenerated Analysis Files:")
    for section in result['section_outputs']:
        if section.get('generated_files'):
            for file_path in section['generated_files']:
                print(f"  - {file_path}")
    
    return result


def example_book_generation():
    """
    Example: Generate a technical book (100,000 words) with multiple chapters.
    
    This demonstrates:
    - Multi-chapter structure
    - Cross-chapter consistency
    - Code examples generation
    - Comprehensive documentation
    """
    print("=" * 80)
    print("EXAMPLE: Generating Technical Book")
    print("=" * 80)
    
    llm_provider = LLMProviderFactory.create_provider(
        provider_name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
        model="gpt-4"
    )
    
    tool_orchestrator = ToolOrchestrator()
    sandbox_path = os.path.join(os.getcwd(), "book_sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    orchestrator = DocumentOrchestrator(
        llm_provider=llm_provider,
        tool_orchestrator=tool_orchestrator,
        base_sandbox_path=sandbox_path
    )
    
    requirements = {
        "total_word_count": 100000,
        "research_question": "How to build production-ready AI systems?",
        "methodology": "Tutorial-based approach with practical examples",
        "output_format": "markdown",
        "citation_style": "apa",
        "key_topics": [
            "AI System Architecture",
            "Data Pipeline Design",
            "Model Training and Evaluation",
            "Deployment Strategies",
            "Monitoring and Maintenance",
            "Ethics and Governance"
        ]
    }
    
    result = orchestrator.generate_document(
        document_type="book",
        title="Building Production AI Systems: A Practical Guide",
        requirements=requirements,
        parallel_execution=True,
        max_workers=6
    )
    
    print("\n" + "=" * 80)
    print("BOOK GENERATION COMPLETE")
    print("=" * 80)
    print(f"Total Word Count: {result['metadata']['total_word_count']:,}")
    print(f"Chapters: {result['metadata']['total_sections']}")
    print(f"Output File: {result['file_path']}")
    
    return result


def example_custom_document():
    """
    Example: Generate custom document with specific section requirements.
    
    This demonstrates:
    - Custom section definitions
    - Specific agent assignments
    - Custom element placement rules
    - Tailored style guides
    """
    print("=" * 80)
    print("EXAMPLE: Custom Document with Specific Requirements")
    print("=" * 80)
    
    # This example shows how to customize the generation process
    # for unique document types not covered by standard templates
    
    llm_provider = LLMProviderFactory.create_provider(
        provider_name="deepseek",  # Using different provider
        api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key"),
        model="deepseek-chat"
    )
    
    tool_orchestrator = ToolOrchestrator()
    sandbox_path = os.path.join(os.getcwd(), "custom_sandbox")
    os.makedirs(sandbox_path, exist_ok=True)
    
    orchestrator = DocumentOrchestrator(
        llm_provider=llm_provider,
        tool_orchestrator=tool_orchestrator,
        base_sandbox_path=sandbox_path
    )
    
    # Custom requirements
    requirements = {
        "total_word_count": 50000,
        "research_question": "Market analysis and strategic recommendations for AI startup",
        "methodology": "Mixed qualitative and quantitative analysis",
        "output_format": "docx",
        "citation_style": "chicago",
        "style_preferences": {
            "executive_summary": True,
            "appendices": ["Financial Projections", "Market Data", "Technical Specifications"],
            "confidential": True
        }
    }
    
    result = orchestrator.generate_document(
        document_type="report",
        title="AI Healthcare Platform: Market Analysis and Strategic Plan 2024-2029",
        requirements=requirements,
        parallel_execution=True,
        max_workers=4
    )
    
    print("\n" + "=" * 80)
    print("CUSTOM DOCUMENT COMPLETE")
    print("=" * 80)
    print(f"Output File: {result['file_path']}")
    
    return result


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" DOCUMENT ORCHESTRATION SYSTEM - COMPREHENSIVE EXAMPLES")
    print("=" * 80)
    print("\nThis demonstrates the complete workflow for generating ultra-long")
    print("documents with intelligent planning, specialized agents, and parallel")
    print("execution.")
    print("\n" + "=" * 80)
    
    # Choose example to run
    print("\nAvailable Examples:")
    print("  1. PhD Thesis Generation (200,000 words)")
    print("  2. Interactive Thesis with Human Review")
    print("  3. Research Paper with Data Analysis (8,000 words)")
    print("  4. Technical Book (100,000 words)")
    print("  5. Custom Business Report (50,000 words)")
    print("  6. Run all examples")
    
    choice = input("\nSelect example (1-6): ").strip()
    
    if choice == "1":
        example_thesis_generation()
    elif choice == "2":
        example_interactive_thesis_generation()
    elif choice == "3":
        example_research_paper_generation()
    elif choice == "4":
        example_book_generation()
    elif choice == "5":
        example_custom_document()
    elif choice == "6":
        print("\nRunning all examples...\n")
        example_thesis_generation()
        print("\n")
        example_interactive_thesis_generation()
        print("\n")
        example_research_paper_generation()
        print("\n")
        example_book_generation()
        print("\n")
        example_custom_document()
    else:
        print("\nDefaulting to PhD Thesis example...")
        example_thesis_generation()
    
    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80)
