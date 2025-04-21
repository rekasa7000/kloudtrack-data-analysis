from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import PROJECT_NAME, API_V1_STR
from app.api.endpoints import forecast, data, internal

app = FastAPI(title=PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast.router, prefix=f"{API_V1_STR}/forecast", tags=["forecast"])
app.include_router(data.router, prefix=f"{API_V1_STR}/data", tags=["data"])
app.include_router(internal.router, prefix=f"{API_V1_STR}/internal", tags=["internal"])