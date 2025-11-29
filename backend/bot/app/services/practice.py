import os
from langchain.chat_models import init_chat_model
from core.config import settings
# from langchain_core.messages import HumanMessage


GOOGLE_API_KEY = settings.GOOGLE_API_KEY
# print(f"Google API Key: {GOOGLE_API_KEY}")
model = init_chat_model(
   "google_genai:gemini-2.5-flash",
    # Kwargs passed to the model:
    temperature=0.3,
    timeout=10,
    max_tokens=1500)

# response = model.invoke("Why do parrots have colorful feathers?")
# print(f"output")
# print(response.content)
# print(f"Track: {response.usage_metadata["output_tokens"]}")

"""1. invoke """
# for chunk in model.stream("Hello there"):
#    print(chunk.content, end="", flush=True)
   
"""
2. models - method -  stream
"""
# try:
#    response = model.invoke([HumanMessage(content="Why do parrots have colorful feathers?")])
#    print("output:", response.content)
#    print("tokens used:", response.usage_metadata["output_tokens"])
# except Exception as e:
#    print("Error:", e)


"""
3. models - method -  batch
"""
from core.model import Event
from core.session import get_db
from core.schema import EventFilter
def get_ticket_by_ticketid_human(ticket_id:str):
   db = next(get_db())
   try:
      event = db.query(Event).filter(Event.ticketmaster_id == ticket_id).first()
      
      # ✅ Use Pydantic model for clean conversion
      event_dict = EventFilter.model_validate(event)
      print(f"EVENT_DICT: {event_dict}")
      return event_dict
      # return event if event else " "
   except Exception as e:
      print(f"@get_ticket_by_ticketid Error:", e)
      return None 
print("ATTEMTION: Testing get_ticket_by_ticketid_human function:")   
get_ticket_by_ticketid_human("1778vxG6GS21go2")