"""
LangChain Integration Core - Modern Chain-of-Thought and Agent Framework

This module integrates LangChain technology into Graive AI, providing:
- Advanced prompt engineering with templates
- Chain-of-thought reasoning chains
- Memory management (conversation buffer, summary, vector store)
- Tool integration with LangChain agents
- Document loaders and text splitters
- Vector store integration for RAG (Retrieval Augmented Generation)
- Multi-agent collaboration patterns
"""

from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import os

# LangChain Core
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate
)
from langchain.chains import (
    LLMChain,
    SequentialChain,
    TransformChain,
    ConversationChain
)
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
    VectorStoreRetrieverMemory
)
from langchain.agents import (
    AgentExecutor,
    create_structured_chat_agent,
    create_openai_tools_agent,
    Tool as LangChainTool
)
from langchain.schema import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage
)
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager

# LangChain LLM Integrations
from langchain_openai import ChatOpenAI, OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama

# Document Processing
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    CharacterTextSplitter
)
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader
)

# Vector Stores
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Output Parsers
from langchain.output_parsers import (
    StructuredOutputParser,
    PydanticOutputParser,
    CommaSeparatedListOutputParser
)


class ManusCallbackHandler(BaseCallbackHandler):
    """
    Custom callback handler for Graive AI integration.
    
    Captures LangChain execution events for logging, monitoring,
    and human-in-the-loop interaction.
    """
    
    def __init__(self):
        """Initialize callback handler."""
        self.events: List[Dict[str, Any]] = []
        self.current_chain: Optional[str] = None
        self.interrupt_requested = False
    
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs
    ) -> None:
        """Called when LLM starts running."""
        self.events.append({
            "type": "llm_start",
            "timestamp": datetime.utcnow().isoformat(),
            "prompts": prompts,
            "model": serialized.get("name", "unknown")
        })
    
    def on_llm_end(self, response: Any, **kwargs) -> None:
        """Called when LLM ends running."""
        self.events.append({
            "type": "llm_end",
            "timestamp": datetime.utcnow().isoformat(),
            "response": str(response)
        })
    
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs
    ) -> None:
        """Called when chain starts running."""
        chain_name = serialized.get("name", "unknown_chain")
        self.current_chain = chain_name
        
        self.events.append({
            "type": "chain_start",
            "timestamp": datetime.utcnow().isoformat(),
            "chain": chain_name,
            "inputs": inputs
        })
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain ends running."""
        self.events.append({
            "type": "chain_end",
            "timestamp": datetime.utcnow().isoformat(),
            "chain": self.current_chain,
            "outputs": outputs
        })
        self.current_chain = None
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs
    ) -> None:
        """Called when tool starts running."""
        self.events.append({
            "type": "tool_start",
            "timestamp": datetime.utcnow().isoformat(),
            "tool": serialized.get("name", "unknown_tool"),
            "input": input_str
        })
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Called when tool ends running."""
        self.events.append({
            "type": "tool_end",
            "timestamp": datetime.utcnow().isoformat(),
            "output": output
        })
    
    def on_agent_action(self, action: Any, **kwargs) -> None:
        """Called when agent takes action."""
        self.events.append({
            "type": "agent_action",
            "timestamp": datetime.utcnow().isoformat(),
            "action": str(action)
        })
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all captured events."""
        return self.events
    
    def clear_events(self):
        """Clear event history."""
        self.events = []


class LangChainLLMManager:
    """
    Manages LangChain LLM integrations for multiple providers.
    
    Provides unified interface for OpenAI, DeepSeek (via OpenAI API),
    Gemini, and local models through LangChain.
    """
    
    def __init__(self):
        """Initialize LLM manager."""
        self.llms: Dict[str, Any] = {}
        self.default_provider = "openai"
    
    def create_llm(
        self,
        provider: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Any:
        """
        Create LangChain LLM instance.
        
        Args:
            provider: Provider name (openai, deepseek, gemini, ollama)
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
        
        Returns:
            LangChain LLM instance
        """
        if provider == "openai":
            api_key = kwargs.get("api_key", os.getenv("OPENAI_API_KEY"))
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                openai_api_key=api_key
            )
        
        elif provider == "deepseek":
            # DeepSeek uses OpenAI-compatible API
            api_key = kwargs.get("api_key", os.getenv("DEEPSEEK_API_KEY"))
            base_url = kwargs.get("base_url", "https://api.deepseek.com/v1")
            
            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                openai_api_key=api_key,
                openai_api_base=base_url
            )
        
        elif provider == "gemini":
            api_key = kwargs.get("api_key", os.getenv("GOOGLE_API_KEY"))
            llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                max_output_tokens=max_tokens,
                google_api_key=api_key
            )
        
        elif provider == "ollama":
            # Local Ollama models
            llm = ChatOllama(
                model=model,
                temperature=temperature
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # Store LLM instance
        llm_key = f"{provider}_{model}"
        self.llms[llm_key] = llm
        
        return llm
    
    def get_llm(self, provider: str, model: str) -> Any:
        """Get existing LLM instance or create new one."""
        llm_key = f"{provider}_{model}"
        
        if llm_key not in self.llms:
            return self.create_llm(provider, model)
        
        return self.llms[llm_key]


class PromptTemplateManager:
    """
    Manages advanced prompt templates for various tasks.
    
    Provides pre-configured templates for:
    - Document generation
    - Research synthesis
    - Data analysis
    - Code generation
    - Question answering
    """
    
    def __init__(self):
        """Initialize template manager."""
        self.templates: Dict[str, ChatPromptTemplate] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize default prompt templates."""
        
        # Document section generation template
        self.templates["document_section"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert academic writer specializing in {domain}. "
                "Your writing is clear, well-structured, and follows {citation_style} citation style. "
                "Maintain a {tone} tone throughout."
            ),
            HumanMessagePromptTemplate.from_template(
                "Write a {section_type} section for a document titled '{title}'.\n\n"
                "Key topics to cover:\n{key_topics}\n\n"
                "Target word count: {word_count} words\n\n"
                "Context from previous sections:\n{context}\n\n"
                "Write the complete section:"
            )
        ])
        
        # Research synthesis template
        self.templates["research_synthesis"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a research synthesis expert. Analyze multiple research papers "
                "and synthesize their findings into a coherent narrative. Identify patterns, "
                "contradictions, and research gaps."
            ),
            HumanMessagePromptTemplate.from_template(
                "Synthesize the following research findings on '{topic}':\n\n"
                "{research_papers}\n\n"
                "Create a comprehensive synthesis that:\n"
                "1. Identifies key themes and patterns\n"
                "2. Highlights agreements and contradictions\n"
                "3. Notes methodological approaches\n"
                "4. Identifies research gaps\n\n"
                "Synthesis:"
            )
        ])
        
        # Data analysis interpretation template
        self.templates["data_analysis"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a data analysis expert. Interpret statistical results and "
                "explain their implications in clear, accessible language."
            ),
            HumanMessagePromptTemplate.from_template(
                "Analyze the following statistical results:\n\n"
                "{statistical_results}\n\n"
                "Research question: {research_question}\n\n"
                "Provide:\n"
                "1. Clear interpretation of the results\n"
                "2. Statistical significance and effect sizes\n"
                "3. Practical implications\n"
                "4. Limitations and caveats\n\n"
                "Analysis:"
            )
        ])
        
        # Code generation template
        self.templates["code_generation"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert programmer. Generate clean, well-documented, "
                "production-quality code following best practices."
            ),
            HumanMessagePromptTemplate.from_template(
                "Generate {language} code for the following task:\n\n"
                "Task: {task_description}\n\n"
                "Requirements:\n{requirements}\n\n"
                "Constraints:\n{constraints}\n\n"
                "Provide complete, executable code with comments:"
            )
        ])
        
        # Question answering with context template
        self.templates["qa_with_context"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are a helpful assistant. Answer questions based on the provided "
                "context. If the answer cannot be found in the context, say so clearly."
            ),
            HumanMessagePromptTemplate.from_template(
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        ])
        
        # Chain-of-thought reasoning template
        self.templates["chain_of_thought"] = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "You are an expert problem solver. Use step-by-step reasoning to "
                "solve complex problems. Show your thinking process clearly."
            ),
            HumanMessagePromptTemplate.from_template(
                "Problem: {problem}\n\n"
                "Think through this step-by-step:\n"
                "1. Understand the problem\n"
                "2. Identify key information\n"
                "3. Develop a solution approach\n"
                "4. Execute the solution\n"
                "5. Verify the result\n\n"
                "Reasoning:"
            )
        ])
    
    def get_template(self, template_name: str) -> ChatPromptTemplate:
        """Get prompt template by name."""
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
        
        return self.templates[template_name]
    
    def add_template(self, name: str, template: ChatPromptTemplate):
        """Add custom prompt template."""
        self.templates[name] = template


