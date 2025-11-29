from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from core.session import get_db
from core.model import Event, User
from core.schema import EventFilter

from langchain.messages import AnyMessage,ToolMessage,SystemMessage
from typing_extensions import TypedDict, Annotated
import operator

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=1,   
    timeout=65,      
)

def get_ticket_by_ticketid_human(ticket_id:str):
   db = next(get_db())
   try:
      event = db.query(Event).filter(Event.ticketmaster_id == ticket_id).first()   
      
      event_dict = EventFilter.model_validate(event)
      # WORKED: print(f"EVENT_DICT: {event_dict}")
      return event_dict
     
   except Exception as e:
      print(f"@get_ticket_by_ticketid Error:", e)
      return None 

# print(f"TEST get_ticket_by_ticketid_human:",)
# new_ticket = get_ticket_by_ticketid_human("177ZvxG6CNemdW1")
# print(f"RESULT: {new_ticket}")
from core.model import OrderedEvent   
from core.session import SessionLocal

def add_event_to_user(ticket_id:str, user_id:str):
   """
   Args:
       ticket_id (str): _description_
       user_id (str): _description_
       db (Session): _description_

   Returns:
       _type_: _description_
   """ 
   with SessionLocal() as db:
      try:
         event = db.query(Event).filter(Event.ticketmaster_id == ticket_id).first()
         if not event:
            return "Event not found. Please try again."
         
         # user = db.query(User).filter(User.id == user_id).first()    
           
         if not user_id:
            return "User not found. Please log in."
         
         # prevent duplicates
         exists = db.query(OrderedEvent).filter_by(user_id=user_id, event_id=event.id).first()
         if exists:
            return "Event already added to your account."

         new_order = OrderedEvent(user_id=user_id, event_id=event.id)
         db.add(new_order)
         db.flush() 
         print(f"New OrderedEvent (pre-commit): {new_order.id}")
         db.commit()
         db.refresh(new_order)
         print("Order persisted:", new_order.id)
         print(f"IMPORTANT Adding event_id={event.id}, user_id={user_id}")
         print(f"CONFIRM ONE MORE TIME: ")
         print(db.query(OrderedEvent).filter_by(user_id=user_id).all())

         return "SUCCESS"
      
      except Exception as e:
         db.rollback()           
         print(f"@add_event_to_user Error:", e)
         return None
      
# print(f"TEST add_event_to_user:",)
# add_event_to_user("1AsZkubGkdxClj6", "ebe72e2c-c22b-49b1-916c-8853461d5a9d")

# Define tools
@tool
def get_weather(location: str) -> str:
    """Get the weather at a location.

    Args:
        location: The location to get the weather for.
    """
    return f"It's sunny in {location}."
 
from typing_extensions import TypedDict, Optional
class AppState(TypedDict):
   user_id: str
   ticket_id: str
   event: Optional[dict]
   bot_msg: Optional[str]
   confirmed: Optional[bool]
   hitl: Optional[bool]
   
@tool
def ask_ticket_id(state: AppState, ticket_id: str):
   """Request a ticket id from the user
   """
   user_id = state["user_id"]
   if not user_id:
      state["bot_msg"] = "You're not authenticated. Please log in to chat with me."
      return state
   
   
   state["ticket_id"] = ticket_id
   event = get_ticket_by_ticketid_human(ticket_id)
   print(f"@tool ask_ticket_id: event SUCCESS: {event}")
   state["event"] = event   
   return state

