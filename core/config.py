import os

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 250
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
VAD_RMS_THRESHOLD = float(os.getenv("VAD_RMS_THRESHOLD", 0.008))
TRANSCRIBE_INTERVAL = float(os.getenv("TRANSCRIBE_INTERVAL", 4.0))
DATABASE_URL = "sqlite:///transcripts.db"

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)

session_id = "live_session"
sessions = {}
