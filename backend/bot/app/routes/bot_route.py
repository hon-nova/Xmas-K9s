from fastapi import APIRouter, Request
from bot.app.services import build_agent
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from typing_extensions import TypedDict, Dict, List

bot_router = APIRouter(prefix="/api/bot", tags=["bot"])
   
class FrontendInput(TypedDict):
   userMsg: str   
   chat_session_id: str
 
chat_sessions = {}

agent = build_agent() 

def serialize_convo(state):
   convo = []
   for msg in state["messages"]:
      content = msg.content
      # Flatten Gemini responses that are lists of chunks
      if isinstance(content, list):
         text_parts = []
         for c in content:
            if isinstance(c, dict) and "text" in c:
               text_parts.append(c["text"])
            elif hasattr(c, "text"):
               text_parts.append(c.text)
            elif isinstance(c, str):
               text_parts.append(c)
         content = " ".join(text_parts)
      elif isinstance(content, dict):
         content = content.get("text", str(content))

      if isinstance(msg, HumanMessage):
         convo.append({"role": "user", "text": content})
      elif isinstance(msg, AIMessage):
         convo.append({"role": "bot", "text": content})
   return convo

from sqlalchemy.orm import Session
from core.auth import get_current_user
from fastapi import Depends
from core.session import get_db
from core.model import User

@bot_router.post("/")
def bot_endpoint(payload: FrontendInput, current_user: User = Depends(get_current_user)):
   user_input = payload["userMsg"]
   chat_session_id = payload["chat_session_id"]

   if chat_session_id not in chat_sessions:
      chat_sessions[chat_session_id] = {
         "messages": [],
         "ticket_id": None,
         "event": None,        
         "hitl": False,
         "user_id": current_user.id,        
         "user_input":None 
      }

   state = chat_sessions[chat_session_id]

   # make sure model knows user is authenticated
   if not any(isinstance(msg, SystemMessage) for msg in state["messages"]):
      state["messages"].insert(0, SystemMessage(content=f"The current user is logged in with ID {state['user_id']}."))

   # user input
   state["messages"].append(HumanMessage(content=user_input))
 
   result_tools = {
      "messages": state["messages"],
      "user_id": state["user_id"],
      "state": state,
      "user_input": user_input        
   }
   
   if state.get("ticket_id"):
      result_tools["ticket_id"] = state["ticket_id"] 
   
   result = agent.invoke(result_tools)   

   latest_ai_msg = result["messages"][-1].content
   latest_ai_text = ""

   if isinstance(latest_ai_msg, list):
      for chunk in latest_ai_msg:
         if isinstance(chunk, dict) and "text" in chunk:
               latest_ai_text += chunk["text"] + " "
   elif isinstance(latest_ai_msg, str):
      latest_ai_text = latest_ai_msg

   # combine controlled + AI reply
   bot_reply = ""
   if state.get("bot_msg"):
      bot_reply += state["bot_msg"] + " "
   if latest_ai_text:
      bot_reply += latest_ai_text.strip()

   # append AI response back to conversation
   state["messages"].append(AIMessage(content=bot_reply))

   # clear transient control messages
   state["bot_msg"] = ""

   return {
      "chat_session_id": chat_session_id,
      "convo": [{"role": "bot", "text": bot_reply}]
   }   

from core.auth import get_current_user
from core.schema import LoginFilter
from core.model import User

@bot_router.get("/me",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   
   base= LoginFilter.model_validate(user) 
   print(f"@BOT: get_me: {base}")
      
   return base

