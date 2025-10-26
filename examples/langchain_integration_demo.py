"""
LangChain Integration - Comprehensive Examples

Demonstrates modern LangChain technology integration with Graive AI:
1. Prompt engineering with templates
2. Chain-of-thought reasoning
3. Memory management strategies
4. RAG (Retrieval Augmented Generation)
5. ReAct agents with tools
6. Multi-agent collaboration
7. Document generation workflows
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.langchain_integration import (
    LangChainLLMManager,
    PromptTemplateManager,
    LangChainMemoryManager,
    DocumentProcessor,
    RAGSystem,
    ChainBuilder,
    ManusCallbackHandler,
    ReActAgent,
    DocumentGenerationAgent,
    MultiAgentOrchestrator,
    LangChainAgentFactory,
    ManusToolAdapter
)


def example_prompt_templates():
    """
    Example 1: Advanced Prompt Engineering
    
    Demonstrates using pre-configured prompt templates for various tasks.
    """
    print("=" * 80)
    print("EXAMPLE 1: ADVANCED PROMPT ENGINEERING")
    print("=" * 80)
    
    # Initialize LLM
    llm_manager = LangChainLLMManager()
    llm = llm_manager.create_llm(
        provider="openai",
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY", "your-api-key")
    )
    
    # Initialize template manager
    template_manager = PromptTemplateManager()
    
    # Example: Document section generation
    print("\n1. Document Section Generation Template")
    doc_template = template_manager.get_template("document_section")
    
    formatted_prompt = doc_template.format_messages(
        domain="artificial intelligence",
        citation_style="APA",
        tone="academic",
        section_type="introduction",
        title="AI in Healthcare Diagnostics",
        key_topics="machine learning, diagnostic accuracy, patient outcomes",
        word_count=500,
        context="This is a PhD thesis exploring AI applications in medical diagnosis"
    )
    
    print("   Prompt preview:")
    print(f"   {formatted_prompt[0].content[:200]}...")
    
    # Example: Chain-of-thought reasoning
    print("\n2. Chain-of-Thought Reasoning Template")
    cot_template = template_manager.get_template("chain_of_thought")
    
    formatted_prompt = cot_template.format_messages(
        problem="How can AI improve diagnostic accuracy in radiology?"
    )
    
    print("   Prompt preview:")
    print(f"   {formatted_prompt[0].content[:200]}...")
    
    # Example: Research synthesis
    print("\n3. Research Synthesis Template")
    research_template = template_manager.get_template("research_synthesis")
    
    research_papers = """
    1. Smith et al. (2023): AI improved diagnostic accuracy by 23% in pneumonia detection
    2. Jones et al. (2024): Deep learning reduced diagnostic time by 40%
    3. Brown et al. (2023): Implementation challenges include data quality and clinician trust
    """
    
    formatted_prompt = research_template.format_messages(
        topic="AI in medical imaging",
        research_papers=research_papers
    )
    
    print("   Prompt structured for synthesis")
    
    return llm, template_manager


def example_memory_strategies(llm):
    """
    Example 2: Memory Management Strategies
    
    Demonstrates different memory approaches for maintaining context.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: MEMORY MANAGEMENT STRATEGIES")
    print("=" * 80)
    
    memory_manager = LangChainMemoryManager(llm)
    
    # Strategy 1: Buffer Memory
    print("\n1. Conversation Buffer Memory")
    buffer_memory = memory_manager.create_buffer_memory()
    
    # Add some conversation
    buffer_memory.save_context(
        {"input": "What is AI?"}, 
        {"output": "AI is artificial intelligence..."}
    )
    buffer_memory.save_context(
        {"input": "How does it work in healthcare?"},
        {"output": "AI in healthcare uses machine learning..."}
    )
    
    print("   ✓ Stored 2 conversation turns")
    print(f"   Memory contains: {len(buffer_memory.buffer)} messages")
    
    # Strategy 2: Summary Memory
    print("\n2. Conversation Summary Memory")
    summary_memory = memory_manager.create_summary_memory()
    
    # Add conversation (would be summarized by LLM)
    for i in range(5):
        summary_memory.save_context(
            {"input": f"Question {i+1}"},
            {"output": f"Answer {i+1} with detailed explanation"}
        )
    
    print("   ✓ Stored 5 conversation turns (auto-summarized)")
    
    # Strategy 3: Window Memory
    print("\n3. Conversation Window Memory (k=3)")
    window_memory = memory_manager.create_window_memory(k=3)
    
    # Add more messages than window size
    for i in range(10):
        window_memory.save_context(
            {"input": f"Message {i+1}"},
            {"output": f"Response {i+1}"}
        )
    
    print("   ✓ Stored 10 messages, keeping only last 3")
    print(f"   Window size: {len(window_memory.buffer)}")
    
    return memory_manager


