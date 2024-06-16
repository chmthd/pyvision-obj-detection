from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import cv2
import numpy as np
import uvicorn

app = FastAPI()

# Allow CORS
origins = [
    "http://localhost:8080",  # computer
    "http://<YOUR_COMPUTER_IP>:8080",  # phone
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s').to('cuda')

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)
    detections = results.pandas().xyxy[0].to_json(orient="records")
    return JSONResponse(content=detections)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
