from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
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
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

ngrok_url = None
origins = [
    "http://localhost:8000",
    f"http://{local_ip}:8000",
]

def update_ngrok_url():
    global ngrok_url, origins
    while not ngrok_url:
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            print(f"ngrok URL: {ngrok_url}")
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

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to('cuda')

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        print(f"File content type: {type(file_content)}")
        print(f"File content length: {len(file_content)} bytes")
        
        # Log a portion of the file content for verification
        print(f"File content (first 100 bytes): {file_content[:100]}")

        # Decode the image
        img = cv2.imdecode(np.frombuffer(file_content, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=422, detail="Invalid image data")
        
        # Perform inference
        results = model(img)
        detections = results.pandas().xyxy[0].to_dict(orient="records")
        print(f"Detections: {detections}")
        return JSONResponse(content=detections)
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
