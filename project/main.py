from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8420",
    "http://localhost:8421",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
