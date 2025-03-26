import subprocess
import sys
import time
import os

def run_fastapi():
    """Run FastAPI server"""
    print("Starting FastAPI server...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", 
                              "backend_ai.app:app", 
                              "--host", "0.0.0.0", 
                              "--port", "8000", 
                              "--reload"])

def run_streamlit():
    """Run Streamlit app"""
    print("Starting Streamlit app...")
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "backend_ai/ap.py"])

def main():
    # Ensure we're in the project root directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start FastAPI server
    fastapi_process = run_fastapi()
    
    # Give the server a moment to start
    time.sleep(3)

    # Start Streamlit
    streamlit_process = run_streamlit()

    try:
        # Wait for processes to complete
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        fastapi_process.terminate()
        streamlit_process.terminate()

if __name__ == "__main__":
    main()