"""
Local LLM manager for AI pair programming.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLMManager:
    """Manage local LLM for code generation tasks."""
    
    def __init__(
        self,
        model_name: str = "mistralai/Mistral-7B-v0.3",
        device: str = "auto",
        quantization: str = "4bit",
        max_context_length: int = 8000,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9
    ):
        """Initialize LLM manager.
        
        Args:
            model_name: Name or path of the model to load
            device: Device to use (auto, cuda, cpu)
            quantization: Quantization level (4bit, 8bit, none)
            max_context_length: Maximum context length
            max_new_tokens: Maximum new tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p nucleus sampling parameter
        """
        self.model_name = model_name
        self.device = device
        self.quantization = quantization
        self.max_context_length = max_context_length
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        
        self.model: Optional[Any] = None
        self.tokenizer: Optional[Any] = None
        self._model_loaded = False
    
    def load_model(self) -> None:
        """Load the LLM model."""
        if self._model_loaded:
            return
        
        # Determine device
        if self.device == "auto":
            if torch.cuda.is_available():
                self.device = "cuda"
            else:
                self.device = "cpu"
        
        # Determine model path
        model_path = self.model_name
        
        # Try to load from Hugging Face
        try:
            print(f"Loading model: {self.model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True
            )
            
            # Load model with appropriate quantization
            if self.quantization == "4bit":
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    device_map="auto" if self.device == "cuda" else {"": self.device},
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                )
            elif self.quantization == "8bit":
                from bitsandbytes import Auto8BitQuantized
                self.model = Auto8BitQuantized.from_pretrained(
                    model_path,
                    device_map="auto" if self.device == "cuda" else {"": self.device},
                    load_in_8bit=True
                )
            else:  # no quantization
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path,
                    device_map="auto" if self.device == "cuda" else {"": self.device},
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    trust_remote_code=True
                )
            
            self._model_loaded = True
            print(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None
    ) -> str:
        """Generate text using the LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate (uses default if None)
            temperature: Temperature for sampling (uses default if None)
            top_p: Top-p parameter (uses default if None)
        
        Returns:
            Generated text
        """
        if not self._model_loaded:
            self.load_model()
        
        if max_tokens is None:
            max_tokens = self.max_new_tokens
        
        if temperature is None:
            temperature = self.temperature
        
        if top_p is None:
            top_p = self.top_p
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_context_length
        ).to(self.model.device)
        
        # Generate
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )
        
        # Decode output
        generated = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        
        return generated
    
    def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> list:
        """Generate multiple completion suggestions.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens per suggestion
            temperature: Temperature for sampling
        
        Returns:
            List of completion suggestions
        """
        if not self._model_loaded:
            self.load_model()
        
        if max_tokens is None:
            max_tokens = self.max_new_tokens
        
        if temperature is None:
            temperature = self.temperature
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_context_length
        ).to(self.model.device)
        
        # Generate multiple completions
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=self.top_p,
                do_sample=True
            )
        
        # Decode outputs
        completions = []
        for output in outputs:
            generated = self.tokenizer.decode(
                output,
                skip_special_tokens=True
            )
            # Remove prompt from completion
            if prompt in generated:
                generated = generated[len(prompt):].strip()
            completions.append(generated)
        
        return completions
    
    def chat(
        self,
        messages: list,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Generate response to chat messages.
        
        Args:
            messages: List of chat messages
            max_tokens: Maximum tokens to generate
            temperature: Temperature for sampling
        
        Returns:
            Generated response
        """
        if not self._model_loaded:
            self.load_model()
        
        if max_tokens is None:
            max_tokens = self.max_new_tokens
        
        if temperature is None:
            temperature = self.temperature
        
        # Format messages as prompt
        prompt = self._format_chat_messages(messages)
        
        # Generate response
        response = self.generate(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response
    
    def _format_chat_messages(self, messages: list) -> str:
        """Format chat messages as prompt.
        
        Args:
            messages: List of chat messages
        
        Returns:
            Formatted prompt string
        """
        # Simple chat formatting
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            prompt_parts.append(f"[{role}]: {content}")
        
        return "\n".join(prompt_parts)
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if not self._model_loaded:
            return {
                "model_name": self.model_name,
                "device": self.device,
                "quantization": self.quantization,
                "loaded": False
            }
        
        return {
            "model_name": self.model_name,
            "device": self.device,
            "quantization": self.quantization,
            "loaded": True
        }
    
    def unload_model(self) -> None:
        """Unload the model to free memory."""
        if self.model is not None:
            self.model = None
            self._model_loaded = False
