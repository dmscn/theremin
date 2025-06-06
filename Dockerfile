FROM python:3.9-slim

# Instala as dependências do OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Cria e define o diretório de trabalho
WORKDIR /app

# Copia o script
COPY simple_webcam.py .

# Instala o OpenCV
RUN pip install opencv-python-headless

# Comando para executar a aplicação
CMD ["python3", "simple_webcam.py"]
