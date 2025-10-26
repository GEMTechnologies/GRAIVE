# Sandbox Storage System - Multi-layered Persistent Data Storage

## Overview

The Graive AI Sandbox Storage System implements a sophisticated multi-layered persistence architecture that enables sandboxes to function as stateful virtual machines with complete data retention across their entire lifecycle. This comprehensive storage framework supports long-running projects including document generation, data analysis, application development, and research workflows that span days, weeks, or months.

The system addresses the fundamental requirement for persistent state in autonomous AI systems where reasoning, execution results, intermediate outputs, and contextual knowledge must survive beyond individual task boundaries. Each sandbox maintains isolated storage across five distinct but integrated layers, providing specialized persistence mechanisms optimized for different data types and access patterns.

## Architecture

The storage architecture employs a layered approach where each layer serves specific persistence requirements while maintaining seamless integration through a unified interface. This design enables efficient data organization, rapid retrieval, and scalable growth as sandbox projects evolve.

### Layer 1: File System Storage

The file system layer provides UNIX-like persistent storage rooted at `/home/ubuntu/` within each sandbox environment. This layer supports standard file operations including create, read, update, delete, append, and directory traversal. All files written to this layer persist for the entire sandbox lifecycle, enabling projects to maintain source code, configuration files, generated documents, analysis scripts, logs, and any file-based artifacts.

The file system implementation uses the host operating system's native file storage with proper isolation between sandboxes. Each sandbox receives a dedicated directory structure ensuring complete separation from other sandboxes. The path `/home/ubuntu/` mimics a standard Ubuntu user environment, providing familiarity for code execution and script development.

File operations support both text and binary modes, UTF-8 and custom encodings, atomic writes preventing corruption, hierarchical directory structures, and glob pattern matching for file discovery. The system automatically creates parent directories when writing files, simplifying file organization without manual directory management.

Persistent file storage enables document generation workflows to save chapter files, research data, analysis scripts, and generated visualizations that accumulate over multi-day thesis generation. Data analysis projects store datasets, processing scripts, intermediate results, and final reports. Application development maintains source code, dependencies, configuration, and build artifacts across iterative development cycles.

### Layer 2: Context/Knowledge Base

The context/knowledge base layer implements an in-memory JSON structure with automatic persistence to disk, capturing reasoning state, task plans, user messages, tool observations, conversation history, and execution metadata. This layer functions as the "memory" of the sandbox, maintaining the logical flow and state information that enables coherent multi-step workflows.

The knowledge base stores arbitrary JSON-serializable data structures including task planning information with current goals, progress tracking, section status, and execution order. Conversation history records user requests, agent responses, clarifications, and feedback. Tool execution observations capture what actions were performed, what results were obtained, and what errors occurred. Research findings accumulate key discoveries, citation information, analysis results, and synthesis conclusions. Execution state tracks current phase, checkpoint positions, intermediate values, and resumption points.

Context entries support type categorization enabling organization by purpose such as task, conversation, research, execution, or custom types. Temporal metadata tracks creation time and last update. Flexible schema allows any JSON-serializable data structure. Text search enables finding contexts by content or key. Type filtering retrieves all contexts of specific categories.

The persistence model maintains in-memory structures for fast access while automatically synchronizing to disk on every modification. This approach provides memory-speed retrieval with disk-level durability. The knowledge base loads automatically when the sandbox initializes, restoring complete state from previous sessions.

Context storage proves essential for document generation where sections reference earlier content requiring shared terminology, consistent citations, cross-section dependencies, and progress tracking across multi-wave parallel execution. Long-running analysis workflows maintain partial results, algorithm state, optimization parameters, and convergence history across multiple execution sessions.

### Layer 3: Database Scaffold

The database scaffold layer provides structured relational data storage supporting SQLite, PostgreSQL, and MySQL database systems. This layer enables data-driven applications, complex analytics, multi-table relationships, SQL querying, and transaction management within sandbox environments.

