import os
import requests
import yaml
import cv2
from dotenv import load_dotenv

# def load_config():
#     """Load configuration from YAML file."""
#     with open("config/config.yaml", "r") as file:
#         return yaml.safe_load(file)

# Load environment variables
load_dotenv()
LANDSAT_API_KEY = os.getenv("LANDSAT_API_KEY")

# Load configuration from YAML
CONFIG_PATH = "config/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

UPLOAD_DIR = config["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)

def fetch_landsat_image(lat: float, lon: float):
    """Fetch Landsat imagery for a given lat/lon location."""
    # config = load_config()
    
    base_url = "https://api.nasa.gov/planetary/earth/imagery"
    params = {
        "lon": lon,
        "lat": lat,
        "dim": 0.1,  # Approximate width/height of the image in degrees
        "date": "2024-01-01",
        "cloud_score": "True",
        "api_key": LANDSAT_API_KEY
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        image_path = os.path.join(UPLOAD_DIR, "landsat_image.jpg")
        # cv2.imwrite(image_path, image)
        with open(image_path, "wb") as f:
            f.write(response.content)
        return {"message": "Landsat image fetched", "file_path": image_path}
    else:
        return {"error": "Failed to fetch Landsat image", "status_code": response.status_code}
