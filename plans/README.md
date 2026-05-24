# AI Pair Engineer - Project Documentation

## Overview

AI Pair Engineer is a Streamlit-based web application that provides AI-assisted development features using local LLMs. It offers code completion, refactoring suggestions, and bug detection capabilities.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download a local LLM (e.g., Mistral-7B)
# Visit https://huggingface.co/mistralai/Mistral-7B-v0.3

# 5. Run the application
streamlit run app.py
```

## Features

- **Code Completion**: Generate intelligent code completions based on context
- **Refactoring Suggestions**: Identify code smells and suggest improvements
- **Bug Detection**: Analyze code for potential bugs and issues
- **Local LLM Support**: Works entirely offline with local models
- **Multi-language Support**: Supports Python, JavaScript, TypeScript, Java, Go, Rust, C, C++

## Architecture

See [`architecture_design.md`](./architecture_design.md) for detailed architecture documentation.

## Configuration

See [`configuration_system.md`](./configuration_system.md) for configuration options.

## Dependencies

See [`requirements.md`](./requirements.md) for Python dependencies.

## Prompt Templates

See [`prompt_templates.md`](./prompt_templates.md) for LLM prompt templates.

## Application Structure

See [`app_structure.md`](./app_structure.md) for application structure details.

## System Requirements

- **RAM**: Minimum 16GB (32GB recommended)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional)
- **Storage**: 20GB+ for models and project files
- **Python**: 3.9+

## Supported Models

- Mistral-7B-v0.3
- Meta-Llama-3-8B
- Microsoft-Phi-3-mini
- Google-Gemma-7b-it

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or pull request.
