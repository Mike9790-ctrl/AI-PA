"""
MIKE AI - Advanced Agent Orchestrator
Coordinates multiple specialized agents with planning, reflection, and self-correction
"""
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from config.settings import AGENT_CONFIG, PLANNING_CONFIG
from core.llm_engine import get_llm_engine

# Import all agents including new ones
from agents.file_agent import FileAgent
from agents.code_agent import CodeAgent
from agents.system_agent import SystemAgent
from agents.web_agent import WebAgent
from agents.communication_agent import CommunicationAgent
from agents.youtube_agent import YouTubeAgent
from agents.business_agent import BusinessAgent
from agents.trading_agent import TradingAgent


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


@dataclass
class Task:
    """Represents a subtask in the execution plan."""
    id: str
    description: str
    agent_type: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    retries: int = 0
    confidence: float = 0.0
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class AgentOrchestrator:
    """
    Advanced orchestrator that coordinates multiple agents.
    Features:
    - Automatic task decomposition
    - Multi-step planning
    - Self-reflection and correction
    - Confidence scoring
    - Parallel execution support
    """
    
    def __init__(self):
        self.llm = get_llm_engine()
        self.max_steps = PLANNING_CONFIG["max_steps"]
        self.enable_reflection = PLANNING_CONFIG["enable_reflection"]
        self.enable_self_correction = PLANNING_CONFIG["enable_self_correction"]
        self.confidence_threshold = PLANNING_CONFIG["confidence_threshold"]
        
        # Available agents
        self.agents = {}
        self._initialize_agents()
        
        # Task tracking
        self.current_plan: List[Task] = []
        self.execution_history: List[Dict[str, Any]] = []
        
    def _initialize_agents(self):
        """Initialize all available agents."""
        if AGENT_CONFIG["enable_file_agent"]:
            from agents.file_agent import FileAgent
            self.agents["file"] = FileAgent()
            
        if AGENT_CONFIG["enable_web_agent"]:
            from agents.web_agent import WebAgent
            self.agents["web"] = WebAgent()
            
        if AGENT_CONFIG["enable_system_agent"]:
            from agents.system_agent import SystemAgent
            self.agents["system"] = SystemAgent()
            
        if AGENT_CONFIG["enable_code_agent"]:
            from agents.code_agent import CodeAgent
            self.agents["code"] = CodeAgent()
        
        # New advanced agents
        if AGENT_CONFIG.get("enable_communication_agent", True):
            self.agents["communication"] = CommunicationAgent()
            
        if AGENT_CONFIG.get("enable_youtube_agent", True):
            self.agents["youtube"] = YouTubeAgent()
            
        if AGENT_CONFIG.get("enable_business_agent", True):
            self.agents["business"] = BusinessAgent()
            
        if AGENT_CONFIG.get("enable_trading_agent", True):
            self.agents["trading"] = TradingAgent()
            
        if AGENT_CONFIG["enable_image_agent"]:
            try:
                from agents.image_agent import ImageAgent
                self.agents["image"] = ImageAgent()
            except ImportError:
                pass
                
        if AGENT_CONFIG["enable_voice_agent"]:
            try:
                from agents.voice_agent import VoiceAgent
                self.agents["voice"] = VoiceAgent()
            except ImportError:
                pass
    
    def decompose_task(self, user_request: str) -> List[Dict[str, Any]]:
        """
        Use LLM to decompose complex tasks into subtasks.
        Returns a list of subtask dictionaries.
        """
        system_prompt = """You are an expert task planner for MIKE AI. Break down the user's request into clear, executable subtasks.

For COMPLEX requests with multiple actions, create separate subtasks for each action.
For SIMPLE requests (greetings, questions, single actions), create just ONE task.

Rules:
1. Create SEPARATE tasks for: creating folders, creating files, writing content, searching web, etc.
2. Specify dependencies correctly (e.g., must create folder before creating file inside it)
3. Choose the right agent: file, web, system, code, image, voice

Return ONLY a valid JSON array. Example for complex task:
[
  {"id": "task_1", "description": "Create directory my_project", "agent_type": "file", "dependencies": []},
  {"id": "task_2", "description": "Create file main.py in my_project with hello world function", "agent_type": "code", "dependencies": ["task_1"]},
  {"id": "task_3", "description": "Create README.md in my_project explaining the project", "agent_type": "file", "dependencies": ["task_1"]}
]

Example for simple greeting:
[{"id": "task_1", "description": "Greet the user and introduce MIKE AI", "agent_type": "system", "dependencies": []}]"""

        response = self.llm.process(user_request, system_prompt)
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response.get("response", ""), re.DOTALL)
        if json_match:
            try:
                subtasks = json.loads(json_match.group())
                if isinstance(subtasks, list) and len(subtasks) > 0:
                    return subtasks
            except json.JSONDecodeError:
                pass
        
        # Fallback: create single task with intelligent agent inference
        agent_type = self._infer_agent_type(user_request)
        return [{
            "id": "task_1",
            "description": user_request,
            "agent_type": agent_type,
            "dependencies": []
        }]
    
    def _infer_agent_type(self, request: str) -> str:
        """Infer the appropriate agent type from the request."""
        request_lower = request.lower()
        
        if any(kw in request_lower for kw in ["file", "folder", "directory", "read", "write", "create", "delete", "copy", "move"]):
            return "file"
        if any(kw in request_lower for kw in ["search", "web", "internet", "url", "website", "http"]):
            return "web"
        if any(kw in request_lower for kw in ["system", "cpu", "memory", "process", "disk", "info"]):
            return "system"
        if any(kw in request_lower for kw in ["code", "program", "script", "function", "debug", "python", "java"]):
            return "code"
        if any(kw in request_lower for kw in ["image", "picture", "photo", "visual"]):
            return "image"
        if any(kw in request_lower for kw in ["speak", "voice", "audio", "say", "tell"]):
            return "voice"
        
        return "file"  # Default
    
    def create_plan(self, user_request: str) -> List[Task]:
        """Create an execution plan from user request."""
        subtasks = self.decompose_task(user_request)
        
        self.current_plan = []
        for subtask in subtasks[:self.max_steps]:
            task = Task(
                id=subtask.get("id", f"task_{len(self.current_plan)+1}"),
                description=subtask.get("description", ""),
                agent_type=subtask.get("agent_type", "file"),
                dependencies=subtask.get("dependencies", [])
            )
            self.current_plan.append(task)
        
        return self.current_plan
    
    def execute_plan(self, user_request: str) -> Dict[str, Any]:
        """Execute the full plan with reflection and self-correction."""
        # Create plan
        plan = self.create_plan(user_request)
        
        results = []
        completed_tasks = set()
        failed_tasks = []
        
        for task in plan:
            # Check dependencies
            deps_met = all(dep in completed_tasks for dep in getattr(task, 'dependencies', []))
            if not deps_met:
                task.status = TaskStatus.FAILED
                task.error = "Dependencies not met"
                failed_tasks.append(task.id)
                continue
            
            # Execute task
            task.status = TaskStatus.IN_PROGRESS
            result = self._execute_task(task, user_request)
            
            if result.get("success"):
                task.status = TaskStatus.COMPLETED
                task.result = result.get("output")
                task.confidence = result.get("confidence", 0.8)
                completed_tasks.add(task.id)
                
                # Reflection step
                if self.enable_reflection and len(plan) > 1:
                    reflection = self._reflect_on_result(task, result)
                    if reflection.get("needs_correction"):
                        task.status = TaskStatus.NEEDS_REVIEW
                        if self.enable_self_correction:
                            corrected_result = self._correct_task(task, user_request)
                            if corrected_result.get("success"):
                                task.status = TaskStatus.COMPLETED
                                task.result = corrected_result.get("output")
            else:
                task.status = TaskStatus.FAILED
                task.error = result.get("error")
                task.retries += 1
                
                # Retry logic
                if task.retries < 3 and self.enable_self_correction:
                    retry_result = self._retry_task(task, user_request)
                    if retry_result.get("success"):
                        task.status = TaskStatus.COMPLETED
                        task.result = retry_result.get("output")
                        completed_tasks.add(task.id)
                    else:
                        failed_tasks.append(task.id)
                else:
                    failed_tasks.append(task.id)
            
            results.append({
                "task_id": task.id,
                "status": task.status.value,
                "result": task.result,
                "error": task.error,
            })
        
        # Generate final summary
        final_response = self._generate_summary(user_request, results, completed_tasks, failed_tasks)
        
        execution_record = {
            "request": user_request,
            "plan": [{"id": t.id, "description": t.description} for t in plan],
            "results": results,
            "completed_count": len(completed_tasks),
            "failed_count": len(failed_tasks),
            "final_response": final_response,
        }
        
        self.execution_history.append(execution_record)
        
        return execution_record
    
    def _execute_task(self, task: Task, context: str) -> Dict[str, Any]:
        """Execute a single task using the appropriate agent."""
        agent_type = task.agent_type
        
        if agent_type not in self.agents:
            return {"success": False, "error": f"Agent type '{agent_type}' not available"}
        
        agent = self.agents[agent_type]
        
        try:
            result = agent.execute(task.description, context=context)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _reflect_on_result(self, task: Task, result: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on task result to check quality."""
        system_prompt = """Review this task result. Is it complete and correct?
Respond with JSON: {"needs_correction": true/false, "reason": "explanation"}"""
        
        prompt = f"Task: {task.description}\nResult: {result.get('output', 'N/A')}"
        response = self.llm.process(prompt, system_prompt)
        
        try:
            json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"needs_correction": False, "reason": ""}
    
    def _correct_task(self, task: Task, context: str) -> Dict[str, Any]:
        """Attempt to correct a failed or low-quality task."""
        # Re-execute with additional context about what went wrong
        enhanced_context = f"{context}\n\nPrevious attempt needs improvement. Focus on accuracy and completeness."
        return self._execute_task(task, enhanced_context)
    
    def _retry_task(self, task: Task, context: str) -> Dict[str, Any]:
        """Retry a failed task."""
        return self._execute_task(task, context)
    
    def _generate_summary(self, request: str, results: List[Dict], 
                         completed: set, failed: set) -> str:
        """Generate a comprehensive summary of the execution."""
        if not failed:
            success_msg = f"✓ Successfully completed all {len(completed)} tasks."
        else:
            success_msg = f"✓ Completed {len(completed)} tasks. ✗ Failed: {len(failed)}"
        
        details = "\n".join([
            f"  • {r['task_id']}: {r['status']}" + 
            (f" - {r['result'][:50]}..." if r['result'] else "") +
            (f" - Error: {r['error']}" if r['error'] else "")
            for r in results
        ])
        
        return f"{success_msg}\n\nExecution Details:\n{details}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "available_agents": list(self.agents.keys()),
            "current_plan_length": len(self.current_plan),
            "execution_history_length": len(self.execution_history),
            "config": {
                "max_steps": self.max_steps,
                "reflection_enabled": self.enable_reflection,
                "self_correction_enabled": self.enable_self_correction,
                "confidence_threshold": self.confidence_threshold,
            }
        }
    
    def reset(self):
        """Reset orchestrator state."""
        self.current_plan = []


# Singleton instance
_orchestrator = None

def get_orchestrator() -> AgentOrchestrator:
    """Get or create the orchestrator singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator
