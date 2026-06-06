"""
MIKE AI - Advanced Multimodal Agentic System
Configuration Settings
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# LLM Configuration
LLM_CONFIG = {
    # Set to False to use real local models (requires Ollama or similar)
    "mock_mode": True,
    
    # Model settings for real usage
    "model_name": "qwen-coder:latest",
    "model_path": str(MODELS_DIR),
    "max_tokens": 4096,
    "temperature": 0.7,
    
    # API endpoints
    "ollama_host": "http://localhost:11434",
    "api_timeout": 120,
}

# Agent Configuration
AGENT_CONFIG = {
    "enable_file_agent": True,
    "enable_web_agent": True,
    "enable_system_agent": True,
    "enable_code_agent": True,
    "enable_image_agent": True,
    "enable_voice_agent": True,
    "enable_scheduler_agent": True,
    "enable_database_agent": True,
    
    # New Advanced Agents
    "enable_communication_agent": True,  # Telegram, KakaoTalk, WhatsApp, Email, Discord
    "enable_youtube_agent": True,        # YouTube channel management
    "enable_business_agent": True,       # Side hustles & business planning
    "enable_trading_agent": True,        # Gold, Forex, Crypto trading
    
    # Safety settings
    "safe_mode": True,
    "allowed_directories": [str(Path.home()), str(BASE_DIR)],
    "blocked_commands": ["rm -rf /", "format", "del /s", "shutdown"],
}

# Multi-model routing for different task types
MODEL_ROUTING = {
    "code_tasks": "qwen-coder:latest",
    "creative_tasks": "llama3.2:latest", 
    "reasoning_tasks": "mistral:latest",
    "vision_tasks": "llava:latest",
    "math_tasks": "qwen-math:latest",
    "default": "qwen-coder:latest",
}

# Voice Configuration
VOICE_CONFIG = {
    "enabled": True,
    "speech_recognition_engine": "google",
    "text_to_speech_engine": "pyttsx3",
    "voice_speed": 150,
    "voice_volume": 0.9,
}

# Web Search Configuration
WEB_CONFIG = {
    "search_engine": "duckduckgo",
    "max_results": 10,
    "timeout": 15,
    "user_agent": "Mozilla/5.0 (compatible; MIKE-AI/2.0)",
}

# System Monitoring
SYSTEM_CONFIG = {
    "monitor_interval": 5,
    "alert_thresholds": {
        "cpu_percent": 90,
        "memory_percent": 85,
        "disk_percent": 95,
    }
}

# Task Planning
PLANNING_CONFIG = {
    "max_steps": 20,
    "enable_reflection": True,
    "enable_self_correction": True,
    "confidence_threshold": 0.7,
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(LOGS_DIR / "mike.log"),
    "max_size_mb": 50,
    "backup_count": 5,
}
