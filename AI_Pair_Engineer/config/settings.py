"""
Default application settings.
These are loaded from environment variables or use sensible defaults.
"""

import os
from pathlib import Path


class Settings:
    """Application settings with environment variable support."""
    
    # Model settings
    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "mistralai/Mistral-7B-v0.3"
    )
    
    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        None  # Auto-detect from MODEL_NAME
    )
    
    # Device settings
    DEVICE = os.getenv(
        "DEVICE",
        "auto"  # auto, cuda, cpu
    )
    
    # Quantization settings
    QUANTIZATION = os.getenv(
        "QUANTIZATION",
        "4bit"  # 4bit, 8bit, none
    )
    
    # Context settings
    MAX_CONTEXT_LENGTH = int(os.getenv(
        "MAX_CONTEXT_LENGTH",
        "8000"
    ))
    
    MAX_NEW_TOKENS = int(os.getenv(
        "MAX_NEW_TOKENS",
        "512"
    ))
    
    # Generation settings
    TEMPERATURE = float(os.getenv(
        "TEMPERATURE",
        "0.7"
    ))
    
    TOP_P = float(os.getenv(
        "TOP_P",
        "0.9"
    ))
    
    # Performance settings
    MAX_RETRIES = int(os.getenv(
        "MAX_RETRIES",
        "3"
    ))
    
    TIMEOUT = int(os.getenv(
        "TIMEOUT",
        "60"
    ))
    
    # Logging settings
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    )
    
    LOG_FILE = os.getenv(
        "LOG_FILE",
        "logs/app.log"
    )
    
    @classmethod
    def validate(cls) -> list:
        """Validate settings and return list of errors."""
        errors = []
        
        # Validate model name
        if not cls.MODEL_NAME:
            errors.append("Model name is required")
        
        # Validate device
        if cls.DEVICE not in ["auto", "cuda", "cpu"]:
            errors.append(f"Invalid device: {cls.DEVICE}")
        
        # Validate quantization
        if cls.QUANTIZATION not in ["4bit", "8bit", "none"]:
            errors.append(f"Invalid quantization: {cls.QUANTIZATION}")
        
        return errors
    
    @classmethod
    def get_log_path(cls) -> Path:
        """Get log file path."""
        return Path(cls.LOG_FILE)
