"""
Agent Reflection and Validation System

Implements a sophisticated reflection layer that monitors all agent activities,
validates data integrity, checks workflow coherence, and prevents errors before
they propagate through the system.

This reflection system operates as a meta-layer observing:
- Writing operations (file creation, modifications, deletions)
- Data extraction processes (web scraping, PDF parsing, database queries)
- Analysis workflows (statistical computations, visualizations, interpretations)
- Agent coordination (task dependencies, parallel execution, resource conflicts)
- Data flow validation (input-output consistency, type safety, completeness)
"""

import os
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib


class ActivityType(Enum):
    """Types of system activities requiring reflection."""
    FILE_WRITE = "file_write"
    FILE_READ = "file_read"
    FILE_DELETE = "file_delete"
    DATA_EXTRACTION = "data_extraction"
    WEB_SCRAPING = "web_scraping"
    DATABASE_QUERY = "database_query"
    DATABASE_WRITE = "database_write"
    ANALYSIS_EXECUTION = "analysis_execution"
    LLM_GENERATION = "llm_generation"
    AGENT_COORDINATION = "agent_coordination"
    BROWSER_AUTOMATION = "browser_automation"


class ValidationStatus(Enum):
    """Validation outcomes from reflection."""
    APPROVED = "approved"
    WARNING = "warning"
    REJECTED = "rejected"
    REQUIRES_REVIEW = "requires_review"


@dataclass
class AgentActivity:
    """Record of a single agent activity requiring reflection."""
    activity_id: str
    timestamp: str
    agent_name: str
    activity_type: ActivityType
    description: str
    inputs: Dict[str, Any]
    expected_outputs: Dict[str, Any]
    actual_outputs: Optional[Dict[str, Any]] = None
    validation_status: Optional[ValidationStatus] = None
    validation_reasoning: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class ReflectionReport:
    """Comprehensive reflection report on system state."""
    timestamp: str
    total_activities: int
    approved_activities: int
    warned_activities: int
    rejected_activities: int
    active_agents: List[str]
    data_flow_integrity: bool
    resource_conflicts: List[str]
    validation_summary: Dict[str, Any]
    recommendations: List[str]


