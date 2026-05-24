# AI Pair Engineer - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites

- Python 3.9+ installed
- 16GB+ RAM available
- Internet connection for initial model download

---

## Step 1: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Download a Local LLM

Visit [Hugging Face](https://huggingface.co/mistralai/Mistral-7B-v0.3) and download the model to your `models/` directory.

---

## Step 4: Configure Settings (Optional)

Create `config/user_config.json`:

```json
{
  "model_name": "mistralai/Mistral-7B-v0.3",
  "device": "auto",
  "quantization": "4bit",
  "max_tokens": 512,
  "temperature": 0.7
}
```

---

## Step 5: Run the Application

```bash
streamlit run app.py
```

---

## Step 6: Use the Application

1. **Upload a file** - Click "Open a File" and upload a code file
2. **Set cursor position** - Enter line and column numbers
3. **Select a feature** - Choose from Code Completion, Refactoring, or Bug Detection
4. **Run analysis** - Click "Run AI Analysis" to get results

---

## 🎯 Quick Tips

- **Start with defaults**: Use default configuration for initial setup
- **Test with small models**: Start with smaller models (7B) before using larger ones
- **Monitor VRAM**: Adjust quantization based on available GPU memory
- **Cache results**: Enable caching for faster repeated queries
- **Backup config**: Regularly backup user_config.json

---

## 🐛 Troubleshooting

### Issue: Model not found
**Solution**: Download the model to the `models/` directory

### Issue: Out of memory
**Solution**: Use CPU device or reduce quantization to 4bit

### Issue: Slow performance
**Solution**: Enable caching and use a smaller model

---

## 📚 Next Steps

- Read the [Company Presentation](./COMPANY_PRESENTATION.md) for details
- Check [Architecture Design](./architecture_design.md) for technical details
- Review [Configuration System](./configuration_system.md) for customization

---

## 🎉 You're Ready!

You now have AI Pair Engineer running locally. Start coding with AI assistance!
