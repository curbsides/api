from fastapi import APIRouter, HTTPException
from geopy.distance import geodesic
import json

# Define the router
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
        nearest = sorted(distances, key=lambda x: x[1])[:5]

        # check if location has parking by making query to model API
        # retry until have min number of images

        nearest_locations = [
            {"id": loc[0], "distance": loc[1], "latitude": loc[2][0], "longitude": loc[2][1]}
            for loc in nearest
        ]
        return {"nearest_locations": nearest_locations}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))