from fastapi.responses import FileResponse
from gtts import gTTS
import tempfile, os

async def text_to_speech(text: str, background_tasks):
    try:
        tts = gTTS(text=text, lang="en")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_path = tmp_file.name
        tmp_file.close()
        tts.save(tmp_path)
        background_tasks.add_task(lambda p: os.remove(p) if os.path.exists(p) else None, tmp_path)
        return FileResponse(tmp_path, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}
