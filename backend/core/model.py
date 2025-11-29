from sqlalchemy.orm import relationship
from sqlalchemy import (
   Boolean,
   Integer,
   Column,
   String,
   Text,
   Numeric,
   ForeignKey,
   ARRAY,
   DateTime   
)
from sqlalchemy.dialects.postgresql import UUID
from core.session import Base
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
   __tablename__="users"   
   
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   username=Column(String, unique=True)
   email=Column(String,unique=True)
   password=Column(String)
   role=Column(String, default="user")
   is_active = Column(Boolean, default=False)
   avatar = Column(String)

class Event(Base):
   __tablename__ = "events"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   ticketmaster_id = Column(String, unique=True,nullable=True)
   name = Column(String)
   url = Column(String)
   images = Column(ARRAY(String))
   start_date_sales = Column(DateTime)
   end_date_sales = Column(DateTime)
   start_date_event = Column(DateTime)
   info = Column(Text)
   please_note = Column(Text)
   venue_name = Column(String)
   venue_city = Column(String)
   venue_state = Column(String)
   venue_state_code = Column(String)
   venue_country = Column(String)
   venue_address = Column(String)
   venue_postal_code = Column(String)
   
   ordered_events = relationship("OrderedEvent", back_populates="event")
   
class OrderedEvent(Base):
   __tablename__ = "ordered_events"

   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)   
   event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)   

   event = relationship("Event", back_populates="ordered_events")