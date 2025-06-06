# Aplicação Simples de Visualização de Webcam

Esta é uma aplicação Python simples que exibe o vídeo da webcam em uma janela, rodando dentro de um container Docker.

## Requisitos

- Docker instalado
- Acesso à webcam do dispositivo

## Como executar

1. Construa a imagem do Docker:
   ```bash
   docker build -t webcam-viewer .
   ```

2. Execute o container com acesso à webcam:
   ```bash
   docker run --device=/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --network=host webcam-viewer
   ```

## Como usar

- A janela da webcam será aberta automaticamente
- Pressione 'q' para sair da aplicação

## Notas

- Certifique-se de que a webcam não está sendo usada por outro aplicativo
- Em alguns sistemas, pode ser necessário instalar o X11 server (XQuartz no macOS)
