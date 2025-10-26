"""Execution module for autonomous task processing."""

from .task_executor import TaskExecutor, create_task_executor

__all__ = [
    'TaskExecutor',
    'create_task_executor'
]