class LangChainMemoryManager:
    """
    Manages different memory strategies for LangChain agents.
    
    Supports:
    - Conversation buffer (recent messages)
    - Summary memory (compressed history)
    - Window memory (fixed-size buffer)
    - Vector store memory (semantic retrieval)
    """
    
    def __init__(self, llm: Any, vector_store: Optional[Any] = None):
        """
        Initialize memory manager.
        
        Args:
            llm: LangChain LLM for summary generation
            vector_store: Optional vector store for semantic memory
        """
        self.llm = llm
        self.vector_store = vector_store
        self.memories: Dict[str, Any] = {}
    
    def create_buffer_memory(
        self,
        memory_key: str = "chat_history",
        return_messages: bool = True
    ) -> ConversationBufferMemory:
        """
        Create conversation buffer memory.
        
        Stores all conversation messages without compression.
        Best for short conversations.
        """
        memory = ConversationBufferMemory(
            memory_key=memory_key,
            return_messages=return_messages
        )
        self.memories["buffer"] = memory
        return memory
    
    def create_summary_memory(
        self,
        memory_key: str = "chat_history"
    ) -> ConversationSummaryMemory:
        """
        Create conversation summary memory.
        
        Progressively summarizes conversation history using LLM.
        Best for long conversations where context compression needed.
        """
        memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key=memory_key
        )
        self.memories["summary"] = memory
        return memory
    
    def create_window_memory(
        self,
        k: int = 5,
        memory_key: str = "chat_history",
        return_messages: bool = True
    ) -> ConversationBufferWindowMemory:
        """
        Create conversation window memory.
        
        Keeps only the last k messages in memory.
        Best for maintaining recent context without unbounded growth.
        """
        memory = ConversationBufferWindowMemory(
            k=k,
            memory_key=memory_key,
            return_messages=return_messages
        )
        self.memories["window"] = memory
        return memory
    
    def create_vector_memory(
        self,
        memory_key: str = "chat_history"
    ) -> Optional[VectorStoreRetrieverMemory]:
        """
        Create vector store memory.
        
        Stores conversation in vector store for semantic retrieval.
        Best for very long conversations requiring intelligent context retrieval.
        """
        if not self.vector_store:
            return None
        
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )
        
        memory = VectorStoreRetrieverMemory(
            retriever=retriever,
            memory_key=memory_key
        )
        self.memories["vector"] = memory
        return memory
    
    def get_memory(self, memory_type: str) -> Any:
        """Get memory instance by type."""
        return self.memories.get(memory_type)


