import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Define the router
router = APIRouter()

# Define the relative path to the images folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")

@router.get("/{filename}")
async def serve_image(filename: str):
    # Construct the full path to the file

    # fetch file from S3
    file_path = os.path.join(IMAGES_FOLDER, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file as a response
    return FileResponse(file_path)