SQLite serves as the default database type, requiring no external server and providing file-based storage ideal for development, prototyping, single-user applications, and embedded data management. The system creates SQLite database files within the sandbox directory, ensuring complete portability and isolation.

Database operations support table creation with custom schemas, INSERT/UPDATE/DELETE operations with parameter binding, SELECT queries with joins and aggregations, transaction management for consistency, and programmatic access via connection objects. The unified query interface accepts SQL statements with optional parameterization, executes queries within transaction contexts, returns structured results with column names, and handles errors with detailed messages.

Structured databases enable research data management storing patient records, clinical measurements, experimental results, and statistical analyses. Citation management maintains bibliographic information with author details, publication metadata, journal information, and cross-references. Document metadata tracks section information, word counts, generation timestamps, and revision history. Application data supports user accounts, configuration settings, application state, and business logic.

The scaffold supports database migration workflows through DDL statement execution, enabling schema evolution as project requirements change. Applications can create tables dynamically, add columns to existing tables, create indexes for performance, and alter constraints as needed.

### Layer 4: Media Cache

The media cache layer provides organized storage and efficient retrieval for generated media files including images, charts, audio, video, and presentations. This layer implements content-addressed storage with type-based organization, automatic indexing, and metadata tracking.

Media types supported include images (PNG, JPEG, GIF, SVG) for visualizations and diagrams, charts (matplotlib, seaborn, plotly outputs) for data visualization, audio (MP3, WAV, generated speech) for text-to-speech outputs, video (MP4, generated animations) for dynamic visualizations, and presentations (PPTX) for slide deck generation.

The cache implementation organizes media into type-specific directories creating separate subdirectories for each media type. Content hashing generates unique identifiers preventing duplication. Automatic indexing maintains a JSON catalog of all cached media. Metadata tracking stores filename, size, creation time, and custom attributes. Binary storage preserves exact file contents.

Caching operations support adding media by providing binary data and media type, optionally specifying filename, automatically detecting format from magic bytes or extension, and storing with unique content hash identifier. Retrieval finds media by content hash, returns complete binary data, supports batch retrieval, and maintains access statistics.

The media cache proves invaluable for document generation workflows caching generated figures, tables rendered as images, chart visualizations, diagram exports, and presentation slides. Data analysis projects store exploratory plots, statistical visualizations, heatmaps and correlation matrices, time series graphs, and publication-quality figures. Multi-modal applications manage image generation outputs, audio synthesis results, video compilations, and presentation decks.

### Layer 5: Vector Store

The vector store layer implements semantic embedding storage enabling intelligent content retrieval based on meaning rather than exact text matching. This layer integrates ChromaDB for persistent vector storage, supports automatic embedding generation using sentence transformers, enables similarity search with cosine distance, and provides metadata filtering for targeted queries.

Vector embeddings represent document sections, research findings, conversation snippets, code documentation, and any textual content requiring semantic search. The system automatically generates embeddings using `sentence-transformers/all-MiniLM-L6-v2` model, achieving good performance with 384-dimensional vectors suitable for most retrieval tasks.

Semantic search capabilities support finding related document sections when writing new content, retrieving relevant research findings for synthesis, discovering similar code examples or solutions, locating pertinent conversation history, and identifying contextually related information across the entire sandbox knowledge base.

The vector store maintains bidirectional linkage with relational data through embedding IDs that reference original content, metadata that includes source type and location, timestamps tracking embedding creation, and search results that include original text with metadata.

Integration with document generation enables finding related literature when writing new sections, retrieving relevant previous sections for consistency, discovering similar research for comparison, maintaining thematic coherence across chapters, and supporting intelligent cross-referencing.

## Storage Layer Comparison