class DocumentProcessor:
    """
    Processes documents using LangChain loaders and text splitters.
    
    Supports loading from multiple formats and intelligent chunking
    for RAG (Retrieval Augmented Generation) applications.
    """
    
    def __init__(self):
        """Initialize document processor."""
        self.loaders: Dict[str, type] = {
            "txt": TextLoader,
            "pdf": PyPDFLoader,
            "md": UnstructuredMarkdownLoader,
            "docx": Docx2txtLoader
        }
    
    def load_document(
        self,
        file_path: str,
        file_type: Optional[str] = None
    ) -> List[Any]:
        """
        Load document from file.
        
        Args:
            file_path: Path to document
            file_type: File type (txt, pdf, md, docx) - auto-detected if None
        
        Returns:
            List of LangChain Document objects
        """
        if not file_type:
            # Auto-detect from extension
            file_type = file_path.split('.')[-1].lower()
        
        loader_class = self.loaders.get(file_type)
        if not loader_class:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        loader = loader_class(file_path)
        documents = loader.load()
        
        return documents
    
    def split_documents(
        self,
        documents: List[Any],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        method: str = "recursive"
    ) -> List[Any]:
        """
        Split documents into chunks for processing.
        
        Args:
            documents: List of documents to split
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks
            method: Splitting method (recursive, character, token)
        
        Returns:
            List of document chunks
        """
        if method == "recursive":
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", " ", ""]
            )
        elif method == "character":
            splitter = CharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        elif method == "token":
            splitter = TokenTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        else:
            raise ValueError(f"Unknown splitting method: {method}")
        
        chunks = splitter.split_documents(documents)
        return chunks


