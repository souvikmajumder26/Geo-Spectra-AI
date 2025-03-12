import os
import yaml
import cv2
from dotenv import load_dotenv
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, bbox_to_dimensions, BBox, MimeType

# def load_config():
#     """Load configuration from YAML file."""
#     with open("config/config.yaml", "r") as file:
#         return yaml.safe_load(file)

# Load environment variables
load_dotenv()
SENTINEL_CLIENT_ID = os.getenv("SENTINEL_CLIENT_ID")
SENTINEL_CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET")
SENTINEL_INSTANCE_ID = os.getenv("SENTINEL_INSTANCE_ID")

# Load configuration from YAML
CONFIG_PATH = "config/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

UPLOAD_DIR = config["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)

def fetch_sentinel_image(lat: float, lon: float, resolution: int = 10):
    """Fetch Sentinel-2 imagery for a given lat/lon location."""
    # config_data = load_config()
    
    config = SHConfig()
    config.sh_client_id = SENTINEL_CLIENT_ID
    config.sh_client_secret = SENTINEL_CLIENT_SECRET
    config.instance_id = SENTINEL_INSTANCE_ID
    
    bbox = BBox([lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01], crs="EPSG:4326")      ######### need to change to get all four lat/lon
    size = bbox_to_dimensions(bbox, resolution=resolution)
    
    evalscript = """
        function setup() {
            return {
                input: [{ bands: ["B04", "B03", "B02"] }],
                output: { bands: 3 }
            };
        }
        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """
    
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L1C, time_interval=("2024-01-01", "2024-12-31"))],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config
    )
    
    image = request.get_data()[0]
    print(f"Image type: {image.dtype}")
    print(f"Image shape: {image.shape}")
    image_path = os.path.join(UPLOAD_DIR, "sentinel_image.png")
    cv2.imwrite(image_path, image)
    
    return {"message": "Sentinel image fetched", "file_path": image_path}
