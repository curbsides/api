from fastapi import APIRouter, HTTPException
from geopy.distance import geodesic
import json
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

MODEL_API_URI = os.getenv("MODEL_API_URI")

router = APIRouter()

location_data = {}
with open("sf_images.json", "r") as file:
    location_data = json.load(file)

locations = {k: tuple(v) for k, v in location_data.items()}

@router.get("/")
async def get_nearest_locations(latitude: float, longitude: float):
    try:
        user_location = (latitude, longitude)

        distances = [
            (location_id, geodesic(user_location, loc).miles, loc)
            for location_id, loc in locations.items()
        ]
        sorted_locations = sorted(distances, key=lambda x: x[1])

        nearest_locations = []
        async with httpx.AsyncClient() as client:
            for location in sorted_locations:
                location_id, distance, coords = location
                # Make request to the model API
                response = await client.get(f"{MODEL_API_URI}{location_id}")
                if response.status_code == 200 and response.json().get("result") is True:
                    nearest_locations.append({
                        "id": location_id,
                        "distance": distance,
                        "latitude": coords[0],
                        "longitude": coords[1]
                    })
                
                if len(nearest_locations) == 5:
                    break

        if len(nearest_locations) < 5:
            raise HTTPException(status_code=404, detail="Not enough valid locations found with parking.")

        return {"nearest_locations": nearest_locations}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))