# ==========================================
# Dockerfile
# ==========================================

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install package
RUN pip install -e .

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "run.py", "api", "--host", "0.0.0.0", "--port", "8000"]


# ==========================================
# docker-compose.yml
# ==========================================

version: '3.8'

services:
  aeon-api:
    build: .
    container_name: aeon-api
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./aeon:/app/aeon
      - ./data:/app/data
    restart: unless-stopped
    command: python run.py api --host 0.0.0.0 --port 8000

  aeon-streamlit:
    build: .
    container_name: aeon-streamlit
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./app.py:/app/app.py
      - ./aeon:/app/aeon
    restart: unless-stopped
    command: streamlit run app.py --server.port 8501 --server.address 0.0.0.0
    depends_on:
      - aeon-api


# ==========================================
# .dockerignore
# ==========================================

__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
dist/
build/
.git/
.gitignore
.env
*.log
.DS_Store
.vscode/
.idea/
tests/
*.md
!README.md
