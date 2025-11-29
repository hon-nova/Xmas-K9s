from encodings.punycode import T
from unittest.mock import Base
from core.model import User
from fastapi import APIRouter, Request
from bot.app.services import build_agent, add_event_to_user
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from typing_extensions import TypedDict
from core.config import settings
from core.utils import read_events_from_db


events_router = APIRouter(prefix="/api/bot", tags=["events"])

@events_router.get("/events")
def get_events():
   events = read_events_from_db()   
   return {"events": events}

from pydantic import BaseModel
# class UserInput(TypedDict):
#    ticketmasterId: str   

class UserInput(BaseModel):
    ticketmasterId: str
   
from fastapi import Depends, Body
from core.auth import get_current_user
   
@events_router.post("/events/add")
def add_event(payload: UserInput, user: User = Depends(get_current_user)):
   
   ticket_id = payload.ticketmasterId
   user_id = user.id   
   result = add_event_to_user(ticket_id, user_id)
 
   if result == "SUCCESS":
      return {"message": "Event successfully added to your account."}
   else:
      return {"message": "nothing"}

