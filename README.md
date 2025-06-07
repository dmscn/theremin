# RTMP Video Consumer

Este projeto consome um stream de vídeo RTMP e exibe em tempo real em uma janela.

## Pré-requisitos
- Python 3.9+
- Node.js 18+
- Um serviço RTMP rodando na rede local (pode ser o `rtmp-server` deste repositório)

## Configuração
1. Copie o arquivo `.env.example` para `.env` e edite a variável `RTMP_URL` com o endpoint do seu stream RTMP.

```zsh
cp .env.example .env
# Edite .env conforme necessário
```

2. Instale as dependências Python:
```zsh
python3 -m venv .venv
pip install -r requirements.txt
```

3. Instale as dependências do servidor RTMP (Node.js):
```zsh
cd rtmp-server
npm install
cd ..
```

## Como executar

### 1. Iniciar o servidor RTMP

Utilize o Makefile:
```zsh
make rtmp-server
```

O servidor estará disponível em `rtmp://<SEU_IP_LOCAL>:1935/livestream` e o painel web em `http://localhost:8000`.

### 2. Enviar vídeo para o servidor RTMP

Exemplo usando ffmpeg (Linux):
```zsh
ffmpeg -f v4l2 -i /dev/video0 -c:v libx264 -f flv rtmp://localhost:1935/livestream
```

Ou utilize um app de streaming no Android apontando para o mesmo endpoint.

### 3. Executar o consumidor Python

```zsh
make run
```

O vídeo será exibido em uma janela. Pressione `q` para fechar.

## Estrutura
- `src/main.py`: Consome e exibe o vídeo RTMP
- `src/config.py`: Carrega variáveis do .env
- `rtmp-server/`: Servidor RTMP local (Node.js)

## Observações
- O serviço RTMP deve estar ativo e acessível na rede local.
- O app é agnóstico à origem do vídeo, apenas consome o endpoint RTMP definido.
- Não é mais necessário Docker para nenhum serviço.
