import os
from typing import Dict

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 250
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
VAD_RMS_THRESHOLD = 0.008
TRANSCRIBE_INTERVAL = 4.0

session_id = "live_session"
sessions: Dict[str, Dict] = {}

DATABASE_URL = "sqlite:///transcripts.db"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)