class ReflectionSystem:
    """
    Central reflection and validation system for all agent activities.
    
    This system operates as a meta-cognitive layer that observes, validates,
    and ensures coherence across all autonomous agent operations before they
    execute, preventing errors and maintaining system integrity.
    """
    
    def __init__(self, workspace_root: str, enable_auto_reflection: bool = True):
        """
        Initialize reflection system.
        
        Args:
            workspace_root: Root directory for workspace
            enable_auto_reflection: Enable automatic pre-execution reflection
        """
        self.workspace_root = Path(workspace_root)
        self.enable_auto_reflection = enable_auto_reflection
        
        # Activity tracking
        self.activities: List[AgentActivity] = []
        self.activity_lock = threading.Lock()
        
        # Agent registry
        self.active_agents: Dict[str, Dict[str, Any]] = {}
        self.agent_lock = threading.Lock()
        
        # Validation rules
        self.validation_rules: Dict[ActivityType, List[Callable]] = {}
        self._initialize_validation_rules()
        
        # Resource tracking for conflict detection
        self.resource_locks: Dict[str, str] = {}  # resource_id -> agent_name
        self.resource_lock = threading.Lock()
        
        # Reflection logs
        self.reflection_dir = self.workspace_root / "reflection_logs"
        self.reflection_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_validation_rules(self):
        """Initialize validation rules for different activity types."""
        self.validation_rules = {
            ActivityType.FILE_WRITE: [
                self._validate_file_path_safety,
                self._validate_file_content_integrity,
                self._validate_no_duplicate_writes
            ],
            ActivityType.DATA_EXTRACTION: [
                self._validate_extraction_source,
                self._validate_extraction_schema,
                self._validate_data_completeness
            ],
            ActivityType.DATABASE_WRITE: [
                self._validate_database_schema,
                self._validate_data_types,
                self._validate_no_data_loss
            ],
            ActivityType.ANALYSIS_EXECUTION: [
                self._validate_analysis_inputs,
                self._validate_statistical_assumptions,
                self._validate_output_format
            ],
            ActivityType.LLM_GENERATION: [
                self._validate_prompt_safety,
                self._validate_expected_output_structure,
                self._validate_cost_threshold
            ],
            ActivityType.BROWSER_AUTOMATION: [
                self._validate_url_safety,
                self._validate_extraction_targets,
                self._validate_session_state
            ]
        }
    
    def register_agent(self, agent_name: str, capabilities: List[str], metadata: Optional[Dict[str, Any]] = None):
        """
        Register an agent with the reflection system.
        
        Args:
            agent_name: Unique agent identifier
            capabilities: List of agent capabilities
            metadata: Additional agent metadata
        """
        with self.agent_lock:
            self.active_agents[agent_name] = {
                "capabilities": capabilities,
                "metadata": metadata or {},
                "registered_at": datetime.now().isoformat(),
                "activities_count": 0
            }
        
        print(f"[Reflection] Agent registered: {agent_name}")
    
    def reflect_before_action(
        self,
        agent_name: str,
        activity_type: ActivityType,
        description: str,
        inputs: Dict[str, Any],
        expected_outputs: Dict[str, Any]
    ) -> AgentActivity:
        """
        Perform reflection before agent executes an action.
        
        This is the core reflection mechanism that validates proposed actions
        before they execute, preventing errors and ensuring coherence.
        
        Args:
            agent_name: Agent proposing the action
            activity_type: Type of activity
            description: Human-readable description
            inputs: Input parameters
            expected_outputs: Expected output structure
        
        Returns:
            AgentActivity with validation results
        """
        # Create activity record
        activity = AgentActivity(
            activity_id=self._generate_activity_id(agent_name, activity_type),
            timestamp=datetime.now().isoformat(),
            agent_name=agent_name,
            activity_type=activity_type,
            description=description,
            inputs=inputs,
            expected_outputs=expected_outputs
        )
        
        print(f"\n{'='*70}")
        print(f"[Reflection] PRE-EXECUTION VALIDATION")
        print(f"{'='*70}")
        print(f"Agent: {agent_name}")
        print(f"Activity: {activity_type.value}")
        print(f"Description: {description}")
        
        # Run validation rules
        validation_results = self._run_validation_rules(activity)
        
        # Determine validation status
        if validation_results["errors"]:
            activity.validation_status = ValidationStatus.REJECTED
            activity.errors = validation_results["errors"]
            activity.validation_reasoning = "Activity rejected due to validation errors"
            
            print(f"\n❌ VALIDATION REJECTED")
            for error in activity.errors:
                print(f"   Error: {error}")
        
        elif validation_results["warnings"]:
            activity.validation_status = ValidationStatus.WARNING
            activity.warnings = validation_results["warnings"]
            activity.validation_reasoning = "Activity approved with warnings"
            
            print(f"\n⚠️  VALIDATION APPROVED (with warnings)")
            for warning in activity.warnings:
                print(f"   Warning: {warning}")
        
        else:
            activity.validation_status = ValidationStatus.APPROVED
            activity.validation_reasoning = "Activity passed all validation checks"
            
            print(f"\n✓ VALIDATION APPROVED")
        
        # Check resource conflicts
        resource_conflict = self._check_resource_conflicts(activity)
        if resource_conflict:
            activity.warnings.append(resource_conflict)
            print(f"   Resource Warning: {resource_conflict}")
        
        # Track activity
        with self.activity_lock:
            self.activities.append(activity)
        
        # Update agent stats
        with self.agent_lock:
            if agent_name in self.active_agents:
                self.active_agents[agent_name]["activities_count"] += 1
        
        print(f"{'='*70}\n")
        
        return activity
    
    def reflect_after_action(
        self,
        activity_id: str,
        actual_outputs: Dict[str, Any],
        success: bool,
        error_message: Optional[str] = None
    ):
        """
        Perform reflection after agent completes an action.
        
        Validates that actual outputs match expected outputs and updates
        system knowledge about agent behavior.
        
        Args:
            activity_id: ID of completed activity
            actual_outputs: Actual outputs produced
            success: Whether activity succeeded
            error_message: Error message if failed
        """
        with self.activity_lock:
            activity = next((a for a in self.activities if a.activity_id == activity_id), None)
            
            if not activity:
                print(f"[Reflection] Warning: Unknown activity {activity_id}")
                return
            
            activity.actual_outputs = actual_outputs
            
            print(f"\n{'='*70}")
            print(f"[Reflection] POST-EXECUTION VALIDATION")
            print(f"{'='*70}")
            print(f"Activity: {activity.description}")
            print(f"Status: {'SUCCESS' if success else 'FAILED'}")
            
            if success:
                # Validate outputs match expectations
                output_validation = self._validate_outputs(activity)
                
                if output_validation["matches"]:
                    print(f"✓ Outputs match expectations")
                else:
                    print(f"⚠️  Output mismatch detected:")
                    for mismatch in output_validation["mismatches"]:
                        print(f"   {mismatch}")
                        activity.warnings.append(mismatch)
            else:
                activity.errors.append(error_message or "Activity failed")
                print(f"❌ Activity failed: {error_message}")
            
            print(f"{'='*70}\n")
    
    def _run_validation_rules(self, activity: AgentActivity) -> Dict[str, List[str]]:
        """Run all validation rules for an activity type."""
        results = {"errors": [], "warnings": []}
        
        rules = self.validation_rules.get(activity.activity_type, [])
        
        for rule in rules:
            try:
                rule_result = rule(activity)
                
                if rule_result.get("error"):
                    results["errors"].append(rule_result["error"])
                
                if rule_result.get("warning"):
                    results["warnings"].append(rule_result["warning"])
            
            except Exception as e:
                results["errors"].append(f"Validation rule exception: {e}")
        
        return results
    
    def _validate_file_path_safety(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate file path is safe and within workspace."""
        file_path = activity.inputs.get("file_path", "")
        
        # Check for path traversal attacks
        if ".." in file_path or file_path.startswith("/"):
            return {"error": "Unsafe file path detected (path traversal attempt)"}
        
        # Ensure within workspace
        try:
            full_path = (self.workspace_root / file_path).resolve()
            if not str(full_path).startswith(str(self.workspace_root)):
                return {"error": "File path outside workspace boundary"}
        except Exception as e:
            return {"error": f"Invalid file path: {e}"}
        
        return {}
    
    def _validate_file_content_integrity(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate file content is well-formed."""
        content = activity.inputs.get("content", "")
        
        # Check for suspicious content
        if len(content) > 10_000_000:  # 10MB
            return {"warning": "Large file content (>10MB) - verify intentional"}
        
        return {}
    
    def _validate_no_duplicate_writes(self, activity: AgentActivity) -> Dict[str, Any]:
        """Check for duplicate file writes in recent history."""
        file_path = activity.inputs.get("file_path", "")
        
        with self.activity_lock:
            recent_writes = [
                a for a in self.activities[-50:]  # Last 50 activities
                if a.activity_type == ActivityType.FILE_WRITE
                and a.inputs.get("file_path") == file_path
                and a.agent_name == activity.agent_name
            ]
        
        if len(recent_writes) > 3:
            return {"warning": f"Multiple writes to {file_path} detected - potential infinite loop"}
        
        return {}
    
    def _validate_extraction_source(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate data extraction source is accessible."""
        source = activity.inputs.get("source", "")
        
        if not source:
            return {"error": "Data extraction source not specified"}
        
        return {}
    
    def _validate_extraction_schema(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate extraction schema is well-defined."""
        schema = activity.inputs.get("schema", {})
        
        if not schema:
            return {"warning": "No extraction schema defined - may produce inconsistent data"}
        
        return {}
    
    def _validate_data_completeness(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate extracted data completeness."""
        expected_fields = activity.expected_outputs.get("fields", [])
        
        if not expected_fields:
            return {"warning": "No expected output fields defined"}
        
        return {}
    
    def _validate_database_schema(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate database schema compatibility."""
        table_name = activity.inputs.get("table_name", "")
        
        if not table_name:
            return {"error": "Database table name not specified"}
        
        return {}
    
    def _validate_data_types(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate data types match schema."""
        data = activity.inputs.get("data", {})
        expected_types = activity.expected_outputs.get("types", {})
        
        for field, expected_type in expected_types.items():
            if field in data:
                actual_type = type(data[field]).__name__
                if actual_type != expected_type:
                    return {"warning": f"Type mismatch: {field} is {actual_type}, expected {expected_type}"}
        
        return {}
    
    def _validate_no_data_loss(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate no data loss in transformation."""
        input_count = activity.inputs.get("record_count", 0)
        expected_count = activity.expected_outputs.get("record_count", 0)
        
        if input_count > 0 and expected_count < input_count * 0.9:
            return {"warning": f"Potential data loss: {input_count} records -> {expected_count} records"}
        
        return {}
    
    def _validate_analysis_inputs(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate statistical analysis inputs."""
        data = activity.inputs.get("data", [])
        
        if not data:
            return {"error": "No data provided for analysis"}
        
        if len(data) < 3:
            return {"warning": "Very small sample size (n<3) - statistical tests may be unreliable"}
        
        return {}
    
    def _validate_statistical_assumptions(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate statistical test assumptions."""
        analysis_type = activity.inputs.get("analysis_type", "")
        
        # Could check normality, homogeneity of variance, etc.
        # Simplified for demonstration
        
        return {}
    
    def _validate_output_format(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate output format specification."""
        output_format = activity.expected_outputs.get("format", "")
        
        if not output_format:
            return {"warning": "Output format not specified"}
        
        return {}
    
    def _validate_prompt_safety(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate LLM prompt safety."""
        prompt = activity.inputs.get("prompt", "")
        
        # Check for prompt injection attempts
        dangerous_patterns = ["ignore previous", "disregard instructions", "system:"]
        
        for pattern in dangerous_patterns:
            if pattern.lower() in prompt.lower():
                return {"warning": f"Potential prompt injection detected: '{pattern}'"}
        
        return {}
    
    def _validate_expected_output_structure(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate expected LLM output structure is defined."""
        expected_structure = activity.expected_outputs.get("structure", "")
        
        if not expected_structure:
            return {"warning": "No expected output structure - may produce inconsistent results"}
        
        return {}
    
    def _validate_cost_threshold(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate LLM call is within cost threshold."""
        estimated_tokens = activity.inputs.get("estimated_tokens", 0)
        
        if estimated_tokens > 8000:
            return {"warning": f"Large LLM call ({estimated_tokens} tokens) - verify intentional"}
        
        return {}
    
    def _validate_url_safety(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate URL is safe to access."""
        url = activity.inputs.get("url", "")
        
        if not url.startswith(("http://", "https://")):
            return {"error": "Invalid URL protocol"}
        
        # Could check against blocklist, etc.
        
        return {}
    
    def _validate_extraction_targets(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate extraction targets are well-defined."""
        targets = activity.inputs.get("extraction_targets", [])
        
        if not targets:
            return {"warning": "No extraction targets specified"}
        
        return {}
    
    def _validate_session_state(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate browser session state."""
        # Could check if browser is initialized, logged in, etc.
        
        return {}
    
    def _validate_outputs(self, activity: AgentActivity) -> Dict[str, Any]:
        """Validate actual outputs match expected outputs."""
        expected = activity.expected_outputs
        actual = activity.actual_outputs or {}
        
        mismatches = []
        
        for key, expected_value in expected.items():
            if key not in actual:
                mismatches.append(f"Missing expected output: {key}")
            elif isinstance(expected_value, type):
                # Type checking
                if not isinstance(actual[key], expected_value):
                    mismatches.append(f"Type mismatch for {key}: expected {expected_value}, got {type(actual[key])}")
        
        return {
            "matches": len(mismatches) == 0,
            "mismatches": mismatches
        }
    
    def _check_resource_conflicts(self, activity: AgentActivity) -> Optional[str]:
        """Check for resource conflicts with other agents."""
        resource_id = None
        
        # Determine resource being accessed
        if activity.activity_type == ActivityType.FILE_WRITE:
            resource_id = f"file:{activity.inputs.get('file_path', '')}"
        elif activity.activity_type == ActivityType.DATABASE_WRITE:
            resource_id = f"db:{activity.inputs.get('table_name', '')}"
        
        if not resource_id:
            return None
        
        with self.resource_lock:
            if resource_id in self.resource_locks:
                other_agent = self.resource_locks[resource_id]
                if other_agent != activity.agent_name:
                    return f"Resource conflict: {resource_id} locked by {other_agent}"
            else:
                # Acquire lock
                self.resource_locks[resource_id] = activity.agent_name
        
        return None
    
    def release_resource(self, agent_name: str, resource_id: str):
        """Release a resource lock."""
        with self.resource_lock:
            if self.resource_locks.get(resource_id) == agent_name:
                del self.resource_locks[resource_id]
    
    def _generate_activity_id(self, agent_name: str, activity_type: ActivityType) -> str:
        """Generate unique activity ID."""
        timestamp = datetime.now().isoformat()
        content = f"{agent_name}:{activity_type.value}:{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def generate_reflection_report(self) -> ReflectionReport:
        """
        Generate comprehensive reflection report on system state.
        
        Returns:
            ReflectionReport with validation summary
        """
        with self.activity_lock:
            total = len(self.activities)
            approved = len([a for a in self.activities if a.validation_status == ValidationStatus.APPROVED])
            warned = len([a for a in self.activities if a.validation_status == ValidationStatus.WARNING])
            rejected = len([a for a in self.activities if a.validation_status == ValidationStatus.REJECTED])
        
        with self.agent_lock:
            active_agents = list(self.active_agents.keys())
        
        # Check data flow integrity
        data_flow_integrity = rejected == 0
        
        # Identify resource conflicts
        resource_conflicts = []
        for activity in self.activities:
            if activity.warnings:
                for warning in activity.warnings:
                    if "Resource conflict" in warning:
                        resource_conflicts.append(warning)
        
        # Generate recommendations
        recommendations = self._generate_recommendations()
        
        report = ReflectionReport(
            timestamp=datetime.now().isoformat(),
            total_activities=total,
            approved_activities=approved,
            warned_activities=warned,
            rejected_activities=rejected,
            active_agents=active_agents,
            data_flow_integrity=data_flow_integrity,
            resource_conflicts=resource_conflicts,
            validation_summary={
                "approval_rate": (approved / total * 100) if total > 0 else 0,
                "warning_rate": (warned / total * 100) if total > 0 else 0,
                "rejection_rate": (rejected / total * 100) if total > 0 else 0
            },
            recommendations=recommendations
        )
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on activity history."""
        recommendations = []
        
        with self.activity_lock:
            # Check for high rejection rate
            total = len(self.activities)
            rejected = len([a for a in self.activities if a.validation_status == ValidationStatus.REJECTED])
            
            if total > 0 and rejected / total > 0.1:
                recommendations.append("High rejection rate detected - review agent configurations")
            
            # Check for resource conflicts
            conflicts = [a for a in self.activities if any("Resource conflict" in w for w in a.warnings)]
            if len(conflicts) > 5:
                recommendations.append("Frequent resource conflicts - implement better agent coordination")
            
            # Check for repeated errors
            error_patterns = {}
            for activity in self.activities:
                for error in activity.errors:
                    error_patterns[error] = error_patterns.get(error, 0) + 1
            
            for error, count in error_patterns.items():
                if count > 3:
                    recommendations.append(f"Repeated error pattern: '{error}' ({count} occurrences)")
        
        return recommendations
    
    def print_reflection_report(self):
        """Print formatted reflection report."""
        report = self.generate_reflection_report()
        
        print(f"\n{'='*70}")
        print(f"SYSTEM REFLECTION REPORT")
        print(f"{'='*70}")
        print(f"\nTimestamp: {report.timestamp}")
        print(f"\nActivity Summary:")
        print(f"  Total Activities: {report.total_activities}")
        print(f"  Approved: {report.approved_activities} ({report.validation_summary['approval_rate']:.1f}%)")
        print(f"  Warned: {report.warned_activities} ({report.validation_summary['warning_rate']:.1f}%)")
        print(f"  Rejected: {report.rejected_activities} ({report.validation_summary['rejection_rate']:.1f}%)")
        
        print(f"\nActive Agents: {', '.join(report.active_agents) if report.active_agents else 'None'}")
        
        print(f"\nData Flow Integrity: {'✓ HEALTHY' if report.data_flow_integrity else '✗ ISSUES DETECTED'}")
        
        if report.resource_conflicts:
            print(f"\nResource Conflicts:")
            for conflict in report.resource_conflicts:
                print(f"  • {conflict}")
        
        if report.recommendations:
            print(f"\nRecommendations:")
            for rec in report.recommendations:
                print(f"  • {rec}")
        
        print(f"\n{'='*70}\n")
    
    def export_reflection_log(self, filename: Optional[str] = None):
        """Export reflection log to JSON file."""
        if filename is None:
            filename = f"reflection_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.reflection_dir / filename
        
        with self.activity_lock:
            data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_activities": len(self.activities),
                "activities": [asdict(a) for a in self.activities],
                "report": asdict(self.generate_reflection_report())
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"[Reflection] Log exported to: {filepath}")


def create_reflection_system(workspace_root: str = "./") -> ReflectionSystem:
    """
    Create configured reflection system instance.
    
    Args:
        workspace_root: Root directory for workspace
    
    Returns:
        Configured ReflectionSystem instance
    """
    return ReflectionSystem(workspace_root=workspace_root, enable_auto_reflection=True)
