"""
Configuration settings for the LLM Summarizer application.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)  # Force reload env vars

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# Text Processing Settings
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 200

# Quiz Settings
DEFAULT_NUM_QUESTIONS = 5
MAX_QUESTIONS = 10

# Available Models
AVAILABLE_MODELS = {
    "Gemini 2.5 Pro": {
        "provider": "gemini",
        "model_name": "gemini-2.5-pro",
        "api_key_env": "GEMINI_API_KEY"
    },
    "Gemini 2.5 Flash": {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "api_key_env": "GEMINI_API_KEY"
    },
    "Gemini 1.5 Flash": {
        "provider": "gemini",
        "model_name": "gemini-1.5-flash",
        "api_key_env": "GEMINI_API_KEY"
    },
    "DeepSeek Chat": {
        "provider": "deepseek",
        "model_name": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY"
    },
    "DeepSeek Reasoner": {
        "provider": "deepseek",
        "model_name": "deepseek-reasoner",
        "api_key_env": "DEEPSEEK_API_KEY"
    }
}

# Default model
DEFAULT_MODEL = "Gemini 2.5 Pro"
