# PyVision: Real-Time Object Detection

## Overview

PyVision is an application designed to leverage real-time object detection using the YOLOv5 model. 
Built with PyTorch, and FastAPI. Uses CUDA GPU utilization.
Aims to provide an easy-to-use interface for detecting objects using your camera.

## Features

- Real-time object detection using the YOLOv5 model (to be updated).
- Displays a live video feed from your camera upon permission.
- Multi device compatability.
- Automated deployment and dynamic ngrok URL handling
- Remote access

## Prerequisites

1. **[Python 3.12+](https://www.python.org/downloads/)**
2. **[pip](https://pypi.org/project/pip/)**
3. **[CUDA](https://developer.nvidia.com/cuda-downloads)** for GPU utilization.
4. **[OpenCV](https://opencv.org/)** for image processing.
5. **[PyTorch](https://pytorch.org/get-started/locally/)** for running the YOLO model.
6. **[ngrok](https://ngrok.com/download)** for creating secure tunnels to localhost. (Make sure to authenticate your ngrok client using the API key provided)


## Installation

### Clone the repo

```bash
git clone https://github.com/yourusername/pyvision-object-detection.git
cd pyvision-object-detection
```
### Setup up environment variables
Create a .env file in the root directory of the project and add the following line:

```bash
IP_ADDRESS=your_ip_address
```

### Run the application
Run the start.py script to automatically start the ngrok tunnel, FastAPI server, and frontend server.
```bash
python start.py
```

###
Open your browser and navigate to the ngrok URL provided in the terminal. You should see the PyVision web application.

### License
This project is licensed under the MIT License.
