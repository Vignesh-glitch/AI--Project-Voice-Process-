Doctor–Patient Real-time Transcription App

A real-time speech-to-text and conversation summarization web application built using FastAPI, WebSocket, and Whisper AI.
It enables two-way transcription between a doctor and a patient — converting their speech into live text, storing it in a database, and generating summarized medical notes automatically.
Features

=> Real-time speech recognition using OpenAI Whisper (CPU mode supported)
=>Two-way conversation – doctor and patient transcribed separately
=>Automatic summarization of the full conversation (Hugging Face model)
=>Database integration (SQLModel + SQLite) for transcript storage
=>WebSocket streaming for live updates
=>Frontend UI with role-based controls (Doctor / Patient)
=>Session management for each conversation
=>Extensible microservice architecture – easily add diarization or translation

Layer	Technologies Used
-Backend	FastAPI, WebSocket, SQLModel, asyncio
-Speech-to-Text	Faster-Whisper (medium model)
-Database	SQLite (via SQLModel ORM)
-Frontend	HTML, CSS, JavaScript (WebSocket client)
-Summarization	Hugging Face Transformers (For Future Implementation)
-Audio Handling	soundfile, numpy
-Deployment Ready	uvicorn (with autoreload)
 Installation & Setup
1. Clone the repository
git clone https://github.com/Vignesh-glitch/AI--Project-Voice-Process-.git
cd doctor-patient-transcription

2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate 

3️. Install dependencies
pip install -r requirements.txt

4️. Initialize database
python -m database.session

5️. Run the app
uvicorn main:app --reload


Then visit:
 http://127.0.0.1:8000

How It Works

  Both doctor and patient connect to the same WebSocket session.

  Each user’s microphone audio is streamed live to the backend.

  The whisper_service.py model converts speech → text in real time.

  Transcripts are stored in SQLite (transcripts.db).

  Once the conversation ends, the summarizer generates a medical summary.

Example Output ::
Doctor: How are you feeling today?
Patient: I have been coughing for the past three days.
Doctor: Any fever or throat pain?
Patient: Yes, mild fever and sore throat.

Summary:

Patient presents with cough, mild fever, and sore throat for 3 days. Possible viral infection. Further investigation or medication recommended.


Vignesh V
🎓 B.E. Computer Science Engineer | Aspiring Software Engineer
💼 Experienced in AI, Python, Flask, FastAPI, and Full Stack Development
