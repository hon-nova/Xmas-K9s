from core.session import SessionLocal
from core.model import Event, OrderedEvent

def add_event_to_user(ticket_id:str, user_id:str):
   with SessionLocal() as db:
      try:
         event = db.query(Event).filter(Event.ticketmaster_id == ticket_id).first()
         if not event:
            return "Event not found. Please try again."          
         
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
         # print(db.query(OrderedEvent).filter_by(user_id=user_id).all())

         return "SUCCESS"
      
      except Exception as e:
         db.rollback()           
         print(f"@add_event_to_user Error:", e)
         return None
      
# print(f"TEST add_event_to_user:",)
# return_str = add_event_to_user("1AsZkubGkdxClj6", "ebe72e2c-c22b-49b1-916c-8853461d5a9d")
# print(f"RESULT: {return_str}")