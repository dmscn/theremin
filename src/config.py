"""
config.py

Carrega variáveis de ambiente do arquivo .env.
"""
from dotenv import load_dotenv
import os

load_dotenv()

RTMP_URL: str = os.getenv("RTMP_URL", "")

if not RTMP_URL:
    raise ValueError("RTMP_URL não definido no .env")
