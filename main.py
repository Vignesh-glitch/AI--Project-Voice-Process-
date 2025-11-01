from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.responses import Response
import uvicorn
import asyncio
import json
import os

from core.config import session_id, sessions, SAMPLE_RATE, TRANSCRIBE_INTERVAL
from core.broadcast import broadcast
from services.tts_service import text_to_speech
from services.stt_service import save_and_transcribe
from services.summarize_service import summarize_conversation
from database.session import init_db

init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/static/recorder-worklet.js")
def get_worklet():
    return Response(open("static/recorder-worklet.js").read(), media_type="application/javascript")

@app.get("/tts")
async def tts_endpoint(text: str, background_tasks: BackgroundTasks):
    return await text_to_speech(text, background_tasks)

@app.websocket("/ws/whisper")
async def websocket_endpoint(ws: WebSocket, role: str = Query(...)):
    await ws.accept()
    if session_id not in sessions:
        sessions[session_id] = {"clients": {}, "transcript": []}
    sessions[session_id]["clients"][ws] = {"role": role, "sample_rate": None}
    print(f"{role} connected")

    audio_buffer = []

    async def periodic_transcriber():
        nonlocal audio_buffer
        try:
            while True:
                await asyncio.sleep(TRANSCRIBE_INTERVAL)
                if audio_buffer:
                    frames = audio_buffer.copy()
                    audio_buffer = []
                    await save_and_transcribe(frames, role, ws)
        except asyncio.CancelledError:
            return

    transcriber_task = asyncio.create_task(periodic_transcriber())

    try:
        while True:
            message = await ws.receive()
            if message.get("type") == "websocket.receive":
                if message.get("text"):
                    try:
                        js = json.loads(message["text"])
                        if js.get("type") == "meta":
                            sr = int(js.get("sampleRate", SAMPLE_RATE))
                            sessions[session_id]["clients"][ws]["sample_rate"] = sr
                            print(f"Set sample rate for {role} -> {sr}")
                    except Exception:
                        pass
                elif message.get("bytes"):
                    audio_buffer.append(message["bytes"])
    except WebSocketDisconnect:
        print(f"{role} disconnected")
    finally:
        transcriber_task.cancel()
        if audio_buffer:
            await save_and_transcribe(audio_buffer.copy(), role, ws)
        sessions[session_id]["clients"].pop(ws, None)
        if not sessions[session_id]["clients"]:
            transcript_text = "\n".join(sessions[session_id]["transcript"])
            summary = summarize_conversation(transcript_text)
            print("\n🧾 FINAL SUMMARY:\n", summary)
            await broadcast({"type": "summary", "text": summary})
            sessions.pop(session_id, None)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
