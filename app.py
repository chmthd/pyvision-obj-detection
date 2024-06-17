from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import cv2
import numpy as np
import uvicorn
import socket
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

local_ip = os.getenv("IP_ADDRESS", get_local_ip())

# Allow CORS
origins = [
    "http://localhost:8080", 
    f"http://{local_ip}:8080",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pretrained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to('cuda')

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)
    detections = results.pandas().xyxy[0].to_json(orient="records")
    return JSONResponse(content=detections)

@app.get("/ip")
def get_ip():
    return JSONResponse(content={"ip": local_ip})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
