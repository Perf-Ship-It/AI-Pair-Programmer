# AI Pair Engineer

AI-powered pair programming assistant with local LLM support.

## Features

- 📝 **Code Completion**: Intelligent code completion suggestions
- 🔧 **Refactoring**: Automated refactoring suggestions
- 🐛 **Bug Detection**: Potential bug identification
- 📖 **Code Explanation**: Understand complex code
- 📝 **Documentation**: Generate docstrings and documentation

## Requirements

- Python 3.9+
- CUDA-enabled GPU (optional, for faster inference)
- 16GB+ RAM (recommended)
- 20GB+ free disk space (for model storage)

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download a model (e.g., Mistral-7B)
# You can download from Hugging Face
# https://huggingface.co/mistralai/Mistral-7B-v0.3
```

## Usage

```bash
# Run the application
streamlit run app.py
```

## Configuration

Edit `config/settings.py` to configure:

- Model name/path
- Device (cuda/cpu)
- Quantization level
- Generation parameters

## Project Structure

```
AI_Pair_Engineer/
├── app.py                    # Main Streamlit application
├── config/                   # Configuration files
│   ├── __init__.py
│   ├── settings.py          # Default settings
│   └── user_config.py       # User-specific settings
├── context/                  # Context analysis
│   ├── __init__.py
│   ├── analyzer.py          # File context analyzer
│   └── parser.py            # Project structure parser
├── models/                   # LLM models
│   ├── __init__.py
│   └── llm_manager.py       # LLM manager
├── engines/                  # Feature engines
│   ├── __init__.py
│   ├── completion_engine.py # Code completion
│   ├── refactoring_engine.py # Refactoring suggestions
│   └── bug_detection_engine.py # Bug detection
├── utils/                    # Utilities
│   ├── __init__.py
│   ├── code_formatter.py    # Code formatting
│   └── prompt_templates.py  # Prompt templates
├── plans/                    # Project plans
│   ├── architecture_design.md
│   ├── requirements.md
│   ├── prompt_templates.md
│   ├── app_structure.md
│   ├── configuration_system.md
│   └── README.md
├── requirements.txt
└── README.md
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