class RAGSystem:
    """
    Retrieval Augmented Generation (RAG) system using LangChain.
    
    Enables question answering over custom documents using vector search
    and LLM generation.
    """
    
    def __init__(
        self,
        llm: Any,
        embedding_model: str = "openai",
        persist_directory: Optional[str] = None
    ):
        """
        Initialize RAG system.
        
        Args:
            llm: LangChain LLM for generation
            embedding_model: Embedding model (openai or huggingface)
            persist_directory: Directory for vector store persistence
        """
        self.llm = llm
        self.persist_directory = persist_directory
        
        # Initialize embeddings
        if embedding_model == "openai":
            self.embeddings = OpenAIEmbeddings()
        else:
            # Use free HuggingFace embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        
        self.vector_store: Optional[Chroma] = None
        self.retriever = None
    
    def create_vector_store(
        self,
        documents: List[Any],
        collection_name: str = "graive_documents"
    ):
        """
        Create vector store from documents.
        
        Args:
            documents: List of document chunks
            collection_name: Name for the collection
        """
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=self.persist_directory
        )
        
        # Create retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
    
    def query(
        self,
        question: str,
        return_source_documents: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: Question to answer
            return_source_documents: Whether to return source documents
        
        Returns:
            Answer and optionally source documents
        """
        if not self.retriever:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        # Retrieve relevant documents
        relevant_docs = self.retriever.get_relevant_documents(question)
        
        # Combine document content
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful assistant. Answer questions based on the provided context."),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:")
        ])
        
        # Generate answer
        chain = LLMChain(llm=self.llm, prompt=prompt)
        answer = chain.run(question=question)
        
        result = {"answer": answer}
        
        if return_source_documents:
            result["source_documents"] = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in relevant_docs
            ]
        
        return result


class ChainBuilder:
    """
    Builds complex LangChain chains for multi-step reasoning and processing.
    
    Supports:
    - Sequential chains (step-by-step processing)
    - Transform chains (data transformation)
    - Router chains (conditional routing)
    """
    
    def __init__(self, llm: Any):
        """
        Initialize chain builder.
        
        Args:
            llm: LangChain LLM instance
        """
        self.llm = llm
        self.chains: Dict[str, Any] = {}
    
    def create_sequential_chain(
        self,
        chain_steps: List[Dict[str, Any]],
        chain_name: str
    ) -> SequentialChain:
        """
        Create sequential chain from steps.
        
        Args:
            chain_steps: List of chain step configurations
            chain_name: Name for the chain
        
        Returns:
            SequentialChain instance
        """
        chains = []
        
        for step in chain_steps:
            prompt = ChatPromptTemplate.from_template(step["prompt_template"])
            chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                output_key=step["output_key"]
            )
            chains.append(chain)
        
        # Combine into sequential chain
        sequential_chain = SequentialChain(
            chains=chains,
            input_variables=chain_steps[0].get("input_variables", []),
            output_variables=[step["output_key"] for step in chain_steps],
            verbose=True
        )
        
        self.chains[chain_name] = sequential_chain
        return sequential_chain
    
    def create_document_generation_chain(self) -> SequentialChain:
        """
        Create chain for multi-step document generation.
        
        Steps:
        1. Outline generation
        2. Research synthesis
        3. Section writing
        4. Editing and refinement
        """
        chain_steps = [
            {
                "prompt_template": (
                    "Create a detailed outline for a document on '{topic}'. "
                    "Include main sections and key points for each section."
                ),
                "output_key": "outline",
                "input_variables": ["topic"]
            },
            {
                "prompt_template": (
                    "Based on this outline:\n{outline}\n\n"
                    "Synthesize relevant research and background information "
                    "for the topic '{topic}'."
                ),
                "output_key": "research",
                "input_variables": ["topic", "outline"]
            },
            {
                "prompt_template": (
                    "Using this outline:\n{outline}\n\n"
                    "And this research:\n{research}\n\n"
                    "Write a complete draft of the document."
                ),
                "output_key": "draft",
                "input_variables": ["outline", "research"]
            }
        ]
        
        return self.create_sequential_chain(chain_steps, "document_generation")
