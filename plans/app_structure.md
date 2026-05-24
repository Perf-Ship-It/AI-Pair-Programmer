# AI Pair Engineer - Application Structure

## Overview

This document describes the Streamlit application structure for the AI Pair Engineer prototype.

## Project Structure

```
AI_Pair_Engineer/
├── app.py                    # Main Streamlit application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py           # Default application settings
│   └── user_config.json      # User-specific configuration
├── engines/
│   ├── __init__.py
│   ├── completion.py         # Code completion engine
│   ├── refactoring.py        # Refactoring suggestions engine
│   └── bug_detection.py      # Bug detection engine
├── context/
│   ├── __init__.py
│   ├── analyzer.py           # File context analyzer
│   └── parser.py             # Project structure parser
├── models/
│   ├── __init__.py
│   └── llm_manager.py        # Local LLM manager
├── utils/
│   ├── __init__.py
│   ├── code_formatter.py     # Code formatting utilities
│   └── prompt_templates.py   # LLM prompt templates
├── static/
│   └── styles.css            # Custom CSS styles
├── logs/                     # Application logs directory
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Main Application File (app.py)

```python
"""
AI Pair Engineer - Main Streamlit Application
"""

import streamlit as st
from config.settings import Settings
from config.user_config import UserConfig
from engines.completion import CompletionEngine
from engines.refactoring import RefactoringEngine
from engines.bug_detection import BugDetectionEngine
from context.analyzer import ContextAnalyzer
from models.llm_manager import LLMManager
from utils.code_formatter import CodeFormatter

def main():
    # Initialize configuration
    settings = Settings()
    user_config = UserConfig()
    
    # Initialize LLM manager
    llm_manager = LLMManager(
        model_name=user_config.model_name,
        device=user_config.device,
        quantization=user_config.quantization
    )
    
    # Initialize engines
    context_analyzer = ContextAnalyzer()
    completion_engine = CompletionEngine(llm_manager, context_analyzer)
    refactoring_engine = RefactoringEngine(llm_manager, context_analyzer)
    bug_detection_engine = BugDetectionEngine(llm_manager, context_analyzer)
    
    # Initialize Streamlit page
    st.set_page_config(
        page_title="AI Pair Engineer",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem 0;
    }
    .feature-section {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🤖 AI Pair Engineer</div>', unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        model_options = user_config.get_available_models()
        selected_model = st.selectbox(
            "Select Model",
            options=model_options,
            index=model_options.index(user_config.model_name)
        )
        
        # Device selection
        device = st.selectbox(
            "Device",
            options=["cuda", "cpu", "auto"],
            index=0 if user_config.device == "auto" else ["cuda", "cpu", "auto"].index(user_config.device)
        )
        
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7
        )
        
        # Max tokens
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4096,
            value=512
        )
        
        # Apply settings
        user_config.model_name = selected_model
        user_config.device = device
        user_config.temperature = temperature
        user_config.max_tokens = max_tokens
    
    # Main content area
    st.header("📝 AI Pair Programming Features")
    
    # File browser
    st.subheader("📂 Open a File")
    uploaded_file = st.file_uploader(
        "Upload a file to analyze",
        type=['py', 'js', 'java', 'ts', 'go', 'rs', 'c', 'cpp', 'h', 'hpp']
    )
    
    # Code editor
    if uploaded_file:
        code = uploaded_file.read().decode('utf-8')
        st.code(code, language='python')
        
        # Cursor position
        cursor_line = st.number_input(
            "Cursor Line",
            min_value=1,
            max_value=len(code.split('\n')),
            value=1
        )
        
        cursor_col = st.number_input(
            "Cursor Column",
            min_value=0,
            max_value=len(code.split('\n')[cursor_line - 1]),
            value=0
        )
        
        # Feature selection
        st.subheader("🎯 Select Feature")
        feature = st.radio(
            "Choose a feature",
            options=["Code Completion", "Refactoring Suggestions", "Bug Detection"]
        )
        
        # Execute selected feature
        if st.button("🚀 Run AI Analysis"):
            with st.spinner("Analyzing code..."):
                if feature == "Code Completion":
                    result = completion_engine.complete(
                        code=code,
                        cursor_line=cursor_line,
                        cursor_col=cursor_col,
                        temperature=user_config.temperature,
                        max_tokens=user_config.max_tokens
                    )
                    st.success("Completion suggestions generated!")
                    st.json(result)
                    
                elif feature == "Refactoring Suggestions":
                    result = refactoring_engine.refactor(
                        code=code,
                        cursor_line=cursor_line,
                        cursor_col=cursor_col,
                        temperature=user_config.temperature,
                        max_tokens=user_config.max_tokens
                    )
                    st.success("Refactoring suggestions generated!")
                    st.json(result)
                    
                elif feature == "Bug Detection":
                    result = bug_detection_engine.detect(
                        code=code,
                        cursor_line=cursor_line,
                        cursor_col=cursor_col,
                        temperature=user_config.temperature,
                        max_tokens=user_config.max_tokens
                    )
                    st.success("Bug detection completed!")
                    st.json(result)
    
    else:
        st.info("Please upload a file to start AI pair programming.")
    
    # Footer
    st.markdown("---")
    st.markdown("🔧 Built with Streamlit | 🤖 Powered by Local LLMs")

if __name__ == "__main__":
    main()
```

## Configuration Files

### config/settings.py

```python
"""
Default application settings.
"""

import os

class Settings:
    """Application settings."""
    
    def __init__(self):
        self.max_context_length = int(os.getenv(
            "MAX_CONTEXT_LENGTH", 
            "8000"
        ))
        
        self.max_new_tokens = int(os.getenv(
            "MAX_NEW_TOKENS",
            "512"
        ))
        
        self.temperature = float(os.getenv(
            "TEMPERATURE",
            "0.7"
        ))
        
        self.max_retries = int(os.getenv(
            "MAX_RETRIES",
            "3"
        ))
        
        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO"
        )
