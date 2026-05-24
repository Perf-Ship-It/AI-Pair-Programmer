# AI Pair Engineer - Deployment Guide

## 📦 Deployment Options

This guide covers multiple deployment scenarios for AI Pair Engineer.

---

## Option 1: Local Development Deployment

### Purpose
Run AI Pair Engineer on a developer's local machine for daily use.

### Requirements
- Python 3.9+
- 16GB+ RAM
- Optional: NVIDIA GPU with 8GB+ VRAM
- 20GB+ storage for models

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Pair_Engineer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download a local LLM**
   - Visit [Hugging Face](https://huggingface.co/mistralai/Mistral-7B-v0.3)
   - Download the model to `models/` directory
   - Or use `huggingface-cli download`

5. **Configure settings** (optional)
   ```bash
   # Create config/user_config.json
   echo '{"model_name": "mistralai/Mistral-7B-v0.3", "device": "auto"}' > config/user_config.json
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the web interface**
   - Open browser to `http://localhost:8501`

---

## Option 2: Docker Deployment

### Purpose
Containerized deployment for consistent environments across teams.

### Prerequisites
- Docker installed
- Docker Compose (optional)

### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application
   COPY . .

   # Download model (or mount as volume)
   RUN huggingface-cli download mistralai/Mistral-7B-v0.3 --local-dir /app/models

   # Expose port
   EXPOSE 8501

   # Run application
   CMD ["streamlit", "run", "app.py"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     ai-pair-engineer:
       build: .
       ports:
         - "8501:8501"
       volumes:
         - ./models:/app/models
         - ./config:/app/config
       environment:
         - MODEL_NAME=mistralai/Mistral-7B-v0.3
         - DEVICE=auto
         - QUANTIZATION=4bit
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: 1
                 capabilities: [gpu]
   ```

3. **Build and run**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Open browser to `http://localhost:8501`

---

## Option 3: Team Server Deployment

### Purpose
Deploy on a team server for shared access.

### Requirements
- Linux server with 32GB+ RAM
- NVIDIA GPU (optional but recommended)
- 50GB+ storage
- Python 3.10+

### Steps

1. **Install Python and dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip -y
   pip install -r requirements.txt
   ```

2. **Download models**
   ```bash
   huggingface-cli download mistralai/Mistral-7B-v0.3 --local-dir models
   ```

3. **Set up systemd service**
   ```ini
   # /etc/systemd/system/ai-pair-engineer.service
   [Unit]
   Description=AI Pair Engineer
   After=network.target

   [Service]
   User=your-user
   Group=your-group
   WorkingDirectory=/opt/ai-pair-engineer
   ExecStart=/opt/ai-pair-engineer/venv/bin/streamlit run app.py
   Restart=always
   Environment=MODEL_NAME=mistralai/Mistral-7B-v0.3
   Environment=DEVICE=auto
   Environment=QUANTIZATION=4bit

   [Install]
   WantedBy=multi-user.target
   ```

4. **Enable and start service**
   ```bash
   sudo systemctl enable ai-pair-engineer
   sudo systemctl start ai-pair-engineer
   ```

5. **Configure firewall**
   ```bash
   sudo ufw allow 8501/tcp
   ```

6. **Access the application**
   - Open browser to `http://your-server-ip:8501`

---

## Option 4: Cloud Deployment (AWS/GCP/Azure)

### Purpose
Deploy on cloud infrastructure for scalability.

### AWS Example

1. **EC2 Instance**
   ```bash
   # Launch EC2 instance with Ubuntu
   # Install Python and dependencies
   # Download models
   # Run application
   ```

2. **ECS/Fargate**
   ```yaml
   # Use ECS with Fargate for containerized deployment
   # Configure task definition with GPU support
   ```

3. **SageMaker**
   ```python
   # Deploy as custom endpoint
   # Configure inference configuration
   ```

### GCP Example

1. **Compute Engine**
   ```bash
   # Launch VM with GPU
   # Install dependencies
   # Deploy application
   ```

2. **Cloud Run**
   ```bash
   # Containerize application
   # Deploy to Cloud Run
   # Configure GPU resources
   ```

### Azure Example

1. **Azure VM**
   ```bash
   # Launch VM with GPU
   # Deploy application
   ```

2. **Azure Container Instances**
   ```bash
   # Containerize and deploy
   # Configure GPU resources
   ```

---

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| MODEL_NAME | LLM model name | mistralai/Mistral-7B-v0.3 |
| DEVICE | Device (cuda/cpu/auto) | auto |
| QUANTIZATION | Quantization level | 4bit |
| MAX_CONTEXT_LENGTH | Context window size | 8000 |
| MAX_NEW_TOKENS | Max tokens per response | 512 |
| TEMPERATURE | Generation temperature | 0.7 |
| LOG_LEVEL | Logging level | INFO |

### Configuration File

Create `config/user_config.json`:

```json
{
  "model_name": "mistralai/Mistral-7B-v0.3",
  "device": "auto",
  "quantization": "4bit",
  "max_tokens": 512,
  "temperature": 0.7,
  "features_enabled": {
    "code_completion": true,
    "refactoring": true,
    "bug_detection": true
  }
}
```

---

## Security Considerations

### Best Practices

1. **Use HTTPS**
   - Configure SSL/TLS for production deployments
   - Use reverse proxy (nginx, Apache)

2. **Limit File Access**
   - Restrict file system access to necessary directories
   - Use chroot or containerization

3. **Secure Model Downloads**
   - Use trusted Hugging Face repositories
   - Verify model checksums

4. **Monitor Resources**
   - Set up monitoring for GPU/CPU usage
   - Configure alerts for resource exhaustion

5. **Regular Updates**
   - Keep dependencies updated
   - Monitor for security vulnerabilities

---

## Performance Optimization

### Tips

1. **Use GPU Acceleration**
   - Enable CUDA for faster inference
   - Use mixed precision (FP16)

2. **Enable Quantization**
   - Use 4-bit quantization for memory efficiency
   - Balance between performance and memory usage

3. **Cache Results**
   - Enable caching for repeated queries
   - Configure cache size appropriately

4. **Batch Processing**
   - Process multiple files in batches
   - Use async operations where possible

5. **Monitor Performance**
   - Track inference time
   - Optimize context window size

---

## Monitoring and Logging

### Setup

1. **Enable Logging**
   ```python
   import logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

2. **Configure Log Rotation**
   ```ini
   # /etc/logrotate.d/ai-pair-engineer
   /var/log/ai-pair-engineer/*.log {
       daily
       rotate 7
       compress
       delaycompress
       missingok
       notifempty
   }
   ```

3. **Monitor GPU Usage**
   ```bash
   # Install nvidia-smi
   nvidia-smi
   ```

4. **Set Up Alerts**
   - Configure email alerts for errors
   - Set up monitoring dashboards

---

## Backup and Recovery

### Backup Strategy

1. **Backup Configuration**
   ```bash
   tar -czf backup-config-$(date +%Y%m%d).tar.gz config/
   ```

2. **Backup Models**
   ```bash
   # Models are large, consider cloud storage
   rsync -av models/ cloud-storage:/models/
   ```

3. **Automated Backups**
   ```bash
   # Add to crontab
   0 2 * * * tar -czf /backup/ai-pair-engineer-$(date +%Y%m%d).tar.gz config/
   ```

### Recovery

1. **Restore Configuration**
   ```bash
   tar -xzf backup-config-YYYYMMDD.tar.gz -C /path/to/restore/
   ```

2. **Redownload Models**
   ```bash
   huggingface-cli download mistralai/Mistral-7B-v0.3 --local-dir models
   ```

---

## Scaling Considerations

### Horizontal Scaling

- Use multiple instances behind load balancer
- Share model weights via shared storage
- Implement request queuing

### Vertical Scaling

- Upgrade GPU/CPU resources
- Increase RAM for larger context windows
- Use faster storage (NVMe SSDs)

---

## Troubleshooting

### Common Issues

1. **Model not found**
   - Ensure model is downloaded to correct path
   - Check model name in configuration

2. **Out of memory**
   - Use CPU device or reduce quantization
   - Close other applications

3. **Slow performance**
   - Enable caching
   - Use smaller model or reduce context window

4. **CUDA errors**
   - Update CUDA drivers
   - Check GPU compatibility

---

## Support

For issues or questions:
- Check the [README](./README.md)
- Review [Architecture Design](./architecture_design.md)
- Contact the development team

---

## License

MIT License
