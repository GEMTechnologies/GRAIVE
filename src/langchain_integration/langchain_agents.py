"""
LangChain Agent Integration - Modern Agent Patterns

This module integrates LangChain agents with Graive AI tools, providing:
- ReAct (Reasoning and Acting) agents
- Structured chat agents with tool use
- Custom agent types for document generation
- Multi-agent collaboration
- Tool conversion from Graive to LangChain format
"""

from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime

from langchain.agents import (
    AgentExecutor,
    create_structured_chat_agent,
    create_react_agent,
    Tool as LangChainTool
)
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field


class ManusToolAdapter:
    """
    Adapts Graive AI tools to LangChain Tool format.
    
    Converts Graive tool interface to LangChain-compatible tools
    for use in LangChain agents.
    """
    
    @staticmethod
    def convert_to_langchain_tool(
        tool_name: str,
        tool_description: str,
        tool_function: Callable,
        args_schema: Optional[type] = None
    ) -> LangChainTool:
        """
        Convert Graive tool to LangChain Tool.
        
        Args:
            tool_name: Name of the tool
            tool_description: Description of what the tool does
            tool_function: Function to execute
            args_schema: Optional Pydantic schema for arguments
        
        Returns:
            LangChain Tool instance
        """
        if args_schema:
            return StructuredTool(
                name=tool_name,
                description=tool_description,
                func=tool_function,
                args_schema=args_schema
            )
        else:
            return LangChainTool(
                name=tool_name,
                description=tool_description,
                func=tool_function
            )
    
    @staticmethod
    def create_document_tool() -> LangChainTool:
        """Create LangChain tool for document operations."""
        
        def document_operation(action: str, **kwargs) -> str:
            """Execute document operation."""
            # This would call actual Graive document tool
            if action == "create":
                return f"Created document: {kwargs.get('filename')}"
            elif action == "read":
                return f"Read document: {kwargs.get('filename')}"
            return f"Executed {action}"
        
        return LangChainTool(
            name="document_tool",
            description="Create, read, edit, and convert documents in various formats (MD, DOCX, PDF, PPTX)",
            func=lambda x: document_operation(**eval(x) if isinstance(x, str) else x)
        )
    
    @staticmethod
    def create_research_tool() -> LangChainTool:
        """Create LangChain tool for research operations."""
        
        def research_operation(query: str) -> str:
            """Execute research query."""
            # This would call actual Graive web scraping/search tools
            return f"Research results for: {query}"
        
        return LangChainTool(
            name="research_tool",
            description="Search academic databases, scrape websites, and gather research information",
            func=research_operation
        )
    
    @staticmethod
    def create_data_analysis_tool() -> LangChainTool:
        """Create LangChain tool for data analysis."""
        
        def analyze_data(data_description: str) -> str:
            """Execute data analysis."""
            # This would call actual Graive data analysis tool
            return f"Analysis results for: {data_description}"
        
        return LangChainTool(
            name="data_analysis_tool",
            description="Perform statistical analysis, create visualizations, and generate insights from data",
            func=analyze_data
        )
    
    @staticmethod
    def create_code_execution_tool() -> LangChainTool:
        """Create LangChain tool for code execution."""
        
        def execute_code(code: str, language: str = "python") -> str:
            """Execute code in sandbox."""
            # This would call actual Graive code execution
            return f"Executed {language} code"
        
        return LangChainTool(
            name="code_execution_tool",
            description="Execute Python code in sandboxed environment for analysis and computation",
            func=lambda x: execute_code(x)
        )


class ReActAgent:
    """
    ReAct (Reasoning and Acting) agent using LangChain.
    
    Combines reasoning traces and task-specific actions in an interleaved manner,
    allowing for greater synergy between the two.
    """
    
    def __init__(
        self,
        llm: Any,
        tools: List[LangChainTool],
        verbose: bool = True
    ):
        """
        Initialize ReAct agent.
        
        Args:
            llm: LangChain LLM instance
            tools: List of available tools
            verbose: Whether to print reasoning steps
        """
        self.llm = llm
        self.tools = tools
        self.verbose = verbose
        
        # Create ReAct prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are a helpful AI assistant with access to various tools. "
                "Use the following format:\n\n"
                "Thought: Consider what to do\n"
                "Action: Choose a tool to use\n"
                "Action Input: Input for the tool\n"
                "Observation: Result from the tool\n"
                "... (repeat Thought/Action/Observation as needed)\n"
                "Thought: I now know the final answer\n"
                "Final Answer: The final answer to the user\n\n"
                "Available tools: {tools}"
            )),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}")
        ])
        
        # Create agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create executor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=15
        )
    
    def run(
        self,
        query: str,
        chat_history: Optional[List] = None
    ) -> Dict[str, Any]:
        """
        Run agent on query.
        
        Args:
            query: User query
            chat_history: Optional conversation history
        
        Returns:
            Agent response with reasoning trace
        """
        result = self.executor.invoke({
            "input": query,
            "chat_history": chat_history or []
        })
        
        return result