```

### config/user_config.py

```python
"""
User-specific configuration.
"""

import json
import os
from pathlib import Path

class UserConfig:
    """User configuration manager."""
    
    def __init__(self):
        self.config_path = Path("config/user_config.json")
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.model_name = config.get("model_name", "mistralai/Mistral-7B-v0.3")
                self.device = config.get("device", "auto")
                self.quantization = config.get("quantization", "4bit")
                self.max_tokens = config.get("max_tokens", 512)
                self.temperature = config.get("temperature", 0.7)
    
    def save_config(self):
        """Save configuration to JSON file."""
        config = {
            "model_name": self.model_name,
            "device": self.device,
            "quantization": self.quantization,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
```

## Engine Modules

### engines/completion.py

```python
"""
Code completion engine.
"""

import json
from models.llm_manager import LLMManager
from context.analyzer import ContextAnalyzer
from utils.prompt_templates import COMPLETION_PROMPT

class CompletionEngine:
    """Code completion engine."""
    
    def __init__(self, llm_manager: LLMManager, context_analyzer: ContextAnalyzer):
        self.llm_manager = llm_manager
        self.context_analyzer = context_analyzer
        self.prompt = COMPLETION_PROMPT
    
    def complete(self, code: str, cursor_line: int, cursor_col: int, 
                 temperature: float, max_tokens: int) -> dict:
        """Generate code completion suggestions."""
        
        # Analyze context
        context = self.context_analyzer.analyze(code, cursor_line, cursor_col)
        
        # Build prompt
        prompt = self.prompt.format(
            code_context=context,
            cursor_line=cursor_line,
            cursor_col=cursor_col
        )
        
        # Generate completions
        response = self.llm_manager.generate(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Parse and return results
        return self._parse_completions(response)
    
    def _parse_completions(self, response: str) -> dict:
        """Parse completion response."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response"}
```

### engines/refactoring.py

```python
"""
Refactoring suggestions engine.
"""

import json
from models.llm_manager import LLMManager
from context.analyzer import ContextAnalyzer
from utils.prompt_templates import REFACTORING_PROMPT

class RefactoringEngine:
    """Refactoring suggestions engine."""
    
    def __init__(self, llm_manager: LLMManager, context_analyzer: ContextAnalyzer):
        self.llm_manager = llm_manager
        self.context_analyzer = context_analyzer
        self.prompt = REFACTORING_PROMPT
    
    def refactor(self, code: str, cursor_line: int, cursor_col: int,
                 temperature: float, max_tokens: int) -> dict:
        """Generate refactoring suggestions."""
        
        # Analyze context
        context = self.context_analyzer.analyze(code, cursor_line, cursor_col)
        
        # Build prompt
        prompt = self.prompt.format(
            code_to_analyze=code,
            language="python"
        )
        
        # Generate refactoring suggestions
        response = self.llm_manager.generate(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Parse and return results
        return self._parse_refactoring(response)
    
    def _parse_refactoring(self, response: str) -> dict:
        """Parse refactoring response."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response"}
```

### engines/bug_detection.py

```python
"""
Bug detection engine.
"""

import json
from models.llm_manager import LLMManager
from context.analyzer import ContextAnalyzer
from utils.prompt_templates import BUG_DETECTION_PROMPT

class BugDetectionEngine:
    """Bug detection engine."""
    
    def __init__(self, llm_manager: LLMManager, context_analyzer: ContextAnalyzer):
        self.llm_manager = llm_manager
        self.context_analyzer = context_analyzer
        self.prompt = BUG_DETECTION_PROMPT
    
    def detect(self, code: str, cursor_line: int, cursor_col: int,
               temperature: float, max_tokens: int) -> dict:
        """Detect potential bugs in code."""
        
        # Analyze context
        context = self.context_analyzer.analyze(code, cursor_line, cursor_col)
        
        # Build prompt
        prompt = self.prompt.format(
            code_to_analyze=code,
            language="python"
        )
        
        # Generate bug detection results
        response = self.llm_manager.generate(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Parse and return results
        return self._parse_bugs(response)
    
    def _parse_bugs(self, response: str) -> dict:
        """Parse bug detection response."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response"}
```

## Context Analyzer

### context/analyzer.py

```python
"""
File context analyzer.
"""

import os
from pathlib import Path

class ContextAnalyzer:
    """Analyze file context for AI pair programming."""
    
    def __init__(self, max_context_length: int = 8000):
        self.max_context_length = max_context_length
    
    def analyze(self, code: str, cursor_line: int, cursor_col: int) -> str:
        """Analyze code context around cursor position."""
        
        lines = code.split('\n')
        
        # Get context window
        start_line = max(0, cursor_line - 10)
        end_line = min(len(lines), cursor_line + 10)
        
        # Extract context
        context_lines = lines[start_line:end_line]
        context = '\n'.join(context_lines)
        
        # Add file metadata
        metadata = f"""
File Context:
- Total lines: {len(lines)}
- Cursor position: line {cursor_line}, column {cursor_col}
- Context window: lines {start_line + 1} to {end_line}
"""
        
        return metadata + context
    
    def get_relevant_files(self, project_path: str, target_file: str) -> list:
        """Get relevant files in project context."""
        # Implementation for multi-file context analysis
        pass
```

## Usage Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Download a local LLM (e.g., Mistral-7B)
3. Run the application: `streamlit run app.py`
4. Upload a code file and select a feature
5. Adjust settings in the sidebar
6. Click "Run AI Analysis" to get results
