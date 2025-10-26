# Windows Testing Guide - Long-Running Operation

This guide provides step-by-step instructions for testing Graive AI's long-running capabilities on your Windows machine without incurring API costs.

## Prerequisites Validation

Before running endurance tests, verify your Windows environment has the required dependencies installed. Open PowerShell in the Graive project directory and execute the dependency check command.

```powershell
cd "c:\Users\GEMTECH 1\Desktop\GRAIVE"
python -m pip install -r requirements.txt
```

The installation will configure all necessary packages including LangChain for agent orchestration, Selenium for browser automation, SQLAlchemy for database operations, ChromaDB for vector storage, and various utility libraries for document processing and cost management.

## Immediate Testing Options

### Test 1: Storage Persistence (5 minutes, $0 cost)

This test validates that the multi-layered storage system maintains state across extended operations without data loss. The storage system represents a critical component for long-running thesis generation projects that may span multiple days.

Execute the storage persistence test to verify file system operations, context knowledge base functionality, database scaffolding, and vector store integration. The test creates a simulated thesis project, writes sections to the file system, stores progress context, creates citation databases, and verifies all data persists correctly.

```powershell
python tests\test_long_running_endurance.py
```

This test will output detailed progress indicators showing each phase of storage validation including section writing, context storage, database operations, and retrieval verification. Successful completion confirms the storage layer can support multi-day projects without state loss.

### Test 2: Memory Management (3 minutes, $0 cost)

This test evaluates the memory management system's ability to handle thousands of conversation turns without exponential memory growth or context degradation. Long-running thesis generation involves hundreds of LLM interactions, requiring sophisticated memory strategies.

The test suite validates three distinct memory approaches: buffer memory maintaining complete conversation history, summary memory using LLM compression to bound growth, and window memory retaining only recent interactions. Each strategy undergoes simulation with 100 conversation turns while monitoring memory consumption.

Run the memory management validation by executing the endurance test suite with the memory-specific flag. The output displays memory growth patterns for each strategy, demonstrating which approach best suits different operational requirements.

### Test 3: Cost Optimization (2 minutes, $0 cost)

This critical test demonstrates intelligent cost reduction through hybrid provider routing without sacrificing output quality. The system routes different task types to appropriate LLM providers based on complexity requirements.

The simulation generates a complete thesis using the hybrid strategy: routing critical research synthesis to GPT-4, routine content generation to DeepSeek at 99% cost savings, simple formatting tasks to GPT-3.5 Turbo, and mixed operations to Gemini Flash. The test tracks cumulative costs and compares total expenditure against the alternative of using GPT-4 exclusively.

Expected results show approximately 70-80% cost reduction compared to single-provider approaches while maintaining equivalent quality for the final output. The detailed cost report breaks down spending by provider, operation type, and task complexity.

### Test 4: Performance Monitoring (3 minutes, $0 cost)

This test monitors system resource utilization during extended operation to detect potential memory leaks, CPU bottlenecks, or file handle exhaustion. The simulation runs through all phases of thesis generation while capturing performance snapshots.

The performance monitor tracks memory consumption in megabytes, CPU usage percentage, active thread counts, and open file descriptors. Analysis algorithms detect abnormal memory growth patterns that would indicate resource leaks requiring investigation.

Successful test completion generates a comprehensive report showing resource usage trends over the simulated runtime, enabling identification of optimization opportunities before production deployment.

## Cost-Free Testing with Mock Providers

For extended testing without API costs, configure the system to use mock LLM providers that simulate realistic behavior including API latency, token consumption, and response generation without making actual API calls.

Create a test configuration file that overrides the default LLM provider settings:

```python
# test_config.py
from src.cost_optimization import create_cost_manager, TaskComplexity

# Initialize cost manager with testing budget
cost_manager = create_cost_manager(
    daily_budget=50.0,
    weekly_budget=200.0,
    enable_caching=True
)

# Enable mock mode for testing
USE_MOCK_PROVIDERS = True
MOCK_API_LATENCY = 0.5  # Simulate 500ms API calls

# Test a complete workflow
from examples.complete_thesis_generation_workflow import CompletThesisWorkflow

# Override LLM with mock
if USE_MOCK_PROVIDERS:
    # Mock provider simulates GPT-4 behavior without costs
    print("Running in MOCK MODE - no API costs incurred")
```

