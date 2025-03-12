import os
import yaml
import shutil
from fastapi import File, UploadFile
from agents.sentinel import fetch_sentinel_image
# from agents.landsat import fetch_landsat_image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration from YAML
CONFIG_PATH = "config/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

UPLOAD_DIR = config["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Read API keys from environment variables
SENTINEL_API_KEY = os.getenv("SENTINEL_API_KEY")
# LANDSAT_API_KEY = os.getenv("LANDSAT_API_KEY")

def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded successfully", "file_path": file_path}

def fetch_sentinel_data(lat: float, lon: float, resolution: int = 10):
    """Fetch Sentinel-2 imagery for a given lat/lon location."""
    return fetch_sentinel_image(lat, lon, resolution)#, SENTINEL_API_KEY, config)

# def fetch_landsat_data(lat: float, lon: float):
#     """Fetch Landsat imagery for a given lat/lon location."""
#     return fetch_landsat_image(lat, lon, LANDSAT_API_KEY, config)