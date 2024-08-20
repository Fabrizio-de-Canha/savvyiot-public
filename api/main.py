from fastapi import FastAPI
from fastapi.security import HTTPBasic
from api import api_router
from fastapi.middleware.cors import CORSMiddleware

security = HTTPBasic()

app = FastAPI(
    title="beta", openapi_url="/beta/openapi.json"
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)