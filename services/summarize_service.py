from transformers import pipeline

print("⏳ Loading summarizer...")
try:
    summarizer = pipeline("summarization", model="Falconsai/medical_summarization")
except Exception:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Summarizer ready")

def summarize_conversation(transcript: str) -> str:
    if not transcript.strip():
        return "No conversation recorded."

    summary_text = ""
    try:
        transcript_short = transcript[-3000:]
        summary_output = summarizer(transcript_short, max_length=120, min_length=30, do_sample=False)
        summary_text = summary_output[0]['summary_text']
    except Exception:
        lines = transcript.split("\n")
        summary_text = f"Doctor spoke {len([l for l in lines if 'doctor' in l.lower()])} times, Patient {len([l for l in lines if 'patient' in l.lower()])} times."
    return summary_text