| Layer | Primary Use Case | Access Pattern | Persistence | Search Capability |
|-------|-----------------|----------------|-------------|-------------------|
| File System | Source code, documents, scripts | Path-based | Permanent | Glob patterns |
| Context/Knowledge | Reasoning state, task plans | Key-value | Permanent | Text search |
| Database | Structured relational data | SQL queries | Permanent | SQL WHERE |
| Media Cache | Images, audio, videos | Content hash | Permanent | Type/metadata filter |
| Vector Store | Semantic content | Embedding similarity | Permanent | Semantic search |

## Integration with Document Generation

The storage system integrates seamlessly with the document orchestration framework, enabling sophisticated workflows for ultra-long document generation with persistent state management across all execution phases.

During the planning phase, the orchestrator stores the complete document plan in the context layer including section structure, word count allocations, agent assignments, and execution order. The plan persists across sessions enabling resumption after interruptions. The planning metadata supports progress tracking, modification history, and execution analytics.

Throughout section execution, specialized agents utilize multiple storage layers simultaneously. The file system stores generated section files, analysis scripts, data files, and temporary outputs. The context layer maintains section status, completion timestamps, word counts, and cross-section references. The database holds research data, citation information, statistical results, and structured metadata. The media cache stores generated figures, tables as images, charts and graphs, and visualization outputs. The vector store indexes section content, key findings, research summaries, and methodology descriptions.

Document assembly leverages the vector store to find related content for intelligent element placement, discover similar sections for consistency checking, retrieve relevant findings for cross-referencing, and maintain thematic coherence. The context layer provides section summaries for table of contents generation, citation lists for bibliography compilation, element catalogs for figure/table numbering, and cross-reference mappings for link generation.

Export processes read section files from the file system, retrieve element data from media cache, fetch metadata from context and database, and compile everything into final output formats. The complete sandbox can be exported as an archive preserving all source files, generated content, databases, media files, and context information for archival or transfer.

## Performance Characteristics

The storage system achieves high performance through several optimization strategies that balance speed, durability, and resource utilization.

File system operations benefit from operating system caching where frequently accessed files remain in memory buffers. Atomic writes use temporary files with rename operations ensuring consistency. Directory structure organization groups related files improving locality. Lazy loading defers reading file contents until explicitly requested.

Context/knowledge base optimization maintains in-memory representations for instant retrieval. Batch updates accumulate changes before disk synchronization. JSON serialization uses compact formatting. Index structures enable fast key lookups without scanning.

Database performance relies on SQLite's optimized B-tree indexes, transaction batching for write efficiency, prepared statements with parameter binding, and connection pooling for concurrent access.

Media cache efficiency employs content hashing to detect duplicates automatically, type-based directory organization reducing search space, index lookups avoiding filesystem scans, and lazy loading of binary data on demand.

Vector store performance leverages ChromaDB's optimized similarity algorithms, embedding cache preventing redundant computation, metadata filtering reducing search space, and incremental index updates on additions.

## Use Cases

### Long-Running Document Generation

A PhD thesis generation spanning multiple days benefits from persistent storage where daily progress automatically saves section files, partial sections, generated figures, and analysis results. The context layer maintains overall progress tracking section completion status and tracking word count accumulation. The database stores citation information, research data, and document metadata. The media cache holds generated visualizations and figures. The vector store enables semantic search across completed sections.

Work sessions resume seamlessly by loading complete state from previous session, continuing from exact stopping point, accessing all prior work products, and maintaining perfect consistency across sessions.

### Data Analysis Workflows

Multi-week analysis projects leverage persistent storage for datasets in file system and database, analysis scripts with complete version history, intermediate processing results, statistical models and parameters, and visualization outputs in media cache.

Iterative development benefits from accumulated knowledge where each analysis builds on previous results, successful approaches persist for reuse, failed attempts inform future strategies, and the complete analytical narrative preserves in context.

### Application Development

Software projects within sandboxes maintain source code across editing sessions, dependency manifests and installed packages, configuration files and environment variables, database schemas and test data, build artifacts and deployment packages, and development logs and debugging information.

