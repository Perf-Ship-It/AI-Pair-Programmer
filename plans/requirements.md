# AI Pair Engineer - Python Dependencies

## Core Dependencies

```bash
pip install streamlit>=1.28.0
pip install transformers>=4.35.0
pip install torch>=2.0.0
pip install accelerate>=0.24.0
pip install langchain>=0.1.0
pip install langchain-community>=0.0.1
pip install sentencepiece>=0.1.99
pip install tokenizers>=0.15.0
pip install huggingface-hub>=0.19.0
pip install tree-sitter>=0.20.0
pip install tree-sitter-languages>=1.10.0
pip install libcst>=1.1.0
pip install python-dotenv>=1.0.0
pip install pyyaml>=6.0.0
pip install requests>=2.31.0
```

## Optional Dependencies

### Model Quantization
```bash
pip install bitsandbytes>=0.41.0
```

### Code Formatting
```bash
pip install black>=23.0.0
pip install isort>=5.12.0
```

### Testing
```bash
pip install pytest>=7.4.0
pip install pytest-cov>=4.1.0
```

## Installation Instructions

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install core dependencies
pip install -r requirements.txt

# Install optional dependencies (if needed)
pip install bitsandbytes black isort pytest pytest-cov
```

## Model Requirements

For local LLM support, download models from Hugging Face:

```bash
# Llama 3 (8B) - Recommended for most use cases
pip install transformers
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
    model = AutoModelForCausalLM.from_pretrained('meta-llama/Meta-Llama-3-8B', device_map='auto'); \
    tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3-8B')"

# Mistral 7B
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
    model = AutoModelForCausalLM.from_pretrained('mistralai/Mistral-7B-v0.3', device_map='auto'); \
    tokenizer = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-v0.3')"
```

## System Requirements

- **RAM**: Minimum 16GB (32GB recommended for 8B models)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional, CPU-only mode available)
- **Storage**: 20GB+ for models and project files
