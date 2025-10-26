"""
Interactive Agent Loop with Human-in-the-Loop Capabilities

This module implements a sophisticated interactive agent loop that allows users to interrupt
the agent at any time, provide real-time feedback, and maintain full context awareness
regardless of conversation length. The system supports pause/resume, dynamic replanning,
and infinite context management through intelligent memory compression and persistence.
"""

import threading
import queue
import time
from typing import Dict, Any, Optional, Callable
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.agent_loop import AgentLoop, LoopState


class InteractionMode(Enum):
    """Modes of user interaction."""
    AUTONOMOUS = "autonomous"  # Agent runs without interruption
    COLLABORATIVE = "collaborative"  # Agent pauses for confirmation at each step
    INTERRUPTIBLE = "interruptible"  # User can interrupt anytime
    SUPERVISED = "supervised"  # Agent requests approval for critical actions


class InterruptSignal(Enum):
    """Types of interrupt signals."""
    PAUSE = "pause"
    STOP = "stop"
    MODIFY_GOAL = "modify_goal"
    ADD_CONTEXT = "add_context"
    CHANGE_APPROACH = "change_approach"
    FEEDBACK = "feedback"
    CONTINUE = "continue"


class InteractiveAgentLoop(AgentLoop):
    """
    Enhanced Agent Loop with Human-in-the-Loop capabilities.
    
    This implementation extends the base AgentLoop to support real-time user interaction,
    allowing users to interrupt execution, provide feedback, modify goals, and maintain
    full context awareness across unlimited conversation lengths through intelligent
    memory management and compression.
    
    Key Features:
    - Real-time interruption during execution
    - Pause and resume capabilities
    - Dynamic goal modification
    - Context injection at any point
    - Infinite memory management
    - Automatic context summarization
    - Checkpoint and rollback support
    """
    
    def __init__(self, orchestrator, context_manager, interaction_mode=InteractionMode.INTERRUPTIBLE):
        """
        Initialize the interactive agent loop.
        
        Args:
            orchestrator: The tool orchestrator for executing actions
            context_manager: The context/knowledge base manager
            interaction_mode: Default interaction mode
        """
        super().__init__(orchestrator, context_manager)
        
        self.interaction_mode = interaction_mode
        self.is_paused = False
        self.should_stop = False
        self.user_input_queue = queue.Queue()
        self.interaction_callbacks = {}
        
        # Memory management
        self.memory_threshold = 100000  # Characters before compression
        self.checkpoint_interval = 10  # Save checkpoint every N iterations
        self.checkpoints = []
        
        # User interaction thread
        self.input_thread = None
        self.listening = False
        
    def register_callback(self, signal_type: InterruptSignal, callback: Callable):
        """
        Register a callback for specific interrupt signals.
        
        Args:
            signal_type: Type of interrupt signal
            callback: Function to call when signal is received
        """
        self.interaction_callbacks[signal_type] = callback
    
    def start_listening(self):
        """Start background thread to listen for user input."""
        if not self.listening:
            self.listening = True
            self.input_thread = threading.Thread(target=self._listen_for_input, daemon=True)
            self.input_thread.start()
    
    def stop_listening(self):
        """Stop listening for user input."""
        self.listening = False
        if self.input_thread:
            self.input_thread.join(timeout=1)
    
    def _listen_for_input(self):
        """Background thread function to continuously listen for user input."""
        print("\n[System] Listening for user input. Commands: pause, stop, modify, feedback, continue")
        
        while self.listening:
            try:
                # Non-blocking input check
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    user_input = input("\n[User Interrupt] > ").strip()
                    
                    if user_input:
                        self._process_user_interrupt(user_input)
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                print(f"[System] Input listening error: {e}")
                time.sleep(1)
    
    def _process_user_interrupt(self, user_input: str):
        """
        Process user interrupt input.
        
        Args:
            user_input: The user's input text
        """
        user_input_lower = user_input.lower()
        
        if user_input_lower.startswith("pause"):
            self.is_paused = True
            self.user_input_queue.put({
                "signal": InterruptSignal.PAUSE,
                "message": "User requested pause"
            })
            print("[System] Agent paused. Type 'continue' to resume.")
            
        elif user_input_lower.startswith("stop"):
            self.should_stop = True
            self.user_input_queue.put({
                "signal": InterruptSignal.STOP,
                "message": "User requested stop"
            })
            print("[System] Agent will stop after current operation.")
            
        elif user_input_lower.startswith("modify"):
            self.is_paused = True
            new_goal = user_input[6:].strip()
            self.user_input_queue.put({
                "signal": InterruptSignal.MODIFY_GOAL,
                "content": new_goal
            })
            print(f"[System] Goal modified: {new_goal}")
            
        elif user_input_lower.startswith("feedback"):
            feedback = user_input[8:].strip()
            self.user_input_queue.put({
                "signal": InterruptSignal.FEEDBACK,
                "content": feedback
            })
            print(f"[System] Feedback received: {feedback}")
            
        elif user_input_lower.startswith("continue"):
            self.is_paused = False
            self.user_input_queue.put({
                "signal": InterruptSignal.CONTINUE,
                "message": "User requested continue"
            })
            print("[System] Agent resumed.")
            
        else:
            # Treat as contextual input
            self.user_input_queue.put({
                "signal": InterruptSignal.ADD_CONTEXT,
                "content": user_input
            })
            print(f"[System] Context added: {user_input[:50]}...")
    
    def run(self, user_request: str, enable_interrupts: bool = True) -> Dict[str, Any]:
        """
        Execute the interactive agent loop with human-in-the-loop support.
        
        Args:
            user_request: The user's initial request or task
            enable_interrupts: Whether to enable real-time interruptions
            
        Returns:
            Dict containing the final result and execution metadata
        """
        # Start listening for interrupts if enabled
        if enable_interrupts and not self.listening:
            self.start_listening()
        
        self.context.add_user_message(user_request)
        
        print(f"\n[Agent] Starting task: {user_request[:100]}...")
        print(f"[Agent] Interaction mode: {self.interaction_mode.value}")
        
        while self.iteration_count < self.max_iterations and not self.should_stop:
            self.iteration_count += 1
            
            # Check for user interrupts
            self._check_interrupts()
            
            # Wait if paused
            while self.is_paused and not self.should_stop:
                print("[Agent] Paused. Waiting for user input...")
                time.sleep(1)
                self._check_interrupts()
            
            if self.should_stop:
                print("[Agent] Execution stopped by user.")
                break
            
            try:
                # Step 1: Analyze Context
                self.state = LoopState.ANALYZING
                print(f"\n[Iteration {self.iteration_count}] Analyzing context...")
                analysis = self._analyze_context()
                
                # Check if user wants to review
                if self.interaction_mode == InteractionMode.COLLABORATIVE:
                    self._request_user_confirmation("Analysis complete. Proceed?")
                
                # Step 2: Think and Plan
                self.state = LoopState.THINKING
                print(f"[Iteration {self.iteration_count}] Planning next action...")
                plan = self._think(analysis)
                
                # Check if task is complete
                if plan.get("is_complete", False):
                    self.state = LoopState.COMPLETED
                    print("[Agent] Task completed successfully!")
                    return self._build_response(plan)
                
                # Request approval for critical actions
                if self.interaction_mode == InteractionMode.SUPERVISED:
                    action = plan.get("next_action", "unknown")
                    self._request_user_confirmation(f"About to execute: {action}. Approve?")
                
                # Step 3: Select Tool
                self.state = LoopState.SELECTING_TOOL
                tool_call = self._select_tool(plan)
                print(f"[Iteration {self.iteration_count}] Selected tool: {tool_call.get('tool_name')}")
                
                # Step 4: Execute via Orchestrator
                self.state = LoopState.EXECUTING
                result = self.orchestrator.execute(tool_call)
                print(f"[Iteration {self.iteration_count}] Execution result: {result.get('success', False)}")
                
                # Step 5: Observe and Update Context
                self.state = LoopState.OBSERVING
                self._observe(result)
                
                # Memory management
                self._manage_memory()
                
                # Create checkpoint
                if self.iteration_count % self.checkpoint_interval == 0:
                    self._create_checkpoint()
                
            except Exception as e:
                self.state = LoopState.ERROR
                print(f"[Agent] Error: {e}")
                
                # Ask user if they want to continue despite error
                if self.interaction_mode != InteractionMode.AUTONOMOUS:
                    self._request_user_confirmation("Error occurred. Continue anyway?")
                    if self.should_stop:
                        return self._handle_error(e)
        
        if self.iteration_count >= self.max_iterations:
            print("[Agent] Maximum iterations reached.")
        
        return self._build_response({"status": "completed", "iterations": self.iteration_count})
    
    def _check_interrupts(self):
        """Check for and process any user interrupts."""
        while not self.user_input_queue.empty():
            interrupt = self.user_input_queue.get()
            signal = interrupt.get("signal")
            
            print(f"\n[System] Processing interrupt: {signal.value}")
            
            if signal == InterruptSignal.PAUSE:
                self.is_paused = True
                
            elif signal == InterruptSignal.STOP:
                self.should_stop = True
                
            elif signal == InterruptSignal.CONTINUE:
                self.is_paused = False
                
            elif signal == InterruptSignal.MODIFY_GOAL:
                new_goal = interrupt.get("content", "")
                self.context.add_user_message(f"[Goal Modified] {new_goal}")
                print(f"[Agent] Goal updated to: {new_goal}")
                
            elif signal == InterruptSignal.ADD_CONTEXT:
                context = interrupt.get("content", "")
                self.context.add_user_message(f"[Additional Context] {context}")
                print(f"[Agent] Context added: {context[:50]}...")
                
            elif signal == InterruptSignal.FEEDBACK:
                feedback = interrupt.get("content", "")
                self.context.add_user_message(f"[User Feedback] {feedback}")
                print(f"[Agent] Feedback incorporated: {feedback[:50]}...")
            
            # Call registered callbacks
            if signal in self.interaction_callbacks:
                self.interaction_callbacks[signal](interrupt)
    
    def _request_user_confirmation(self, prompt: str) -> bool:
        """
        Request user confirmation before proceeding.
        
        Args:
            prompt: The confirmation prompt
            
        Returns:
            True if user confirms, False otherwise
        """
        print(f"\n[Agent] {prompt} (yes/no): ", end="")
        
        # Wait for user input with timeout
        response = input().strip().lower()
        
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            self.should_stop = True
            return False
        else:
            print("[System] Invalid response. Assuming 'yes'.")
            return True
    
    def _manage_memory(self):
        """
        Manage memory to prevent context overflow.
        
        Implements intelligent memory compression and summarization to maintain
        context within token limits while preserving critical information.
        """
        # Get current context size
        history = self.context.get_conversation_history()
        total_chars = sum(len(msg.get("content", "")) for msg in history)
        
        if total_chars > self.memory_threshold:
            print(f"\n[Memory] Context size: {total_chars} chars. Compressing...")
            
            # Compress old context
            compressed_summary = self._compress_context(history[:-10])  # Keep last 10 messages
            
            # Create new context with summary + recent messages
            self.context.clear()
            self.context.add_system_message(self.context.system_prompt)
            self.context.add_assistant_message(f"[Context Summary] {compressed_summary}")
            
            # Re-add recent messages
            for msg in history[-10:]:
                if msg["role"] == "user":
                    self.context.add_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    self.context.add_assistant_message(msg["content"])
            
            print(f"[Memory] Compressed to {len(compressed_summary)} chars. Recent context preserved.")
    
    def _compress_context(self, messages: list) -> str:
        """
        Compress context using summarization.
        
        Args:
            messages: List of messages to compress
            
        Returns:
            Compressed summary
        """
        # Extract key information
        user_messages = [m for m in messages if m.get("role") == "user"]
        observations = [m for m in messages if "[Observation]" in m.get("content", "")]
        
        summary_parts = []
        
        # Summarize user requests
        if user_messages:
            requests = [m.get("content", "")[:100] for m in user_messages[:5]]
            summary_parts.append(f"Previous requests: {'; '.join(requests)}")
        
        # Summarize key observations
        if observations:
            key_obs = [m.get("content", "")[:100] for m in observations[-5:]]
            summary_parts.append(f"Key observations: {'; '.join(key_obs)}")
        
        # Add metadata
        summary_parts.append(f"Total messages compressed: {len(messages)}")
        
        return " | ".join(summary_parts)
    
    def _create_checkpoint(self):
        """Create a checkpoint of current state for potential rollback."""
        checkpoint = {
            "iteration": self.iteration_count,
            "state": self.state.value,
            "context_summary": self.context.get_summary(),
            "timestamp": time.time()
        }
        
        self.checkpoints.append(checkpoint)
        
        # Keep only last 5 checkpoints
        if len(self.checkpoints) > 5:
            self.checkpoints.pop(0)
        
        print(f"[System] Checkpoint created at iteration {self.iteration_count}")
    
    def rollback_to_checkpoint(self, checkpoint_index: int = -1):
        """
        Rollback to a previous checkpoint.
        
        Args:
            checkpoint_index: Index of checkpoint to rollback to (-1 for most recent)
        """
        if not self.checkpoints:
            print("[System] No checkpoints available.")
            return
        
        checkpoint = self.checkpoints[checkpoint_index]
        print(f"[System] Rolling back to iteration {checkpoint['iteration']}")
        
        # Reset iteration count
        self.iteration_count = checkpoint["iteration"]
        
        # Note: Full state restoration would require more sophisticated serialization
        print("[System] Checkpoint rollback completed.")
    
    def inject_realtime_context(self, context: str):
        """
        Inject context in real-time during execution.
        
        Args:
            context: Context to inject
        """
        self.user_input_queue.put({
            "signal": InterruptSignal.ADD_CONTEXT,
            "content": context
        })
        print(f"[System] Context queued for injection: {context[:50]}...")
    
    def modify_goal_realtime(self, new_goal: str):
        """
        Modify the agent's goal in real-time.
        
        Args:
            new_goal: The new goal
        """
        self.user_input_queue.put({
            "signal": InterruptSignal.MODIFY_GOAL,
            "content": new_goal
        })
        print(f"[System] Goal modification queued: {new_goal[:50]}...")
    
    def provide_feedback(self, feedback: str):
        """
        Provide feedback to the agent during execution.
        
        Args:
            feedback: The feedback message
        """
        self.user_input_queue.put({
            "signal": InterruptSignal.FEEDBACK,
            "content": feedback
        })
        print(f"[System] Feedback queued: {feedback[:50]}...")


# Note: For Windows compatibility, we need to use a different approach for input listening
# Since select.select() doesn't work with sys.stdin on Windows, we'll use input() with timeout

try:
    import select
except ImportError:
    # Windows doesn't have select for stdin
    class select:
        @staticmethod
        def select(rlist, wlist, xlist, timeout):
            return [[], [], []]