Mock providers generate realistic response times and token usage statistics while returning simulated content, enabling comprehensive testing of orchestration logic, memory management, cost tracking, and storage operations without financial expenditure.

## Progressive Real Testing Strategy

Once mock testing validates system stability, begin progressive real testing with actual API calls under controlled budget constraints. This approach minimizes risk while validating production behavior.

### Phase 1: Short Workflow (30 minutes, $2-5 budget)

Begin with a constrained workflow generating a single thesis section of approximately 2,000 words. Configure the cost manager with a strict $5 daily budget and enable caching to reduce redundant calls.

```powershell
# Set environment variables for API keys
$env:OPENAI_API_KEY = "your-openai-key"
$env:DEEPSEEK_API_KEY = "your-deepseek-key"

# Run short workflow
python examples\short_thesis_test.py
```

Monitor the cost report generated after completion, verifying that hybrid routing functions correctly and total expenditure remains within the $5 constraint. Examine the cache hit rate to confirm response caching operates effectively.

### Phase 2: Medium Workflow (2 hours, $10-15 budget)

Expand testing to generate three thesis sections totaling approximately 10,000 words with citations and basic statistical analysis. Increase the daily budget to $15 while maintaining weekly budget enforcement.

This phase validates sustained operation across multiple sections, context management between sections, citation database integration, and RAG system performance. The two-hour duration tests memory management effectiveness and identifies potential performance degradation.

### Phase 3: Extended Workflow (8 hours, $30-50 budget)

Execute a complete thesis generation workflow producing 50,000 words across seven major sections with full statistical analysis, figure generation, and bibliography assembly. Configure a $50 daily budget with automatic throttling if approaching the limit.

Run the extended test overnight or during a period when you can monitor progress intermittently. The system implements automatic checkpointing every 30 minutes, enabling resumption if interruption occurs.

```powershell
# Run extended workflow with monitoring
python examples\complete_thesis_generation_workflow.py --checkpoint-interval 1800 --daily-budget 50
```

The checkpoint system stores progress to the multi-layered storage, allowing restart from the last completed section if the process terminates. Monitor the generated log files for performance metrics, cost tracking, and completion status.

## Real-Time Monitoring During Tests

While tests execute, monitor system behavior through multiple channels providing visibility into operations, costs, and performance.

### Terminal Output Monitoring

The primary terminal displays real-time progress indicators showing current operation, tokens consumed, estimated cost, cache hit/miss status, and cumulative spending. Example output during literature review generation:

```
Literature Review Generation (Section 2/7)
  Operation: RAG query for "machine learning diagnostics"
  Provider: deepseek/deepseek-chat
  Tokens: 1,247 in, 856 out
  Cost: $0.0003 (cached: no)
  Total daily spend: $2.47 / $50.00
  Progress: 28% complete
```

### Cost Reports

Request cost reports at any time by sending SIGINT (Ctrl+C once, not twice) which triggers graceful checkpoint and report generation without terminating the process. The report displays spending breakdown by provider, operation type, and task complexity along with budget status and cache performance.

### Performance Metrics

Monitor system resource usage through Windows Task Manager or PowerShell commands to detect abnormal behavior:

```powershell
# Monitor Python process memory usage
Get-Process python | Select-Object WorkingSet,CPU
```

Normal operation maintains memory usage below 1GB for thesis generation workflows. Memory growth exceeding 100MB per hour indicates potential leaks requiring investigation.

## Optimization Recommendations Based on Testing

After completing test phases, analyze generated reports to identify optimization opportunities specific to your usage patterns.

### Cost Optimization Adjustments

If testing reveals costs exceeding budget targets, implement these optimization strategies systematically. Increase DeepSeek usage for routine content generation, implementing provider routing that reserves GPT-4 for critical reasoning while using DeepSeek for drafting. Enable aggressive caching with extended TTL (time-to-live) of 14 days for literature review content that rarely changes. Reduce output token limits for iterative refinement passes, using shorter responses for validation and formatting operations.

