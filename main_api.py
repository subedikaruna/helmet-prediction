import io
import os
import cv2
import tempfile
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

app = FastAPI(title="Helmet Detection API")

# Load YOLO model
MODEL_PATH = "Weights/best (1).pt"
model = YOLO(MODEL_PATH)

MEDIA_DIR = "Media"

@app.get("/health")
def health_check():
    return {"status": "online", "model": MODEL_PATH}

# Helper generator to process video frame by frame
def stream_video_frames(video_source):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Could not open video file.")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Run YOLO detection on the frame
            results = model(frame)
            annotated_frame = results[0].plot()

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            # Yield frame in Multipart JPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        cap.release()

# --- IMAGE DETECTION ENDPOINT ---
@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Run YOLO detection
    results = model(image)
    annotated_frame = results[0].plot()
    
    # Convert BGR to RGB
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    res_pil = Image.fromarray(annotated_frame)
    
    buf = io.BytesIO()
    res_pil.save(buf, format="JPEG")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpeg")

# --- VIDEO UPLOAD STREAMING ENDPOINT ---
@app.post("/detect/video/upload")
async def detect_uploaded_video(file: UploadFile = File(...)):
    # Save uploaded video bytes temporarily to disk for OpenCV processing
    suffix = os.path.splitext(file.filename)[1] or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    def generate_and_clean():
        try:
            yield from stream_video_frames(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    return StreamingResponse(
        generate_and_clean(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# --- LOCAL MEDIA VIDEO STREAMING ENDPOINT ---
@app.get("/detect/video/local/{video_name}")
def detect_local_video(video_name: str):
    video_path = os.path.join(MEDIA_DIR, video_name)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found in Media folder.")
    
    return StreamingResponse(
        stream_video_frames(video_path),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )