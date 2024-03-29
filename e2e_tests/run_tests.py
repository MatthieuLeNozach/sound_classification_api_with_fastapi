import os
import time
import requests
import logging


API_BASE_URL = "http://api:5555"
AUTH_ENDPOINT = "/auth"
PREDICT_ENDPOINT = "/mlservice/v1/predict"
AUDIO_FOLDER_PATH = "audio"


logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
log_file_path = "/app/logs/test_logs.log" 

def setup_logging():
    """Set up logging configuration."""
    logger = logging.getLogger()  # Get the root logger
    logger.setLevel(logging.INFO)  # Set the logging level to INFO

    # Create a file handler and set its level to INFO
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')     # Create a logging format
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)     # Add the file handler to the logger

setup_logging()


def authenticate():
    """Authenticate and return the access token."""
    data = {
        "grant_type": "",
        "username": "superuser@example.com",
        "password": "8888",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    response = requests.post(f"{API_BASE_URL}/auth/token", data=data)
    response.raise_for_status()  # This will raise an exception for HTTP error responses
    return response.json()["access_token"]


def upload_file(token, file_path):
    """Upload the .wav file using the obtained token."""
    file_name = os.path.basename(file_path)  # Get the name of the file
    file_size = os.path.getsize(file_path)  # Get the size of the file

    with open(file_path, 'rb') as file:
        headers = {"Authorization": f"Bearer {token}"}
        files = {"audio_file": file}
        response = requests.post(f"{API_BASE_URL}{PREDICT_ENDPOINT}", headers=headers, files=files)
        response.raise_for_status()

        # Log upload details
        logging.info(f"Upload successful: File='{file_name}', Size={file_size} bytes, Response='{response.json()}'")


def main():
    token = authenticate()
    audio_files = [f for f in os.listdir(AUDIO_FOLDER_PATH) if f.endswith('.wav')]
    for audio_file in audio_files:
        audio_file_path = os.path.join(AUDIO_FOLDER_PATH, audio_file)
        print(f"Uploading {audio_file}...")
    
        upload_file(token, audio_file_path)
        time.sleep(2)  # Pause for 2 seconds between each request


if __name__ == "__main__":
    main()