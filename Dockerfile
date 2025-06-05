# Dockerfile para Codespaces - Teremim Invisível
FROM python:3.11-slim

# Instala dependências de sistema para Kivy e OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libasound2-dev \
    libmtdev-dev \
    libjpeg-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta para preview (ex: Kivy, Gradio, etc)
EXPOSE 7860

CMD ["bash"]
