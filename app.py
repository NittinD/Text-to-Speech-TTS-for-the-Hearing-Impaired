from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import os
import uuid

app = FastAPI()

# Serve static files (like index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Homepage route
@app.get("/")
async def get_homepage():
    return FileResponse("static/index.html")

# Convert text to speech using gTTS
@app.post("/convert/")
async def convert_text_to_speech(
    text: str = Form(...),
    rate: int = Form(200),        # Not used by gTTS but kept for compatibility
    volume: float = Form(1.0)     # Not used by gTTS but kept for compatibility
):
    try:
        # Generate unique filename to avoid caching issues
        filename = f"output_{uuid.uuid4().hex}.mp3"

        # Generate speech
        tts = gTTS(text)
        tts.save(filename)

        return {"message": "Audio generated successfully!", "file": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

# Download endpoint
@app.get("/download/{file_name}")
async def download_audio(file_name: str):
    file_path = f"./{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)
    raise HTTPException(status_code=404, detail="File not found")
