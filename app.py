from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
import cv2
import numpy as np
import socket
from dotenv import load_dotenv
import os
import requests
import time
import threading
import uvicorn

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

def get_ngrok_url():
    try:
        ngrok_api = "http://127.0.0.1:4040/api/tunnels"
        response = requests.get(ngrok_api).json()
        tunnels = response.get("tunnels", [])
        for tunnel in tunnels:
            if tunnel.get("proto") == "https":
                return tunnel.get("public_url")
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
    return None

local_ip = os.getenv("IP_ADDRESS", get_local_ip())

# Initialize ngrok_url to none and origins list
ngrok_url = None
origins = [
    "http://localhost:8080",
    f"http://{local_ip}:8080",
]

# Update ngrok URL and origins dynamically
def update_ngrok_url():
    global ngrok_url, origins
    while not ngrok_url:
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            print(f"ngrok URL: {ngrok_url}")  # Logging
            origins.append(ngrok_url)
            app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            break
        time.sleep(1)

ngrok_thread = threading.Thread(target=update_ngrok_url)
ngrok_thread.start()

# Load the pretrained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to('cuda')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Object Detection API"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    img = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)
    detections = results.pandas().xyxy[0].to_json(orient="records")
    return JSONResponse(content=detections)

@app.get("/ip")
def get_ip():
    print(f"Local IP: {local_ip}")
    return JSONResponse(content={"ip": local_ip})

@app.get("/ngrok-url")
def fetch_ngrok_url():
    global ngrok_url
    if ngrok_url:
        return JSONResponse(content={"url": ngrok_url})
    return JSONResponse(content={"error": "ngrok URL not found"}, status_code=500)

if __name__ == "__main__":
    print("Starting FastAPI server...") 
    uvicorn.run(app, host="0.0.0.0", port=8000)
