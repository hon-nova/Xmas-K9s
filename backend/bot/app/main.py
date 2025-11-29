from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import settings
from bot.app.routes import bot_router, events_router

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() 

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
) 
    
app.include_router(bot_router) 
app.include_router(events_router)

@app.get("/botping")
def ping():
   return {"botping": "bot-pong"}
   
if __name__ == "__main__":   
   import os
   port = int(os.environ.get("PORT", 2025))
   import uvicorn
   uvicorn.run("bot.app.main:app", host="0.0.0.0", port=port)