class DocumentGenerationAgent:
    """
    Specialized agent for document generation using LangChain.
    
    Coordinates multiple tools and reasoning steps to generate
    high-quality documents with research, analysis, and formatting.
    """
    
    def __init__(
        self,
        llm: Any,
        storage_manager: Optional[Any] = None
    ):
        """
        Initialize document generation agent.
        
        Args:
            llm: LangChain LLM instance
            storage_manager: Optional storage manager for persistence
        """
        self.llm = llm
        self.storage_manager = storage_manager
        
        # Create specialized tools
        self.tools = [
            ManusToolAdapter.create_document_tool(),
            ManusToolAdapter.create_research_tool(),
            ManusToolAdapter.create_data_analysis_tool(),
            ManusToolAdapter.create_code_execution_tool()
        ]
        
        # Create structured chat agent
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are an expert document generation agent. Your task is to create "
                "comprehensive, well-researched documents by:\n"
                "1. Planning the document structure\n"
                "2. Gathering necessary research and data\n"
                "3. Generating high-quality content\n"
                "4. Formatting and finalizing the document\n\n"
                "You have access to tools for document creation, research, "
                "data analysis, and code execution. Use them strategically "
                "to produce the best possible output."
            )),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=20
        )
    
    def generate_document(
        self,
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate document based on requirements.
        
        Args:
            requirements: Document requirements including:
                - title: Document title
                - type: Document type (thesis, paper, report)
                - word_count: Target word count
                - topics: Key topics to cover
                - style: Writing style
        
        Returns:
            Generated document and metadata
        """
        # Create detailed prompt from requirements
        prompt = self._create_generation_prompt(requirements)
        
        # Execute agent
        result = self.executor.invoke({
            "input": prompt,
            "chat_history": []
        })
        
        # Store result if storage manager available
        if self.storage_manager:
            self._store_result(result, requirements)
        
        return result
    
    def _create_generation_prompt(self, requirements: Dict[str, Any]) -> str:
        """Create detailed generation prompt from requirements."""
        prompt = f"""Generate a {requirements.get('type', 'document')} with the following specifications:

Title: {requirements.get('title', 'Untitled')}
Word Count: {requirements.get('word_count', 5000)} words
Topics: {', '.join(requirements.get('topics', []))}
Style: {requirements.get('style', 'academic')}

Please:
1. Create a detailed outline
2. Research relevant information for each section
3. Write comprehensive content meeting the word count
4. Format professionally
5. Include citations where appropriate

Begin the generation process."""
        
        return prompt
    
    def _store_result(self, result: Dict[str, Any], requirements: Dict[str, Any]):
        """Store generation result in storage manager."""
        if self.storage_manager:
            self.storage_manager.store_context(
                key=f"document_{datetime.utcnow().isoformat()}",
                value={
                    "requirements": requirements,
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                },
                context_type="document_generation"
            )


class MultiAgentOrchestrator:
    """
    Orchestrates multiple LangChain agents for collaborative work.
    
    Enables:
    - Agent-to-agent communication
    - Task delegation
    - Parallel agent execution
    - Result synthesis
    """
    
    def __init__(self, llm: Any):
        """
        Initialize multi-agent orchestrator.
        
        Args:
            llm: LangChain LLM instance
        """
        self.llm = llm
        self.agents: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
    
    def register_agent(
        self,
        agent_name: str,
        agent_type: str,
        tools: List[LangChainTool],
        description: str
    ):
        """
        Register an agent with the orchestrator.
        
        Args:
            agent_name: Unique agent identifier
            agent_type: Type of agent (react, structured_chat, custom)
            tools: Tools available to the agent
            description: Agent's capabilities and role
        """
        if agent_type == "react":
            agent = ReActAgent(self.llm, tools)
        elif agent_type == "document":
            agent = DocumentGenerationAgent(self.llm)
        else:
            # Create custom structured chat agent
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=description),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content="{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            langchain_agent = create_structured_chat_agent(
                llm=self.llm,
                tools=tools,
                prompt=prompt
            )
            
            agent = AgentExecutor(
                agent=langchain_agent,
                tools=tools,
                verbose=True
            )
        
        self.agents[agent_name] = {
            "executor": agent,
            "type": agent_type,
            "description": description,
            "tools": tools
        }
    
    def delegate_task(
        self,
        task: str,
        preferred_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delegate task to appropriate agent.
        
        Args:
            task: Task description
            preferred_agent: Optional specific agent to use
        
        Returns:
            Task result from agent
        """
        # Select agent
        if preferred_agent and preferred_agent in self.agents:
            agent_name = preferred_agent
        else:
            # Auto-select based on task description
            agent_name = self._select_agent_for_task(task)
        
        # Execute task
        agent_info = self.agents[agent_name]
        
        if agent_info["type"] == "react":
            result = agent_info["executor"].run(task)
        elif agent_info["type"] == "document":
            # Parse task as document requirements
            requirements = self._parse_document_requirements(task)
            result = agent_info["executor"].generate_document(requirements)
        else:
            result = agent_info["executor"].invoke({"input": task})
        
        # Log execution
        self.execution_log.append({
            "task": task,
            "agent": agent_name,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result
        })
        
        return {
            "agent": agent_name,
            "result": result
        }
    
    def _select_agent_for_task(self, task: str) -> str:
        """Select most appropriate agent for task."""
        task_lower = task.lower()
        
        # Simple keyword-based selection
        if any(word in task_lower for word in ["document", "write", "generate", "thesis", "paper"]):
            # Prefer document generation agent
            for name, info in self.agents.items():
                if info["type"] == "document":
                    return name
        
        if any(word in task_lower for word in ["research", "find", "search", "analyze"]):
            # Prefer agents with research tools
            for name, info in self.agents.items():
                if any(t.name == "research_tool" for t in info["tools"]):
                    return name
        
        # Default to first available agent
        return list(self.agents.keys())[0]
    
    def _parse_document_requirements(self, task: str) -> Dict[str, Any]:
        """Parse task string into document requirements."""
        # Simplified parsing - would use LLM in production
        return {
            "title": "Generated Document",
            "type": "document",
            "word_count": 5000,
            "topics": [],
            "style": "professional"
        }
    
    def collaborative_execution(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple tasks across agents collaboratively.
        
        Args:
            tasks: List of task dictionaries with:
                - description: Task description
                - agent: Optional specific agent
                - dependencies: Optional task dependencies
        
        Returns:
            List of results from all tasks
        """
        results = []
        completed_tasks = set()
        
        for task in tasks:
            # Check dependencies
            dependencies = task.get("dependencies", [])
            if all(dep in completed_tasks for dep in dependencies):
                # Execute task
                result = self.delegate_task(
                    task["description"],
                    task.get("agent")
                )
                results.append(result)
                completed_tasks.add(task["description"])
        
        return results


class LangChainAgentFactory:
    """
    Factory for creating pre-configured LangChain agents.
    
    Provides quick creation of common agent types with
    appropriate tools and configurations.
    """
    
    @staticmethod
    def create_research_agent(llm: Any) -> ReActAgent:
        """Create agent specialized in research and information gathering."""
        tools = [
            ManusToolAdapter.create_research_tool(),
            ManusToolAdapter.create_document_tool()
        ]
        
        return ReActAgent(llm, tools, verbose=True)
    
    @staticmethod
    def create_analysis_agent(llm: Any) -> ReActAgent:
        """Create agent specialized in data analysis."""
        tools = [
            ManusToolAdapter.create_data_analysis_tool(),
            ManusToolAdapter.create_code_execution_tool()
        ]
        
        return ReActAgent(llm, tools, verbose=True)
    
    @staticmethod
    def create_document_agent(
        llm: Any,
        storage_manager: Optional[Any] = None
    ) -> DocumentGenerationAgent:
        """Create agent specialized in document generation."""
        return DocumentGenerationAgent(llm, storage_manager)
    
    @staticmethod
    def create_general_purpose_agent(llm: Any) -> ReActAgent:
        """Create general-purpose agent with all tools."""
        tools = [
            ManusToolAdapter.create_document_tool(),
            ManusToolAdapter.create_research_tool(),
            ManusToolAdapter.create_data_analysis_tool(),
            ManusToolAdapter.create_code_execution_tool()
        ]
        
        return ReActAgent(llm, tools, verbose=True)
