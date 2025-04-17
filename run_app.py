import os
import sys
import subprocess
import threading
import time


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

def run_uvicorn():
    subprocess.run(["python", "-m", "uvicorn", "model_api:app", "--host", "127.0.0.1", "--port", "8000"])

def run_streamlit():
    time.sleep(3)  # Wait for server to start
    subprocess.run(["python", "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    uvicorn_thread = threading.Thread(target=run_uvicorn)
    uvicorn_thread.start()
    run_streamlit()