@tool
def validate_event_existence(state:AppState,ticket_id: Optional[str]=None, user_id: Optional[str] = None, user_input: Optional[str] = None):
   """Validate if an event exists for a given user and ticketmaster ID."""
   if state is None:
      raise ValueError("Missing state")
   
   ticket_id = ticket_id or state.get("ticket_id") 

   if not ticket_id:
      state["bot_msg"] = "⚠️ Missing Ticketmaster ID."
      state["hitl"] = False
      return state

    # Use a new session for this tool  
   with SessionLocal() as db:
      try:
         event = db.query(Event).filter(Event.ticketmaster_id == ticket_id).first()
         if not event:
            state["bot_msg"] = f"⚠️ No event found in the system for Ticketmaster ID: {ticket_id}."
            state["hitl"] = False
            return state

         # Step 1: Ask user to confirm event
         if user_input is None:
            state["bot_msg"] = (
               f"🔎 Found event:\n\n"
               f"🎫 '{event.name}'\n"
               f"📍 {event.venue_name}, {event.venue_city}\n"
               f"📮 Address: {event.venue_address}, {event.venue_postal_code}\n\n"
               f"Is this the correct event? (yes/no)"
            )
            state["ticket_id"] = ticket_id
            state["hitl"] = True
            return state

         # Step 2: Process confirmation response
         answer = user_input.strip().lower()
         if answer in ["yes", "y"]:
            ordered_event = (
               db.query(OrderedEvent)
               .filter_by(user_id=user_id, ticketmaster_id=event.ticketmaster_id) 
               .first()
            )
            if not ordered_event:
               state["bot_msg"] = (
                  f"⚠️ The event '{event.name}' (Ticketmaster ID: {ticket_id}) "
                  f"is not yet in your account."
               )
            else:
               state["bot_msg"] = (
                  f"✅ Yes! The event '{event.name}' "
                  f"(Ticketmaster ID: {ticket_id}) exists in your account."
               )
         else:
            state["bot_msg"] = "❌ Okay, cancelled validation."

         state["hitl"] = False

      except Exception as e:
         print(f"@validate_event_existence Error:", e)
         state["bot_msg"] = "❌ Something went wrong while checking the event."

      return state

# print(f"TEST ORDEREDEVENT QUERY: ")
# db = SessionLocal()
# event = {"ticketmaster_id":"1AsZkubGkdxClj6"}
# order =  (
#                db.query(OrderedEvent)
#                .filter_by(user_id="ebe72e2c-c22b-49b1-916c-8853461d5a9d", event_id="7010abde-096c-45a5-b101-abb0f51a43d1")
#                .first()
#             )
# print(f"ORDER QUERY RESULT: {order}")

# Augment the LLM with tools
tools = [ask_ticket_id,validate_event_existence]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

class MessagesState(TypedDict):
   messages: Annotated[list[AnyMessage], operator.add]
   llm_calls: str   


def llm_call(state: dict):
   """LLM decides whether to call a tool or not""" 

   return {
   "messages": [
      model_with_tools.invoke(
         [
            SystemMessage(
               content=(
                  "You are an event assistant chatbot. "
                  "Always start by greeting the user in a friendly and natural tone. "
                  "Then ask what they would like help with today. "

                  "If the user wants to verify whether an event exists in their account, "
                  "ask them for their Ticketmaster ID. "
                  "Use the `ask_ticket_id` tool to collect and validate the ticket ID format. "

                  "Once you have a valid ticket ID and user ID, use the `validate_event_existence` tool "
                  "to confirm whether that event exists in the system. "

                  "If the tool finds the event, show the event name, venue, and address, "
                  "and ask the user to confirm if it is correct (Yes/no). "
                  "If the user confirms yes, finalize the verification with a clear success message. "
                  "If no, tell them the validation has been cancelled. "

                  "Be concise, polite, and avoid repeating questions unnecessarily."
               )
                )
         ]
         + state["messages"]
      )
   ]
}

def tool_node(state: dict):
   """Performs the tool call"""

   result = []
   for tool_call in state["messages"][-1].tool_calls:
      tool = tools_by_name[tool_call["name"]]
      observation = tool.invoke(tool_call["args"])
      result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
   return {"messages": result}

from typing import Literal
from langgraph.graph import StateGraph, START, END

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
   """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

   messages = state["messages"]
   last_message = messages[-1]

   # If the LLM makes a tool call, then perform an action
   if last_message.tool_calls:
      return "tool_node"

   # Otherwise, we stop (reply to the user)
   return END

# Build workflow
def build_agent():
    
   agent_builder = StateGraph(MessagesState)

   # Add nodes
   agent_builder.add_node("llm_call", llm_call)
   agent_builder.add_node("tool_node", tool_node)

   # Add edges to connect nodes
   agent_builder.add_edge(START, "llm_call")
   agent_builder.add_conditional_edges(
      "llm_call",
      should_continue,
      ["tool_node", END]
   )
   agent_builder.add_edge("tool_node", "llm_call")

   # Compile the agent
   agent = agent_builder.compile()
   return agent