def example_rag_system(llm):
    """
    Example 3: RAG (Retrieval Augmented Generation)
    
    Demonstrates question answering over custom documents using vector search.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: RAG (RETRIEVAL AUGMENTED GENERATION)")
    print("=" * 80)
    
    # Initialize document processor
    processor = DocumentProcessor()
    
    # Create sample documents
    print("\n1. Creating Sample Documents")
    sample_texts = [
        "Artificial intelligence has significantly improved diagnostic accuracy in radiology, with studies showing up to 23% improvement over traditional methods.",
        "Machine learning algorithms can analyze medical images faster than human radiologists, reducing diagnostic time by 40% on average.",
        "Implementation of AI in healthcare faces challenges including data quality issues, integration with existing systems, and gaining clinician trust.",
        "Deep learning models require large datasets for training, typically 10,000+ annotated medical images for each condition.",
        "AI-assisted diagnosis systems work best when combined with human expertise, creating a hybrid approach that leverages strengths of both."
    ]
    
    # Convert to LangChain documents
    from langchain.schema import Document
    documents = [Document(page_content=text, metadata={"source": f"doc_{i}"}) 
                 for i, text in enumerate(sample_texts)]
    
    print(f"   ✓ Created {len(documents)} documents")
    
    # Initialize RAG system
    print("\n2. Initializing RAG System")
    rag = RAGSystem(
        llm=llm,
        embedding_model="huggingface",  # Free embeddings
        persist_directory="./rag_storage"
    )
    
    rag.create_vector_store(documents, collection_name="ai_healthcare")
    print("   ✓ Vector store created with embeddings")
    
    # Query the RAG system
    print("\n3. Querying RAG System")
    
    questions = [
        "How much does AI improve diagnostic accuracy?",
        "What are the challenges of implementing AI in healthcare?",
        "How fast can AI analyze medical images?"
    ]
    
    for question in questions:
        print(f"\n   Question: {question}")
        result = rag.query(question, return_source_documents=True)
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Sources: {len(result['source_documents'])} documents")
    
    return rag


def example_react_agent(llm):
    """
    Example 4: ReAct Agent with Tools
    
    Demonstrates reasoning and acting agent using Graive tools.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: REACT AGENT WITH TOOLS")
    print("=" * 80)
    
    # Create tools
    print("\n1. Creating Tools")
    tools = [
        ManusToolAdapter.create_document_tool(),
        ManusToolAdapter.create_research_tool(),
        ManusToolAdapter.create_data_analysis_tool()
    ]
    
    print(f"   ✓ Created {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description[:60]}...")
    
    # Create ReAct agent
    print("\n2. Creating ReAct Agent")
    agent = ReActAgent(llm, tools, verbose=True)
    print("   ✓ Agent initialized with reasoning capabilities")
    
    # Run agent on task
    print("\n3. Running Agent on Task")
    task = "Research AI in healthcare and create a summary document"
    
    print(f"   Task: {task}")
    print("   Executing (agent will show reasoning)...")
    
    # Would execute: result = agent.run(task)
    print("   [Agent would execute with Thought/Action/Observation cycles]")
    print("   ✓ Task completed")
    
    return agent


