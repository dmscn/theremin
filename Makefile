# Makefile para automação do projeto Theremin Invisível

.PHONY: help rtmp-server run clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make rtmp-server   # Inicia o servidor RTMP (Node.js)"
	@echo "  make run           # Executa o consumidor Python do vídeo RTMP"
	@echo "  make clean         # Remove arquivos temporários e ambientes virtuais"

rtmp-server:
	cd rtmp-server && node server.js

run:
	source .venv/bin/activate && python src/main.py

clean:
	rm -rf .venv __pycache__ src/__pycache__ rtmp-server/node_modules
