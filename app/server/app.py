from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.loc_routes import router as loc_router
from .routes.img_routes import router as img_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loc_router, prefix="/loc")
app.include_router(img_router, prefix="/img")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Healthcheck!"}
