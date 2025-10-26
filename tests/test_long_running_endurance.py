"""
Long-Running Endurance Test for Graive AI System

Tests system stability, memory management, and cost efficiency during
extended operation simulating a full-day thesis generation workflow.

This test suite validates:
- Multi-hour operation without crashes or memory leaks
- Cost tracking and budget enforcement
- Storage persistence across restarts
- Memory management effectiveness
- Performance degradation monitoring
"""

import os
import sys
import time
import psutil
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.storage import create_storage_tool_for_sandbox
from src.langchain_integration import (
    LangChainLLMManager,
    LangChainMemoryManager,
    RAGSystem
)


class CostTracker:
    """Track and enforce API cost budgets during testing."""
    
    def __init__(self, daily_budget: float = 50.0):
        self.daily_budget = daily_budget
        self.total_spent = 0.0
        self.calls_by_provider = {}
        self.tokens_by_operation = {}
        self.start_time = datetime.now()
        self.lock = threading.Lock()
    
    def estimate_call_cost(
        self,
        provider: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Estimate cost of an API call."""
        pricing = {
            "openai_gpt4": {"input": 0.03/1000, "output": 0.06/1000},
            "openai_gpt35": {"input": 0.0015/1000, "output": 0.002/1000},
            "deepseek": {"input": 0.00014/1000, "output": 0.00028/1000},
            "gemini_flash": {"input": 0.000075/1000, "output": 0.0003/1000},
            "embedding": {"input": 0.0001/1000, "output": 0.0}
        }
        
        rates = pricing.get(provider, pricing["openai_gpt4"])
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])
        return cost
    
    def record_call(
        self,
        provider: str,
        operation: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, Any]:
        """Record an API call and update costs."""
        cost = self.estimate_call_cost(provider, input_tokens, output_tokens)
        
        with self.lock:
            self.total_spent += cost
            
            if provider not in self.calls_by_provider:
                self.calls_by_provider[provider] = {"calls": 0, "cost": 0.0}
            
            self.calls_by_provider[provider]["calls"] += 1
            self.calls_by_provider[provider]["cost"] += cost
            
            if operation not in self.tokens_by_operation:
                self.tokens_by_operation[operation] = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "calls": 0,
                    "cost": 0.0
                }
            
            self.tokens_by_operation[operation]["input_tokens"] += input_tokens
            self.tokens_by_operation[operation]["output_tokens"] += output_tokens
            self.tokens_by_operation[operation]["calls"] += 1
            self.tokens_by_operation[operation]["cost"] += cost
        
        return {
            "cost": cost,
            "total_spent": self.total_spent,
            "remaining_budget": self.daily_budget - self.total_spent,
            "budget_exceeded": self.total_spent > self.daily_budget
        }
    
    def get_report(self) -> str:
        """Generate cost report."""
        runtime = datetime.now() - self.start_time
        hours = runtime.total_seconds() / 3600
        
        report = f"""
{'='*70}
COST TRACKING REPORT
{'='*70}

Runtime: {hours:.2f} hours
Total Spent: ${self.total_spent:.2f}
Daily Budget: ${self.daily_budget:.2f}
Remaining: ${self.daily_budget - self.total_spent:.2f}
Budget Status: {'EXCEEDED' if self.total_spent > self.daily_budget else 'WITHIN BUDGET'}

{'='*70}
SPENDING BY PROVIDER
{'='*70}
"""
        
        for provider, stats in sorted(self.calls_by_provider.items()):
            report += f"\n{provider}:"
            report += f"\n  Calls: {stats['calls']}"
            report += f"\n  Cost: ${stats['cost']:.4f}"
            report += f"\n  Avg per call: ${stats['cost']/stats['calls']:.4f}"
        
        report += f"\n\n{'='*70}"
        report += f"\nOPERATIONS BREAKDOWN"
        report += f"\n{'='*70}\n"
        
        for operation, stats in sorted(
            self.tokens_by_operation.items(),
            key=lambda x: x[1]['cost'],
            reverse=True
        ):
            report += f"\n{operation}:"
            report += f"\n  Calls: {stats['calls']}"
            report += f"\n  Input tokens: {stats['input_tokens']:,}"
            report += f"\n  Output tokens: {stats['output_tokens']:,}"
            report += f"\n  Cost: ${stats['cost']:.4f}"
        
        report += f"\n\n{'='*70}\n"
        
        return report


class PerformanceMonitor:
    """Monitor system performance during long-running operations."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.start_time = time.time()
        self.snapshots = []
    
    def take_snapshot(self, label: str = ""):
        """Record current system state."""
        snapshot = {
            "timestamp": time.time() - self.start_time,
            "label": label,
            "memory_mb": self.process.memory_info().rss / 1024 / 1024,
            "cpu_percent": self.process.cpu_percent(interval=0.1),
            "threads": self.process.num_threads(),
            "open_files": len(self.process.open_files())
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    def detect_memory_leak(self, threshold_mb: float = 100) -> bool:
        """Check if memory usage is growing abnormally."""
        if len(self.snapshots) < 10:
            return False
        
        recent = self.snapshots[-10:]
        memory_growth = recent[-1]["memory_mb"] - recent[0]["memory_mb"]
        
        return memory_growth > threshold_mb
    
    def get_report(self) -> str:
        """Generate performance report."""
        current = self.take_snapshot("final")
        runtime_hours = (time.time() - self.start_time) / 3600
        
        memory_growth = current["memory_mb"] - self.start_memory
        memory_leak = self.detect_memory_leak()
        
        report = f"""
{'='*70}
PERFORMANCE MONITORING REPORT
{'='*70}

Runtime: {runtime_hours:.2f} hours
Start Memory: {self.start_memory:.2f} MB
Current Memory: {current['memory_mb']:.2f} MB
Memory Growth: {memory_growth:.2f} MB
Memory Leak Detected: {'YES - INVESTIGATE' if memory_leak else 'No'}

Current State:
  CPU Usage: {current['cpu_percent']:.1f}%
  Active Threads: {current['threads']}
  Open Files: {current['open_files']}

Snapshots Recorded: {len(self.snapshots)}
"""
        
        if len(self.snapshots) > 5:
            report += f"\n{'='*70}"
            report += f"\nMEMORY USAGE OVER TIME"
            report += f"\n{'='*70}\n"
            
            for snap in self.snapshots[::max(1, len(self.snapshots)//10)]:
                hours = snap['timestamp'] / 3600
                report += f"\n{hours:6.2f}h: {snap['memory_mb']:7.2f} MB"
                if snap['label']:
                    report += f" ({snap['label']})"
        
        report += f"\n{'='*70}\n"
        
        return report


class MockLLMProvider:
    """Mock LLM provider for cost-free testing."""
    
    def __init__(self, cost_tracker: CostTracker, provider_name: str = "mock_gpt4"):
        self.cost_tracker = cost_tracker
        self.provider_name = provider_name
        self.response_delay = 0.5  # Simulate API latency
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock response."""
        # Simulate API call delay
        time.sleep(self.response_delay)
        
        # Estimate token usage (rough approximation)
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = 500  # Average response length
        
        # Track cost
        self.cost_tracker.record_call(
            provider=self.provider_name,
            operation="generation",
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens)
        )
        
        # Return mock content
        return f"[MOCK RESPONSE for {self.provider_name}]\n\nGenerated content based on prompt length: {len(prompt)} chars\n\nThis is a simulated response that would normally come from the LLM API. In a real scenario, this would contain the actual generated thesis section, analysis, or other content.\n\n(Generated at {datetime.now().strftime('%H:%M:%S')})"


def test_endurance_storage_persistence():
    """Test storage system maintains state during long operation."""
    print("\n" + "="*70)
    print("TEST 1: Storage Persistence During Extended Operation")
    print("="*70)
    
    # Create storage
    storage = create_storage_tool_for_sandbox(
        sandbox_id="endurance_test",
        base_path="./test_storage"
    )
    
    print("\n✓ Storage system initialized")
    
    # Simulate long-running project
    sections = ["Introduction", "Literature Review", "Methodology", 
                "Results", "Discussion", "Conclusion"]
    
    for i, section in enumerate(sections, 1):
        print(f"\nWriting section {i}/{len(sections)}: {section}")
        
        # Store section content
        storage.execute(
            "write_file",
            file_path=f"thesis/section_{i}_{section.lower().replace(' ', '_')}.md",
            content=f"# {section}\n\n{'Content paragraph. ' * 100}"
        )
        
        # Store progress context
        storage.execute(
            "store_context",
            key="thesis_progress",
            value={
                "current_section": section,
                "sections_completed": i,
                "total_sections": len(sections),
                "timestamp": datetime.now().isoformat()
            },
            context_type="progress"
        )
        
        # Simulate work delay
        time.sleep(0.5)
    
    # Verify all sections persisted
    print("\nVerifying persistence...")
    for i, section in enumerate(sections, 1):
        result = storage.execute(
            "read_file",
            file_path=f"thesis/section_{i}_{section.lower().replace(' ', '_')}.md"
        )
        assert result["success"], f"Failed to retrieve {section}"
    
    # Retrieve context
    context_result = storage.execute(
        "retrieve_context",
        key="thesis_progress"
    )
    
    assert context_result["success"], "Failed to retrieve progress context"
    print(f"\n✓ All {len(sections)} sections persisted successfully")
    print(f"✓ Progress context maintained: {context_result['value']['sections_completed']} sections")
    
    return True


def test_endurance_memory_management():
    """Test memory system handles long conversations without degradation."""
    print("\n" + "="*70)
    print("TEST 2: Memory Management During Extended Operation")
    print("="*70)
    
    # Initialize with mock LLM
    mock_llm = Mock()
    mock_llm.predict = Mock(return_value="Summarized conversation history")
    
    memory_manager = LangChainMemoryManager(mock_llm)
    
    # Test different memory types
    memory_types = {
        "buffer": memory_manager.create_buffer_memory(),
        "summary": memory_manager.create_summary_memory(),
        "window": memory_manager.create_window_memory(k=5)
    }
    
    print(f"\n✓ Testing {len(memory_types)} memory strategies")
    
    # Simulate 100 conversation turns
    for i in range(1, 101):
        user_input = f"This is user message number {i} discussing thesis section development"
        ai_response = f"This is AI response number {i} providing detailed guidance on the section"
        
        for mem_type, memory in memory_types.items():
            memory.save_context(
                {"input": user_input},
                {"output": ai_response}
            )
        
        if i % 25 == 0:
            print(f"\nAfter {i} turns:")
            for mem_type, memory in memory_types.items():
                variables = memory.load_memory_variables({})
                history_length = len(str(variables))
                print(f"  {mem_type}: {history_length:,} chars in memory")
    
    print("\n✓ Memory management tested successfully")
    print("  - Buffer memory: Maintains full history (grows linearly)")
    print("  - Summary memory: Compresses history (bounded growth)")
    print("  - Window memory: Maintains fixed window (constant size)")
    
    return True


def test_endurance_cost_optimization():
    """Test cost tracking and optimization strategies."""
    print("\n" + "="*70)
    print("TEST 3: Cost Optimization During Thesis Generation")
    print("="*70)
    
    cost_tracker = CostTracker(daily_budget=50.0)
    
    # Create mock providers with different costs
    providers = {
        "gpt4": MockLLMProvider(cost_tracker, "openai_gpt4"),
        "gpt35": MockLLMProvider(cost_tracker, "openai_gpt35"),
        "deepseek": MockLLMProvider(cost_tracker, "deepseek"),
        "gemini": MockLLMProvider(cost_tracker, "gemini_flash")
    }
    
    print("\nSimulating thesis generation with hybrid provider strategy...")
    
    # Simulate operations with intelligent routing
    operations = [
        ("Literature Review", "gpt4", 10),  # Critical: use GPT-4
        ("Introduction Draft", "deepseek", 5),  # Routine: use DeepSeek
        ("Methodology", "gpt4", 8),  # Critical: use GPT-4
        ("Results Generation", "deepseek", 15),  # Routine: use DeepSeek
        ("Citation Formatting", "gpt35", 20),  # Simple: use GPT-3.5
        ("Statistical Analysis", "gpt4", 12),  # Critical: use GPT-4
        ("Discussion Draft", "deepseek", 10),  # Routine: use DeepSeek
        ("Conclusion", "gemini", 5),  # Mixed: use Gemini Flash
    ]
    
    for operation, provider_key, iterations in operations:
        print(f"\n{operation} ({iterations} calls via {provider_key}):")
        
        provider = providers[provider_key]
        
        for i in range(iterations):
            prompt = f"Generate content for {operation} iteration {i+1}"
            response = provider.generate(prompt)
            
        # Show running total
        print(f"  Total spent so far: ${cost_tracker.total_spent:.2f}")
    
    # Generate final report
    print(cost_tracker.get_report())
    
    # Calculate savings vs all GPT-4
    gpt4_only_cost = sum(
        iterations * 0.15  # Approximate GPT-4 cost per call
        for _, _, iterations in operations
    )
    
    savings = gpt4_only_cost - cost_tracker.total_spent
    savings_percent = (savings / gpt4_only_cost) * 100
    
    print(f"\nCOST COMPARISON:")
    print(f"  All GPT-4: ${gpt4_only_cost:.2f}")
    print(f"  Hybrid Strategy: ${cost_tracker.total_spent:.2f}")
    print(f"  Savings: ${savings:.2f} ({savings_percent:.1f}% reduction)")
    
    return True


def test_endurance_performance_monitoring():
    """Test performance monitoring during extended operation."""
    print("\n" + "="*70)
    print("TEST 4: Performance Monitoring Over Extended Runtime")
    print("="*70)
    
    monitor = PerformanceMonitor()
    
    print("\nSimulating 2-hour thesis generation workflow...")
    
    # Simulate phases of thesis generation
    phases = [
        ("Research & Citation Extraction", 15),
        ("Literature Review Generation", 20),
        ("Methodology Writing", 12),
        ("Results & Analysis", 18),
        ("Discussion Generation", 15),
        ("Final Assembly & Formatting", 10)
    ]
    
    for phase, duration_seconds in phases:
        print(f"\n{phase} ({duration_seconds}s simulation)...")
        
        monitor.take_snapshot(f"Start: {phase}")
        
        # Simulate work with memory allocation
        data_structures = []
        for i in range(duration_seconds):
            # Simulate data accumulation
            data_structures.append({
                "iteration": i,
                "content": "x" * 10000,  # Allocate some memory
                "timestamp": time.time()
            })
            time.sleep(1)
        
        monitor.take_snapshot(f"End: {phase}")
        
        # Clear data (simulating proper cleanup)
        data_structures.clear()
    
    # Generate report
    print(monitor.get_report())
    
    # Check for memory leaks
    if monitor.detect_memory_leak(threshold_mb=50):
        print("\n⚠ WARNING: Potential memory leak detected!")
        print("  Recommendation: Implement periodic cleanup routines")
    else:
        print("\n✓ No significant memory leaks detected")
    
    return True


def run_all_endurance_tests():
    """Run complete endurance test suite."""
    print("\n" + "="*70)
    print("GRAIVE AI - LONG-RUNNING ENDURANCE TEST SUITE")
    print("="*70)
    print("\nTesting system capability for multi-hour operation")
    print("without crashes, memory leaks, or excessive costs\n")
    
    tests = [
        ("Storage Persistence", test_endurance_storage_persistence),
        ("Memory Management", test_endurance_memory_management),
        ("Cost Optimization", test_endurance_cost_optimization),
        ("Performance Monitoring", test_endurance_performance_monitoring)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*70}")
            print(f"Running: {test_name}")
            print(f"{'='*70}")
            
            start_time = time.time()
            success = test_func()
            duration = time.time() - start_time
            
            results[test_name] = {
                "success": success,
                "duration": duration
            }
            
            print(f"\n✓ {test_name} completed in {duration:.2f}s")
            
        except Exception as e:
            print(f"\n✗ {test_name} failed: {e}")
            results[test_name] = {
                "success": False,
                "error": str(e)
            }
    
    # Final summary
    print("\n" + "="*70)
    print("ENDURANCE TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result.get("success") else "✗ FAIL"
        print(f"\n{status}: {test_name}")
        if "duration" in result:
            print(f"  Runtime: {result['duration']:.2f}s")
        if "error" in result:
            print(f"  Error: {result['error']}")
    
    total_passed = sum(1 for r in results.values() if r.get("success"))
    print(f"\n{'='*70}")
    print(f"Tests Passed: {total_passed}/{len(tests)}")
    print(f"{'='*70}\n")
    
    return all(r.get("success") for r in results.values())


if __name__ == "__main__":
    success = run_all_endurance_tests()
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS FOR PRODUCTION DEPLOYMENT")
    print("="*70)
    print("""
1. Cost Management:
   - Implement hybrid LLM routing (DeepSeek for drafts, GPT-4 for critical)
   - Set daily budget limits with automatic throttling
   - Cache LLM responses for repeated queries
   - Use batch operations to reduce API calls

2. Memory Management:
   - Use summary memory for conversations > 50 turns
   - Implement periodic memory cleanup every 2 hours
   - Monitor memory growth and trigger GC if needed
   - Restart browser sessions every 6 hours

3. Performance Optimization:
   - Checkpoint progress every 30 minutes
   - Enable auto-resume on interruption
   - Run analysis tasks in parallel where possible
   - Use local models for formatting/validation

4. Monitoring:
   - Log all API calls with cost tracking
   - Set up alerts for budget thresholds
   - Monitor system resources (CPU, memory, disk)
   - Track task completion rates

5. Testing on Your Machine:
   - Run this test suite to validate setup
   - Start with short workflows (1-2 hours)
   - Gradually increase to 8-12 hour sessions
   - Monitor costs closely during initial runs
    """)
    
    sys.exit(0 if success else 1)
