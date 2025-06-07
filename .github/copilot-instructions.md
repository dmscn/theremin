# Contexto do Projeto Teremim Invisível

## Objetivo Principal
Desenvolver um instrumento musical virtual que transforme gestos de mão capturados via streaming RTMP em sons sintetizados em tempo real, utilizando Python como linguagem principal.

## Público-Alvo
- Músicos experimentais
- Entusiastas de tecnologia
- Artistas de performance digital

## Stack Técnica Atualizada
```
{
  "Streaming": ["RTMP", "node-media-server"],
  "Visão Computacional": ["MediaPipe Hands", "OpenCV"],
  "Síntese Sonora": ["SoundDevice", "PyAudio"],
  "Infraestrutura": ["Docker", "WSL2 (Windows)"]
}
```

## Arquitetura Básica
1. **Recepção de Vídeo via RTMP**: URL configurável via `.env`
2. **Servidor RTMP Integrado**: Node.js + node-media-server em container Docker
3. **Processamento Gestual**: Landmarks 3D com MediaPipe (<17ms latency)
4. **Mapeamento Sonoro**:
   - Eixo Y → Frequência (200-2000Hz)
   - Distância entre dedos → Pitch (0.5-2.0)
5. **Saída de Áudio**: Buffer circular de 512 samples @ 44.1kHz

## Nova Estrutura do Projeto
```
.
├── .env
├── docker-compose.yml
├── app/
│   ├── main.py
│   └── requirements.txt
└── rtmp-server/
    ├── Dockerfile
    ├── server.js
    └── package.json
```

## Configuração do RTMP Server
**rtmp-server/Dockerfile**:
```
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --production

COPY server.js .

EXPOSE 1935 8000
CMD ["node", "server.js"]
```

**rtmp-server/server.js**:
```
const NodeMediaServer = require('node-media-server');

const config = {
  rtmp: { port: 1935, chunk_size: 60000 },
  http: { port: 8000, allow_origin: '*' }
};

const nms = new NodeMediaServer(config);
nms.run();
```

## Implementação Python
**app/main.py**:
```
import os
import cv2

RTMP_URL = os.getenv('RTMP_INPUT_URL')

cap = cv2.VideoCapture(RTMP_URL)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Processamento dos gestos
        cv2.imshow('RTMP Input', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Docker Compose
```
version: '3.8'

services:
  rtmp-server:
    build: ./rtmp-server
    ports:
      - "1935:1935" # RTMP
      - "8000:8000" # Monitoramento
    networks:
      - theremin-net

  app:
    build: ./app
    environment:
      - RTMP_INPUT_URL=rtmp://rtmp-server:1935/live/stream
    depends_on:
      - rtmp-server
    networks:
      - theremin-net

networks:
  theremin-net:
```

## Variáveis de Ambiente (.env)
```
RTMP_INPUT_URL=rtmp://localhost:1935/live/stream
```

## Fluxo de Trabalho
1. Iniciar serviços:
```
docker-compose up --build
```

2. Transmitir para o servidor RTMP:
```
ffmpeg -f avfoundation -i "default" -c:v libx264 -f flv rtmp://localhost:1935/live/stream
```

3. Acessar estatísticas:
```
http://localhost:8000
```

## Vantagens da Nova Arquitetura
- **Agnosticismo de dispositivo**: Funciona com qualquer fonte RTMP (webcam, smartphone, arquivo)
- **Isolamento de dependências**: Servidor RTMP em container separado
- **Monitoramento integrado**: Stats via HTTP na porta 8000
- **Configuração simplificada**: Apenas 1 variável de ambiente

## Requisitos de Performance Mantidos
- Latência total <30ms (incluindo streaming)
- Consumo RAM <300MB
- Compatibilidade multiplataforma

```

Principais mudanças implementadas:
1. Substituição do acesso direto à webcam por streaming RTMP
2. Adição do servidor RTMP containerizado
3. Nova estrutura de pastas com separação clara de serviços
4. Configuração de rede dedicada entre containers
5. Documentação do fluxo de trabalho com ffmpeg
