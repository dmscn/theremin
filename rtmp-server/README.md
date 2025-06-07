# RTMP Local Server (node-media-server)

Este serviço cria um endpoint RTMP local para receber streaming de vídeo (ex: de apps Android, ffmpeg, OBS) e repassar para outros consumidores (ex: Python/OpenCV).

## Como usar

1. Instale as dependências:

```zsh
npm install
```

2. Inicie o servidor RTMP:

```zsh
node server.js
```

3. No app de streaming (Android, ffmpeg, OBS), configure o endpoint para:

```
rtmp://<SEU_IP_LOCAL>:1935/livestream
```

- O servidor escuta na porta padrão RTMP (1935).
- O painel web estará disponível em http://localhost:8000.
- O endpoint de status pode ser consultado em http://localhost:8000/api/streams.

## Exemplo de publicação com ffmpeg

```zsh
ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -f flv rtmp://localhost:1935/livestream
```

## Observações
- O app Python consumidor deve usar o mesmo endpoint RTMP para consumir o vídeo.
- Não é necessário Docker para rodar o servidor.