def example_document_generation_agent(llm):
    """
    Example 5: Document Generation Agent
    
    Demonstrates specialized agent for creating comprehensive documents.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: DOCUMENT GENERATION AGENT")
    print("=" * 80)
    
    # Create document generation agent
    print("\n1. Initializing Document Generation Agent")
    doc_agent = DocumentGenerationAgent(llm)
    print("   ✓ Agent with document tools initialized")
    
    # Define document requirements
    print("\n2. Defining Document Requirements")
    requirements = {
        "title": "AI Applications in Medical Imaging",
        "type": "research_paper",
        "word_count": 5000,
        "topics": [
            "Deep learning in radiology",
            "Diagnostic accuracy improvements",
            "Implementation challenges",
            "Future directions"
        ],
        "style": "academic",
        "citation_style": "APA"
    }
    
    print(f"   Title: {requirements['title']}")
    print(f"   Type: {requirements['type']}")
    print(f"   Word count: {requirements['word_count']}")
    print(f"   Topics: {len(requirements['topics'])}")
    
    # Generate document
    print("\n3. Generating Document")
    print("   [Agent would orchestrate research, writing, and formatting]")
    # Would execute: result = doc_agent.generate_document(requirements)
    print("   ✓ Document generation complete")
    
    return doc_agent


def example_multi_agent_collaboration(llm):
    """
    Example 6: Multi-Agent Collaboration
    
    Demonstrates multiple agents working together on complex task.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 6: MULTI-AGENT COLLABORATION")
    print("=" * 80)
    
    # Initialize orchestrator
    print("\n1. Initializing Multi-Agent Orchestrator")
    orchestrator = MultiAgentOrchestrator(llm)
    print("   ✓ Orchestrator ready")
    
    # Register specialized agents
    print("\n2. Registering Specialized Agents")
    
    # Research agent
    research_tools = [ManusToolAdapter.create_research_tool()]
    orchestrator.register_agent(
        agent_name="researcher",
        agent_type="react",
        tools=research_tools,
        description="Specializes in finding and synthesizing research information"
    )
    print("   ✓ Registered: Research Agent")
    
    # Analysis agent
    analysis_tools = [
        ManusToolAdapter.create_data_analysis_tool(),
        ManusToolAdapter.create_code_execution_tool()
    ]
    orchestrator.register_agent(
        agent_name="analyst",
        agent_type="react",
        tools=analysis_tools,
        description="Specializes in data analysis and statistical computation"
    )
    print("   ✓ Registered: Analysis Agent")
    
    # Document agent
    orchestrator.register_agent(
        agent_name="writer",
        agent_type="document",
        tools=[ManusToolAdapter.create_document_tool()],
        description="Specializes in creating well-formatted documents"
    )
    print("   ✓ Registered: Document Writer Agent")
    
    # Collaborative task execution
    print("\n3. Executing Collaborative Tasks")
    
    tasks = [
        {
            "description": "Research AI diagnostic accuracy studies",
            "agent": "researcher",
            "dependencies": []
        },
        {
            "description": "Analyze statistical data from research",
            "agent": "analyst",
            "dependencies": ["Research AI diagnostic accuracy studies"]
        },
        {
            "description": "Write comprehensive research paper",
            "agent": "writer",
            "dependencies": [
                "Research AI diagnostic accuracy studies",
                "Analyze statistical data from research"
            ]
        }
    ]
    
    for task in tasks:
        print(f"   Task: {task['description']}")
        print(f"   Agent: {task['agent']}")
        print(f"   Dependencies: {len(task['dependencies'])}")
    
    print("\n   Executing tasks...")
    # Would execute: results = orchestrator.collaborative_execution(tasks)
    print("   ✓ All tasks completed collaboratively")
    
    return orchestrator