The persistent environment supports continuous development without restart overhead, immediate resumption after breaks, complete project history in context, and seamless collaboration through sandbox export.

## Storage Management

### Capacity Planning

Each sandbox consumes storage proportional to its workload characteristics. Typical capacity requirements for different project types include:

**Small Projects** (< 100 MB total):
- Simple scripts and configuration
- Modest context and database usage
- Few media files
- Limited vector embeddings

**Medium Projects** (100 MB - 1 GB):
- Document generation with figures
- Moderate database content
- Reasonable media cache
- Section-level vector search

**Large Projects** (1 GB - 10 GB):
- Thesis-scale documents
- Comprehensive citation databases
- Extensive figure/chart collections
- Complete document embedding

**Extra-Large Projects** (> 10 GB):
- Multi-document corpora
- Large research datasets
- Video/audio libraries
- Cross-document semantic search

### Maintenance Operations

The storage system supports various maintenance operations for managing sandbox lifecycle and resource utilization.

Layer clearing removes all data from specific layers while preserving others, useful for resetting file system while keeping context, clearing media cache to free space, or purging database while maintaining files.

Selective deletion targets specific files, contexts, database tables, or cached media based on age, size, access frequency, or custom criteria.

Archival exports create complete sandbox snapshots as compressed archives, supporting versioning with timestamp labels, migration to different environments, backup for disaster recovery, and collaboration through sandbox sharing.

Storage statistics provide visibility into disk usage by layer, file count distributions, database size metrics, media cache utilization, and growth trends over time.

### Security and Isolation

Each sandbox operates in complete isolation from others through separate directory trees preventing cross-sandbox access, independent database files, isolated context stores, separate media caches, and distinct vector collections.

The file system layer enforces sandbox boundaries through path validation preventing directory traversal, symlink restrictions avoiding escape, permission models ensuring proper access, and chroot-like isolation containing all operations within sandbox root.

## Integration with Graive AI Platform

The storage system integrates deeply with other Graive AI components providing unified persistence across the platform.

Tool orchestrator integration enables all tools to access storage consistently with document tools reading/writing files, data tools using databases, media tools caching outputs, and analysis tools storing results.

Infinite memory integration stores compressed memory segments in file system, indexes segments in vector store, maintains memory metadata in context, and enables semantic retrieval of historical context.

Database integration shares vector storage infrastructure, coordinates embedding generation, maintains consistent metadata, and supports cross-system queries.

Interactive agent loop integration persists conversation state in context, stores checkpoint data in file system, maintains user feedback in database, and enables perfect state resumption.

## Best Practices

### Effective Storage Usage

Organize files hierarchically grouping related content, use descriptive names for discoverability, avoid deep nesting reducing path complexity, and maintain README files documenting structure.

Store appropriate data in each layer with transient calculations in memory, persistent state in context, structured data in database, large files in file system, and searchable content in vector store.

Regular cleanup removes temporary files periodically, archives old media, prunes outdated contexts, and optimizes database tables.

### Performance Optimization

Batch operations when possible accumulating file writes, combining database inserts, caching database connections, and reusing embedding lookups.

Use appropriate search methods with file system for known paths, context for key lookup, database for structured queries, media cache for content retrieval, and vector store for semantic discovery.

Monitor storage growth tracking layer sizes, identifying large files, reviewing database growth, and managing media accumulation.

## Conclusion

The Graive AI Sandbox Storage System provides enterprise-grade persistent data management for autonomous AI environments through a sophisticated multi-layered architecture. By offering specialized persistence mechanisms for different data types while maintaining seamless integration, the system enables complex long-running workflows including document generation, data analysis, and application development with complete state preservation across sessions.

The combination of file system storage, context management, relational databases, media caching, and semantic search creates a comprehensive persistence foundation that supports the full spectrum of AI agent activities from simple script execution to month-long research projects generating publication-quality documents.
