"""
Cost Management and Optimization System

Implements intelligent cost controls for long-running Graive AI operations:
- Budget enforcement and tracking
- Hybrid LLM provider routing
- Response caching
- Token usage monitoring
- Cost estimation and reporting
"""

import os
import json
import hashlib
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class TaskComplexity(Enum):
    """Task complexity levels for intelligent provider routing."""
    SIMPLE = "simple"          # Formatting, citation cleanup
    ROUTINE = "routine"        # Draft generation, summarization
    MODERATE = "moderate"      # Section writing, analysis
    COMPLEX = "complex"        # Research synthesis, methodology
    CRITICAL = "critical"      # Final review, validation


@dataclass
class CostEstimate:
    """Cost estimation for a planned operation."""
    estimated_input_tokens: int
    estimated_output_tokens: int
    recommended_provider: str
    estimated_cost: float
    alternative_providers: List[Dict[str, Any]]
    reasoning: str


@dataclass
class APICallRecord:
    """Record of a single API call."""
    timestamp: str
    provider: str
    model: str
    operation: str
    input_tokens: int
    output_tokens: int
    cost: float
    cached: bool
    task_complexity: str


class ProviderPricing:
    """Current API pricing for different providers."""
    
    PRICING = {
        "openai": {
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000},
            "gpt-3.5-turbo": {"input": 0.0015/1000, "output": 0.002/1000},
            "text-embedding-ada-002": {"input": 0.0001/1000, "output": 0.0}
        },
        "deepseek": {
            "deepseek-chat": {"input": 0.00014/1000, "output": 0.00028/1000},
            "deepseek-coder": {"input": 0.00014/1000, "output": 0.00028/1000}
        },
        "gemini": {
            "gemini-1.5-pro": {"input": 0.00125/1000, "output": 0.005/1000},
            "gemini-1.5-flash": {"input": 0.000075/1000, "output": 0.0003/1000}
        },
        "local": {
            "ollama": {"input": 0.0, "output": 0.0}  # Free local models
        }
    }
    
    @classmethod
    def get_cost(
        cls,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for a provider/model combination."""
        provider_pricing = cls.PRICING.get(provider, {})
        model_pricing = provider_pricing.get(model, {"input": 0.03/1000, "output": 0.06/1000})
        
        cost = (input_tokens * model_pricing["input"]) + (output_tokens * model_pricing["output"])
        return cost
    
    @classmethod
    def compare_providers(
        cls,
        input_tokens: int,
        output_tokens: int,
        providers: List[tuple]  # [(provider, model), ...]
    ) -> List[Dict[str, Any]]:
        """Compare costs across multiple providers."""
        comparisons = []
        
        for provider, model in providers:
            cost = cls.get_cost(provider, model, input_tokens, output_tokens)
            comparisons.append({
                "provider": provider,
                "model": model,
                "cost": cost,
                "cost_per_call": cost
            })
        
        return sorted(comparisons, key=lambda x: x["cost"])


class ResponseCache:
    """Cache LLM responses to avoid redundant API calls."""
    
    def __init__(self, cache_dir: str = "./cache/llm_responses", ttl_hours: int = 168):
        """
        Initialize response cache.
        
        Args:
            cache_dir: Directory for cache storage
            ttl_hours: Time-to-live for cached responses (default: 7 days)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.lock = threading.Lock()
        
        # In-memory cache for frequently used responses
        self.memory_cache = {}
        self.max_memory_cache = 100
    
    def _generate_cache_key(self, prompt: str, provider: str, model: str, **kwargs) -> str:
        """Generate cache key from request parameters."""
        # Create consistent hash from request
        cache_input = {
            "prompt": prompt,
            "provider": provider,
            "model": model,
            **kwargs
        }
        
        cache_string = json.dumps(cache_input, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    def get(
        self,
        prompt: str,
        provider: str,
        model: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if available and not expired."""
        cache_key = self._generate_cache_key(prompt, provider, model, **kwargs)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            cached_data = self.memory_cache[cache_key]
            
            # Check expiration
            cached_time = datetime.fromisoformat(cached_data["timestamp"])
            if datetime.now() - cached_time < self.ttl:
                return cached_data["response"]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with self.lock:
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    # Check expiration
                    cached_time = datetime.fromisoformat(cached_data["timestamp"])
                    if datetime.now() - cached_time < self.ttl:
                        # Add to memory cache
                        if len(self.memory_cache) < self.max_memory_cache:
                            self.memory_cache[cache_key] = cached_data
                        
                        return cached_data["response"]
                    else:
                        # Expired, delete
                        cache_file.unlink()
                
                except Exception:
                    pass
        
        return None
    
    def set(
        self,
        prompt: str,
        provider: str,
        model: str,
        response: Dict[str, Any],
        **kwargs
    ):
        """Cache a response."""
        cache_key = self._generate_cache_key(prompt, provider, model, **kwargs)
        
        cached_data = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt[:500],  # Store truncated prompt for debugging
            "provider": provider,
            "model": model,
            "response": response
        }
        
        # Add to memory cache
        if len(self.memory_cache) < self.max_memory_cache:
            self.memory_cache[cache_key] = cached_data
        
        # Write to disk
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        with self.lock:
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cached_data, f, indent=2)
            except Exception as e:
                print(f"Warning: Failed to cache response: {e}")
    
    def clear_expired(self):
        """Remove expired cache entries."""
        now = datetime.now()
        
        with self.lock:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cached_data["timestamp"])
                    if now - cached_time >= self.ttl:
                        cache_file.unlink()
                
                except Exception:
                    # Delete corrupted cache files
                    cache_file.unlink()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_files = len(list(self.cache_dir.glob("*.json")))
        total_size_mb = sum(f.stat().st_size for f in self.cache_dir.glob("*.json")) / 1024 / 1024
        
        return {
            "memory_cache_entries": len(self.memory_cache),
            "disk_cache_entries": total_files,
            "total_size_mb": round(total_size_mb, 2),
            "cache_directory": str(self.cache_dir)
        }


class CostManager:
    """
    Comprehensive cost management system for Graive AI.
    
    Features:
    - Budget tracking and enforcement
    - Intelligent provider routing
    - Response caching
    - Cost estimation
    - Detailed reporting
    """
    
    def __init__(
        self,
        daily_budget: float = 50.0,
        weekly_budget: float = 200.0,
        enable_caching: bool = True,
        cache_dir: str = "./cache/llm_responses"
    ):
        """
        Initialize cost manager.
        
        Args:
            daily_budget: Maximum daily spend in USD
            weekly_budget: Maximum weekly spend in USD
            enable_caching: Enable response caching
            cache_dir: Directory for cache storage
        """
        self.daily_budget = daily_budget
        self.weekly_budget = weekly_budget
        
        # Cost tracking
        self.call_records: List[APICallRecord] = []
        self.lock = threading.Lock()
        
        # Caching
        self.cache_enabled = enable_caching
        self.cache = ResponseCache(cache_dir=cache_dir) if enable_caching else None
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
    
    def estimate_cost(
        self,
        prompt: str,
        task_complexity: TaskComplexity = TaskComplexity.MODERATE,
        preferred_provider: Optional[str] = None
    ) -> CostEstimate:
        """
        Estimate cost for a task and recommend optimal provider.
        
        Args:
            prompt: Input prompt
            task_complexity: Complexity level
            preferred_provider: User's preferred provider (optional)
        
        Returns:
            Cost estimation with provider recommendation
        """
        # Estimate token counts (rough approximation)
        estimated_input = int(len(prompt.split()) * 1.3)
        
        # Output token estimation based on complexity
        output_estimates = {
            TaskComplexity.SIMPLE: 200,
            TaskComplexity.ROUTINE: 500,
            TaskComplexity.MODERATE: 1000,
            TaskComplexity.COMPLEX: 2000,
            TaskComplexity.CRITICAL: 1500
        }
        estimated_output = output_estimates[task_complexity]
        
        # Get provider options based on complexity
        provider_options = self._get_provider_recommendations(task_complexity)
        
        # Calculate costs for each option
        cost_comparisons = ProviderPricing.compare_providers(
            input_tokens=estimated_input,
            output_tokens=estimated_output,
            providers=provider_options
        )
        
        # Select recommended provider
        if preferred_provider:
            recommended = next(
                (p for p in cost_comparisons if p["provider"] == preferred_provider),
                cost_comparisons[0]
            )
        else:
            recommended = cost_comparisons[0]  # Cheapest option
        
        return CostEstimate(
            estimated_input_tokens=estimated_input,
            estimated_output_tokens=estimated_output,
            recommended_provider=f"{recommended['provider']}/{recommended['model']}",
            estimated_cost=recommended["cost"],
            alternative_providers=cost_comparisons,
            reasoning=self._get_recommendation_reasoning(task_complexity, recommended)
        )
    
    def _get_provider_recommendations(
        self,
        task_complexity: TaskComplexity
    ) -> List[tuple]:
        """Get appropriate provider options based on task complexity."""
        if task_complexity == TaskComplexity.SIMPLE:
            return [
                ("local", "ollama"),
                ("deepseek", "deepseek-chat"),
                ("openai", "gpt-3.5-turbo")
            ]
        
        elif task_complexity == TaskComplexity.ROUTINE:
            return [
                ("deepseek", "deepseek-chat"),
                ("gemini", "gemini-1.5-flash"),
                ("openai", "gpt-3.5-turbo")
            ]
        
        elif task_complexity == TaskComplexity.MODERATE:
            return [
                ("deepseek", "deepseek-chat"),
                ("gemini", "gemini-1.5-flash"),
                ("openai", "gpt-4-turbo")
            ]
        
        elif task_complexity == TaskComplexity.COMPLEX:
            return [
                ("gemini", "gemini-1.5-pro"),
                ("openai", "gpt-4-turbo"),
                ("openai", "gpt-4")
            ]
        
        else:  # CRITICAL
            return [
                ("openai", "gpt-4"),
                ("gemini", "gemini-1.5-pro")
            ]
    
    def _get_recommendation_reasoning(
        self,
        task_complexity: TaskComplexity,
        recommended: Dict[str, Any]
    ) -> str:
        """Generate reasoning for provider recommendation."""
        complexity_reasoning = {
            TaskComplexity.SIMPLE: "Simple task suitable for local/low-cost models",
            TaskComplexity.ROUTINE: "Routine task - DeepSeek offers 99% cost savings vs GPT-4",
            TaskComplexity.MODERATE: "Moderate complexity - balance cost and quality",
            TaskComplexity.COMPLEX: "Complex reasoning required - use advanced models",
            TaskComplexity.CRITICAL: "Critical task - use most capable model for accuracy"
        }
        
        base_reasoning = complexity_reasoning[task_complexity]
        provider_info = f"Recommended: {recommended['provider']} ({recommended['model']}) at ${recommended['cost']:.4f}"
        
        return f"{base_reasoning}. {provider_info}"
    
    def record_call(
        self,
        provider: str,
        model: str,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        task_complexity: TaskComplexity = TaskComplexity.MODERATE,
        cached: bool = False
    ) -> Dict[str, Any]:
        """
        Record an API call and update costs.
        
        Args:
            provider: LLM provider name
            model: Model name
            operation: Operation description
            input_tokens: Input token count
            output_tokens: Output token count
            task_complexity: Task complexity level
            cached: Whether response came from cache
        
        Returns:
            Call record and budget status
        """
        cost = 0.0 if cached else ProviderPricing.get_cost(
            provider, model, input_tokens, output_tokens
        )
        
        record = APICallRecord(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            cached=cached,
            task_complexity=task_complexity.value
        )
        
        with self.lock:
            self.call_records.append(record)
            
            if cached:
                self.cache_hits += 1
            else:
                self.cache_misses += 1
        
        # Check budget status
        daily_spent = self.get_daily_spend()
        weekly_spent = self.get_weekly_spend()
        
        return {
            "cost": cost,
            "cached": cached,
            "daily_spent": daily_spent,
            "daily_remaining": self.daily_budget - daily_spent,
            "daily_budget_exceeded": daily_spent > self.daily_budget,
            "weekly_spent": weekly_spent,
            "weekly_remaining": self.weekly_budget - weekly_spent,
            "weekly_budget_exceeded": weekly_spent > self.weekly_budget
        }
    
    def get_daily_spend(self) -> float:
        """Get total spend for current day."""
        today = datetime.now().date()
        
        with self.lock:
            daily_records = [
                r for r in self.call_records
                if datetime.fromisoformat(r.timestamp).date() == today
            ]
        
        return sum(r.cost for r in daily_records)
    
    def get_weekly_spend(self) -> float:
        """Get total spend for current week."""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        
        with self.lock:
            weekly_records = [
                r for r in self.call_records
                if datetime.fromisoformat(r.timestamp) >= week_start
            ]
        
        return sum(r.cost for r in weekly_records)
    
    def check_budget(self) -> Dict[str, Any]:
        """Check current budget status."""
        daily_spent = self.get_daily_spend()
        weekly_spent = self.get_weekly_spend()
        
        return {
            "daily": {
                "budget": self.daily_budget,
                "spent": daily_spent,
                "remaining": self.daily_budget - daily_spent,
                "percent_used": (daily_spent / self.daily_budget * 100) if self.daily_budget > 0 else 0,
                "exceeded": daily_spent > self.daily_budget
            },
            "weekly": {
                "budget": self.weekly_budget,
                "spent": weekly_spent,
                "remaining": self.weekly_budget - weekly_spent,
                "percent_used": (weekly_spent / self.weekly_budget * 100) if self.weekly_budget > 0 else 0,
                "exceeded": weekly_spent > self.weekly_budget
            }
        }
    
    def get_report(self, detailed: bool = True) -> str:
        """
        Generate comprehensive cost report.
        
        Args:
            detailed: Include detailed breakdown
        
        Returns:
            Formatted cost report
        """
        budget_status = self.check_budget()
        
        report = f"""
{'='*70}
COST MANAGEMENT REPORT
{'='*70}

BUDGET STATUS:
  Daily Budget: ${self.daily_budget:.2f}
  Daily Spent: ${budget_status['daily']['spent']:.2f} ({budget_status['daily']['percent_used']:.1f}% used)
  Daily Remaining: ${budget_status['daily']['remaining']:.2f}
  
  Weekly Budget: ${self.weekly_budget:.2f}
  Weekly Spent: ${budget_status['weekly']['spent']:.2f} ({budget_status['weekly']['percent_used']:.1f}% used)
  Weekly Remaining: ${budget_status['weekly']['remaining']:.2f}

CACHE PERFORMANCE:
  Enabled: {self.cache_enabled}
  Cache Hits: {self.cache_hits}
  Cache Misses: {self.cache_misses}
  Hit Rate: {(self.cache_hits/(self.cache_hits+self.cache_misses)*100) if (self.cache_hits+self.cache_misses) > 0 else 0:.1f}%
"""
        
        if self.cache:
            cache_stats = self.cache.get_stats()
            report += f"""  Cached Responses: {cache_stats['disk_cache_entries']}
  Cache Size: {cache_stats['total_size_mb']:.2f} MB
"""
        
        if detailed and self.call_records:
            # Group by provider
            provider_stats = {}
            complexity_stats = {}
            
            with self.lock:
                for record in self.call_records:
                    # Provider stats
                    key = f"{record.provider}/{record.model}"
                    if key not in provider_stats:
                        provider_stats[key] = {
                            "calls": 0,
                            "cost": 0.0,
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "cached_calls": 0
                        }
                    
                    provider_stats[key]["calls"] += 1
                    provider_stats[key]["cost"] += record.cost
                    provider_stats[key]["input_tokens"] += record.input_tokens
                    provider_stats[key]["output_tokens"] += record.output_tokens
                    if record.cached:
                        provider_stats[key]["cached_calls"] += 1
                    
                    # Complexity stats
                    if record.task_complexity not in complexity_stats:
                        complexity_stats[record.task_complexity] = {
                            "calls": 0,
                            "cost": 0.0
                        }
                    complexity_stats[record.task_complexity]["calls"] += 1
                    complexity_stats[record.task_complexity]["cost"] += record.cost
            
            report += f"\n{'='*70}\nSPENDING BY PROVIDER\n{'='*70}\n"
            
            for provider, stats in sorted(provider_stats.items(), key=lambda x: x[1]["cost"], reverse=True):
                avg_cost = stats["cost"] / stats["calls"] if stats["calls"] > 0 else 0
                report += f"\n{provider}:"
                report += f"\n  Calls: {stats['calls']} ({stats['cached_calls']} cached)"
                report += f"\n  Cost: ${stats['cost']:.4f}"
                report += f"\n  Avg/call: ${avg_cost:.4f}"
                report += f"\n  Tokens: {stats['input_tokens']:,} in, {stats['output_tokens']:,} out"
            
            report += f"\n\n{'='*70}\nSPENDING BY TASK COMPLEXITY\n{'='*70}\n"
            
            for complexity, stats in sorted(complexity_stats.items(), key=lambda x: x[1]["cost"], reverse=True):
                report += f"\n{complexity}:"
                report += f"\n  Calls: {stats['calls']}"
                report += f"\n  Cost: ${stats['cost']:.4f}"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    def export_records(self, filepath: str):
        """Export call records to JSON file."""
        with self.lock:
            records_data = [asdict(r) for r in self.call_records]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "export_timestamp": datetime.now().isoformat(),
                "total_records": len(records_data),
                "daily_budget": self.daily_budget,
                "weekly_budget": self.weekly_budget,
                "records": records_data
            }, f, indent=2)


def create_cost_manager(
    daily_budget: float = 50.0,
    weekly_budget: float = 200.0,
    enable_caching: bool = True
) -> CostManager:
    """
    Create configured cost manager instance.
    
    Args:
        daily_budget: Maximum daily spend
        weekly_budget: Maximum weekly spend
        enable_caching: Enable response caching
    
    Returns:
        Configured CostManager instance
    """
    return CostManager(
        daily_budget=daily_budget,
        weekly_budget=weekly_budget,
        enable_caching=enable_caching
    )