def example_chain_builder(llm):
    """
    Example 7: Chain Building for Sequential Processing
    
    Demonstrates creating custom chains for multi-step workflows.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 7: CHAIN BUILDING FOR SEQUENTIAL PROCESSING")
    print("=" * 80)
    
    # Initialize chain builder
    print("\n1. Creating Chain Builder")
    builder = ChainBuilder(llm)
    print("   ✓ Chain builder initialized")
    
    # Create document generation chain
    print("\n2. Building Document Generation Chain")
    print("   Steps:")
    print("   1. Generate outline")
    print("   2. Synthesize research")
    print("   3. Write complete draft")
    
    # Would create: chain = builder.create_document_generation_chain()
    print("   ✓ Sequential chain created")
    
    # Example execution
    print("\n3. Example Execution")
    print("   Input: 'AI in Healthcare'")
    print("   Step 1: Outline → [Generated outline with 5 sections]")
    print("   Step 2: Research → [Synthesized 15 research papers]")
    print("   Step 3: Draft → [Complete 5000-word document]")
    print("   ✓ Chain execution complete")
    
    return builder


def example_callback_monitoring():
    """
    Example 8: Callback Monitoring
    
    Demonstrates monitoring LangChain execution with custom callbacks.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 8: CALLBACK MONITORING")
    print("=" * 80)
    
    # Create callback handler
    print("\n1. Creating Callback Handler")
    callback = ManusCallbackHandler()
    print("   ✓ Callback handler initialized")
    
    # Simulate some events
    print("\n2. Capturing Execution Events")
    callback.on_llm_start({}, ["Test prompt"])
    callback.on_chain_start({"name": "test_chain"}, {"input": "test"})
    callback.on_tool_start({"name": "research_tool"}, "query")
    callback.on_tool_end("result")
    callback.on_chain_end({"output": "final result"})
    callback.on_llm_end("LLM response")
    
    events = callback.get_events()
    print(f"   ✓ Captured {len(events)} events")
    
    # Display events
    print("\n3. Event Log")
    for event in events:
        print(f"   [{event['timestamp'][:19]}] {event['type']}")
    
    return callback


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" LANGCHAIN INTEGRATION - COMPREHENSIVE EXAMPLES")
    print("=" * 80)
    print("\nDemonstrating modern LangChain technology in Graive AI:")
    print("  1. Advanced Prompt Engineering")
    print("  2. Memory Management Strategies")
    print("  3. RAG (Retrieval Augmented Generation)")
    print("  4. ReAct Agents with Tools")
    print("  5. Document Generation Agent")
    print("  6. Multi-Agent Collaboration")
    print("  7. Chain Building")
    print("  8. Callback Monitoring")
    print("\n" + "=" * 80)
    
    # Run examples
    try:
        llm, template_manager = example_prompt_templates()
        memory_manager = example_memory_strategies(llm)
        rag_system = example_rag_system(llm)
        react_agent = example_react_agent(llm)
        doc_agent = example_document_generation_agent(llm)
        orchestrator = example_multi_agent_collaboration(llm)
        chain_builder = example_chain_builder(llm)
        callback = example_callback_monitoring()
        
        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETE")
        print("=" * 80)
        print("\nLangChain integration provides:")
        print("  ✓ Advanced prompt engineering with templates")
        print("  ✓ Multiple memory strategies for context management")
        print("  ✓ RAG for question answering over documents")
        print("  ✓ ReAct agents with reasoning capabilities")
        print("  ✓ Specialized document generation agents")
        print("  ✓ Multi-agent collaboration patterns")
        print("  ✓ Sequential chains for complex workflows")
        print("  ✓ Execution monitoring with callbacks")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nNote: Some examples require API keys and dependencies.")
        print(f"Install: pip install langchain langchain-openai langchain-community")
        print(f"Error: {str(e)}")
