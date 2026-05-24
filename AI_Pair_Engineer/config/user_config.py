"""
User-specific configuration manager.
"""

import json
import os
from pathlib import Path
from typing import Optional


class UserConfig:
    """Manages user-specific configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. Defaults to config/user_config.json
        """
        self.config_path = config_path or Path("config/user_config.json")
        self._config = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading config: {e}")
                self._config = {}
    
    def save_config(self) -> None:
        """Save configuration to JSON file."""
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    @property
    def model_name(self) -> str:
        """Get model name."""
        return self._config.get("model_name", "mistralai/Mistral-7B-v0.3")
    
    @model_name.setter
    def model_name(self, value: str) -> None:
        """Set model name."""
        self._config["model_name"] = value
    
    @property
    def device(self) -> str:
        """Get device for model loading."""
        return self._config.get("device", "auto")
    
    @device.setter
    def device(self, value: str) -> None:
        """Set device."""
        self._config["device"] = value
    
    @property
    def quantization(self) -> str:
        """Get quantization setting."""
        return self._config.get("quantization", "4bit")
    
    @quantization.setter
    def quantization(self, value: str) -> None:
        """Set quantization."""
        self._config["quantization"] = value
    
    @property
    def max_tokens(self) -> int:
        """Get max tokens for generation."""
        return self._config.get("max_tokens", 512)
    
    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        """Set max tokens."""
        self._config["max_tokens"] = value
    
    @property
    def temperature(self) -> float:
        """Get temperature for generation."""
        return self._config.get("temperature", 0.7)
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        """Set temperature."""
        self._config["temperature"] = value
    
    @property
    def top_p(self) -> float:
        """Get top_p for generation."""
        return self._config.get("top_p", 0.9)
    
    @top_p.setter
    def top_p(self, value: float) -> None:
        """Set top_p."""
        self._config["top_p"] = value
    
    @property
    def features_enabled(self) -> dict:
        """Get enabled features."""
        return self._config.get("features_enabled", {
            "code_completion": True,
            "refactoring": True,
            "bug_detection": True
        })
    
    @features_enabled.setter
    def features_enabled(self, value: dict) -> None:
        """Set enabled features."""
        self._config["features_enabled"] = value
    
    @property
    def supported_languages(self) -> list:
        """Get supported programming languages."""
        return self._config.get("supported_languages", [
            "python", "javascript", "typescript", "java",
            "go", "rust", "c", "cpp"
        ])
    
    @property
    def max_files_in_context(self) -> int:
        """Get max files to include in context."""
        return self._config.get("max_files_in_context", 10)
    
    @property
    def context_window_per_file(self) -> int:
        """Get context window size per file."""
        return self._config.get("context_window_per_file", 50)
    
    @property
    def cache_enabled(self) -> bool:
        """Get cache enabled status."""
        return self._config.get("cache_enabled", True)
    
    @property
    def cache_dir(self) -> str:
        """Get cache directory."""
        return self._config.get("cache_dir", "cache/")
    
    @property
    def ui_settings(self) -> dict:
        """Get UI settings."""
        return self._config.get("ui_settings", {
            "theme": "dark",
            "font_size": "medium",
            "code_highlighting": True
        })
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        return [
            "mistralai/Mistral-7B-v0.3",
            "meta-llama/Meta-Llama-3-8B",
            "microsoft/Phi-3-mini-4k-instruct",
            "google/gemma-7b-it"
        ]
    
    def validate_config(self) -> list:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate model name
        if not self.model_name:
            errors.append("Model name is required")
        
        # Validate device
        if self.device not in ["auto", "cuda", "cpu"]:
            errors.append(f"Invalid device: {self.device}")
        
        # Validate quantization
        if self.quantization not in ["4bit", "8bit", "none"]:
            errors.append(f"Invalid quantization: {self.quantization}")
        
        return errors
