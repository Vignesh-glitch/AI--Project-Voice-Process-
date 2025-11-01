import asyncio
import tempfile, os, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
from sqlmodel import Session
from database.models import Transcript
from database.session import engine
from core.helpers import is_speech, resample_audio_if_needed, trim_silence
from core.config import SAMPLE_RATE, sessions, session_id, WHISPER_MODEL
from core.broadcast import broadcast

model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print(" Whisper model loaded")

async def save_and_transcribe(audio_frames, role, ws):
    print(f" Received {len(audio_frames)} frames from {role}")
    if not audio_frames:
        return

    # Combine audio chunks
    audio_data = b"".join(audio_frames)
    audio_int16 = np.frombuffer(audio_data, dtype=np.int16)
    if audio_int16.size == 0:
        return

    # Normalize and resample if needed
    audio_float = audio_int16.astype(np.float32) / 32768.0

    # 🧩 Safely extract sample rate
    client_meta = sessions.get(session_id, {}).get("clients", {}).get(ws, {})
    client_sr = client_meta.get("sample_rate", None)

    if client_sr is None:
        print("⚠️ Warning: No client sample rate found, using default 16000 Hz.")
        client_sr = 16000  # Default sample rate for Whisper

    if int(client_sr) != SAMPLE_RATE:
        print(f"Resampling audio from {client_sr} Hz → {SAMPLE_RATE} Hz")
        audio_float = resample_audio_if_needed(audio_float, int(client_sr), SAMPLE_RATE)

    # 🔇 Skip silence
    if not is_speech(audio_float):
        print("Skipped silence.")
        return

    audio_float = trim_silence(audio_float)
    if audio_float.size == 0:
        return

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        sf.write(tmp.name, audio_float, SAMPLE_RATE)
        tmp_path = tmp.name

    try:
        # 🧠 Run Whisper in a background thread (non-blocking)
        segments, _ = await asyncio.to_thread(
            model.transcribe,
            tmp_path,
            beam_size=5,
            language="en"
        )

        # Combine transcribed text
        text = " ".join([s.text for s in segments if s.text]).strip()
        print(f"{role}: {text}")

        # 💾 Save transcript in database
        if text:
            with Session(engine) as db:
                db.add(Transcript(role=role, text=text))
                db.commit()

        # 📡 Broadcast to all connected clients
        payload = {"type": "stt", "role": role, "is_final": True, "text": text}
        await broadcast(payload)

        # Store in memory session
        sessions[session_id]["transcript"].append(f"{role}: {text}")

    except Exception as e:
        print("Transcription error:", e)
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

