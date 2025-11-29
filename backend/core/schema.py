from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EventFilter(BaseModel):

   ticketmaster_id: str
   name: str  
   images: list[str]
   start_date_event: Optional[datetime]     
   venue_name: Optional[str]
   venue_city: Optional[str]
   venue_state: Optional[str]
   venue_state_code: Optional[str]  
   venue_address: Optional[str]
   venue_postal_code: Optional[str]
   
   model_config = {
      "from_attributes": True
   }

class LoginFilter(BaseModel):
   id: UUID
   username: str
   email: str
   is_active: bool
   role: str
   avatar: Optional[str]
   
   model_config = {
      "from_attributes": True
   }
