from fastapi import FastAPI, UploadFile, File, Query
from agents.data_ingestion import upload_image, fetch_sentinel_data#, fetch_landsat_data
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables
load_dotenv()

app = FastAPI()

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return upload_image(file)

@app.get("/sentinel/")
async def get_sentinel_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    resolution: int = Query(10, description="Resolution in meters")
):
    return fetch_sentinel_data(lat, lon, resolution)


# @app.get("/landsat/")
# async def get_landsat_data(
#     lat: float = Query(..., description="Latitude"),
#     lon: float = Query(..., description="Longitude")
# ):
#     return fetch_landsat_data(lat, lon)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
