from fastapi import FastAPI
from .routes.loc_routes import router as loc_router
from .routes.img_routes import router as img_router

app = FastAPI()

app.include_router(loc_router, prefix="/loc")
app.include_router(img_router, prefix="/img")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Healthcheck!"}
