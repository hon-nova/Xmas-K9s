from fastapi import FastAPI
from auth.app.routers.auth_route import auth_router
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI() 

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
) 

app.include_router(auth_router) 

@app.get("/profileping")
def ping(): 
   return {"profileping": "profile-pong"}

import os   
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 8001))
   import uvicorn
   uvicorn.run("auth.app.main:app", host="0.0.0.0", port=port)


   