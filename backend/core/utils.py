from core.events_client import load_events
from core.session import SessionLocal
from core.model import Event, OrderedEvent

def seed_events():
   events = load_events()
   session = SessionLocal()
   for event_data in events:
      event = Event(
         ticketmaster_id=event_data['id'],
         name=event_data['name'],
         url=event_data['url'],
         images=event_data['images'],
         start_date_sales=event_data['start_date_sales'],
         end_date_sales=event_data['end_date_sales'],
         start_date_event=event_data['start_date_event'],
         info=event_data['info'],
         please_note=event_data['please_note'],
         venue_name=event_data['venue']['name'],
         venue_city=event_data['venue']['city'],
         venue_state=event_data['venue']['state'],
         venue_state_code=event_data['venue']['state_code'],
         venue_country=event_data['venue']['country'],
         venue_address=event_data['venue']['address'],
         venue_postal_code=event_data['venue']['postal_code'],
      )
      session.merge(event) 
   session.commit()
   session.close()
   print("Seeding completed. Length of events seeded:", len(events))
   
# seed_events()

def read_events_from_db():
   session = SessionLocal()
   events = session.query(Event).all()
   print(f"SUCCESS Read {len(events)} events from database.")
   session.close()
   return events

# read_events_from_db()
# RUN:  python -m core.utils 
def user_events(user_id):
   session = SessionLocal()
   user_events = session.query(Event).join(OrderedEvent).filter(OrderedEvent.user_id == user_id).all()
   session.close()
   
   print(f"User {user_id} has {len(user_events)} ordered events.")   
   
   return user_events
