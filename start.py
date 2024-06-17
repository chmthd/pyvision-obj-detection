import subprocess
import time
import requests

def start_ngrok():
    print("Starting ngrok...")
    ngrok = subprocess.Popen(['ngrok', 'http', '8000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    return ngrok

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

def start_fastapi():
    print("Starting FastAPI server...")
    fastapi = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5) 
    return fastapi

def start_frontend():
    print("Starting frontend server...")
    frontend = subprocess.Popen(['python', '-m', 'http.server', '8080'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return frontend

if __name__ == "__main__":
    try:
        ngrok_process = start_ngrok()
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            print(f"Ngrok tunnel URL: {ngrok_url}")
        else:
            print("Failed to get ngrok URL")

        fastapi_process = start_fastapi()
        frontend_process = start_frontend()

        print("All services started successfully.")
        print("Ngrok is tunneling to port 8000.")
        print("FastAPI server is running on port 8000.")
        print("Frontend server is running on port 8080.")

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all services...")
        ngrok_process.terminate()
        fastapi_process.terminate()
        frontend_process.terminate()
        print("All services stopped.")
