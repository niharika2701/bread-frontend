import pytest
import subprocess
import time
import requests
import os
import sys

SERVER_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///./test_e2e.db"

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    for _ in range(20):
        try:
            requests.get(f"{SERVER_URL}/health", timeout=1)
            break
        except Exception:
            time.sleep(0.5)

    yield

    proc.terminate()
    proc.wait()
    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")