### Performance Optimization Adjustments

If testing identifies performance bottlenecks or resource constraints, address them through targeted modifications. Increase checkpoint frequency from 30 minutes to 15 minutes for better resumption granularity without significant overhead. Enable parallel section generation for independent chapters, maximizing throughput on multi-core systems. Implement browser session recycling every 4 hours to prevent memory accumulation in long-running automation tasks. Configure database connection pooling with limits appropriate to your system's available memory.

### Memory Management Adjustments

If conversation history grows excessively during testing, switch memory strategies based on observed behavior. Replace buffer memory with summary memory for conversations exceeding 50 turns, implementing automatic compression. Reduce window size from default 10 to 5 messages for operations requiring minimal context. Implement explicit memory clearing between major sections to prevent context contamination.

## Expected Test Results

Successful testing produces these benchmark results indicating production readiness.

### Storage Tests

All sections persist correctly across restarts with context retrieval accuracy of 100%, database query performance under 10ms for citation lookups, and vector store similarity search completing within 100ms for collections under 10,000 embeddings. File system operations complete without errors and storage utilization remains proportional to generated content volume.

### Memory Tests

Buffer memory grows linearly at approximately 500 tokens per conversation turn, summary memory maintains bounded size around 2,000 tokens regardless of conversation length, and window memory remains constant at configured size with immediate retrieval. No memory degradation occurs across 100+ conversation turns.

### Cost Tests

Hybrid provider strategy achieves 70-85% cost reduction compared to GPT-4-only approaches while maintaining equivalent output quality. Cache hit rates exceed 30% for repeated thesis generation tasks with similar topics. Daily budget enforcement prevents overspending with automatic throttling when approaching limits.

### Performance Tests

Memory usage remains stable below 1GB throughout 8-hour test sessions with no detected leaks. CPU usage averages 15-25% during generation phases with spikes to 60% during statistical analysis code execution. The system completes 200-page thesis generation in 8-12 hours of continuous operation without crashes or errors.

## Troubleshooting Common Issues

If tests fail or produce unexpected results, consult these troubleshooting steps addressing frequent issues.

### Import Errors

If Python reports module not found errors for Graive components, verify the Python path includes the src directory. Add the following to test scripts:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### API Key Errors

If tests using real providers fail with authentication errors, verify environment variables contain valid API keys without extra whitespace or quotes:

```powershell
$env:OPENAI_API_KEY = "sk-actual-key-here"
echo $env:OPENAI_API_KEY  # Verify correct value
```

### Memory Errors

If tests terminate with out-of-memory errors, reduce batch sizes and enable more aggressive memory management. Decrease chunk size for RAG document processing from 1000 to 500 tokens, reduce maximum conversation buffer from unlimited to 10,000 tokens, and enable periodic garbage collection after major operations.

### Performance Issues

If tests run extremely slowly, verify network connectivity to API providers and check for antivirus software interfering with file operations. Disable real-time scanning for the Graive project directory if file I/O appears throttled. Consider using local models through Ollama for development testing to eliminate network latency.

## Conclusion and Next Steps

After completing all test phases successfully, your Graive AI installation demonstrates production readiness for long-running autonomous thesis generation. The system can operate continuously for 8-16 hours generating comprehensive academic documents while maintaining cost control through hybrid provider routing, response caching, and budget enforcement.

Typical operation costs for a complete 200-page thesis range from $20 to $50 depending on provider selection and caching effectiveness, representing 60-80% cost reduction compared to naive implementations. The multi-layered storage system enables project persistence across days or weeks, supporting extended research projects with full state recovery.

Begin production usage with conservative daily budgets of $25-30, gradually increasing as you develop confidence in cost management effectiveness. Monitor early productions closely to refine provider routing rules and identify opportunities for additional caching. The system learns from usage patterns, improving efficiency over time through accumulated cache entries and optimized prompt templates.
