"""
MIKE AI - Advanced Multi-Model LLM Engine
Supports routing tasks to specialized models based on task type
"""
import json
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path

from config.settings import LLM_CONFIG, MODEL_ROUTING


class MultiModelEngine:
    """
    Advanced LLM engine that routes tasks to specialized models.
    Supports code, creative, reasoning, vision, and math tasks.
    """
    
    def __init__(self):
        self.mock_mode = LLM_CONFIG["mock_mode"]
        self.ollama_host = LLM_CONFIG["ollama_host"]
        self.api_timeout = LLM_CONFIG["api_timeout"]
        self.model_routing = MODEL_ROUTING
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 50
        
    def classify_task(self, user_input: str) -> str:
        """Classify the task type to route to appropriate model."""
        user_input_lower = user_input.lower()
        
        # Code-related tasks
        code_keywords = ["code", "program", "script", "function", "debug", 
                        "python", "javascript", "java", "c++", "write code",
                        "implement", "algorithm", "api", "library", "module"]
        if any(kw in user_input_lower for kw in code_keywords):
            return "code_tasks"
        
        # Math-related tasks
        math_keywords = ["calculate", "math", "equation", "solve", "derivative",
                        "integral", "algebra", "geometry", "statistics", "probability"]
        if any(kw in user_input_lower for kw in math_keywords):
            return "math_tasks"
        
        # Vision-related tasks (image analysis)
        vision_keywords = ["image", "picture", "photo", "visual", "diagram",
                          "chart", "graph", "screenshot", "analyze image"]
        if any(kw in user_input_lower for kw in vision_keywords):
            return "vision_tasks"
        
        # Creative tasks
        creative_keywords = ["write story", "poem", "creative", "imagine",
                           "compose", "design", "artistic", "fiction"]
        if any(kw in user_input_lower for kw in creative_keywords):
            return "creative_tasks"
        
        # Reasoning tasks
        reasoning_keywords = ["analyze", "reason", "think", "explain why",
                            "compare", "evaluate", "assess", "conclusion"]
        if any(kw in user_input_lower for kw in reasoning_keywords):
            return "reasoning_tasks"
        
        return "default"
    
    def get_model_for_task(self, task_type: str) -> str:
        """Get the appropriate model for the task type."""
        return self.model_routing.get(task_type, self.model_routing["default"])
    
    def _mock_response(self, user_input: str, task_type: str) -> Dict[str, Any]:
        """Generate intelligent mock responses for testing."""
        task_type_map = {
            "code_tasks": "I'll help you with that coding task. In full mode, I would use the Qwen-Coder model to generate optimized, well-documented code.",
            "math_tasks": "I can solve this mathematical problem. With the math model enabled, I'd provide step-by-step solutions with explanations.",
            "vision_tasks": "For image analysis, I would use the LLaVA model to interpret visual content and provide detailed descriptions.",
            "creative_tasks": "Let me craft a creative response. The creative model would help generate engaging, imaginative content.",
            "reasoning_tasks": "I'll analyze this systematically. The reasoning model excels at logical deduction and complex problem-solving.",
            "default": "I understand your request. I'm ready to assist with comprehensive capabilities across multiple domains."
        }
        
        base_response = task_type_map.get(task_type, task_type_map["default"])
        
        # Add context-aware suggestions
        suggestions = []
        if "file" in user_input.lower():
            suggestions.append("Try: 'Create a Python script that reads CSV files'")
        if "search" in user_input.lower() or "find" in user_input.lower():
            suggestions.append("Try: 'Search for latest Python best practices'")
        if "system" in user_input.lower():
            suggestions.append("Try: 'Monitor my CPU usage and alert if high'")
        
        return {
            "success": True,
            "response": f"{base_response}\n\n(Mock Mode Active - Enable real models in config/settings.py)",
            "task_type": task_type,
            "model_used": "mock_engine",
            "confidence": 0.95,
            "suggestions": suggestions,
            "metadata": {
                "input_length": len(user_input),
                "processing_time_ms": 50,
            }
        }
    
    def _call_ollama(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call Ollama API for real model inference."""
        try:
            url = f"{self.ollama_host}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": LLM_CONFIG["temperature"],
                    "num_predict": LLM_CONFIG["max_tokens"],
                }
            }
            
            response = requests.post(url, json=payload, timeout=self.api_timeout)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "response": result.get("response", ""),
                "task_type": self.classify_task(prompt),
                "model_used": model,
                "confidence": 0.9,
                "metadata": {
                    "total_duration": result.get("total_duration", 0),
                    "load_duration": result.get("load_duration", 0),
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                }
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API call failed: {str(e)}",
                "fallback_to_mock": True,
            }
    
    def process(self, user_input: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input with automatic model routing.
        
        Args:
            user_input: The user's request
            system_prompt: Optional system instruction
            
        Returns:
            Dictionary with response and metadata
        """
        # Classify task and select model
        task_type = self.classify_task(user_input)
        model = self.get_model_for_task(task_type)
        
        # Build prompt with context
        full_prompt = user_input
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {user_input}"
        
        # Add conversation history for context
        if self.conversation_history:
            history_context = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in self.conversation_history[-10:]
            ])
            full_prompt = f"{history_context}\n\nUser: {full_prompt}"
        
        # Generate response
        if self.mock_mode:
            result = self._mock_response(user_input, task_type)
        else:
            result = self._call_ollama(model, full_prompt)
            if not result.get("success") and result.get("fallback_to_mock"):
                result = self._mock_response(user_input, task_type)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": result.get("response", "")})
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        return result
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Simple chat interface returning just the response text."""
        result = self.process(message, system_prompt)
        return result.get("response", "Error: No response generated")
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return engine capabilities."""
        return {
            "mock_mode": self.mock_mode,
            "available_models": list(self.model_routing.keys()),
            "model_mapping": self.model_routing,
            "ollama_host": self.ollama_host,
            "conversation_length": len(self.conversation_history),
            "supported_task_types": [
                "code_tasks", "math_tasks", "vision_tasks",
                "creative_tasks", "reasoning_tasks", "default"
            ]
        }


# Singleton instance
_llm_engine = None

def get_llm_engine() -> MultiModelEngine:
    """Get or create the LLM engine singleton."""
    global _llm_engine
    if _llm_engine is None:
        _llm_engine = MultiModelEngine()
    return _llm_engine
