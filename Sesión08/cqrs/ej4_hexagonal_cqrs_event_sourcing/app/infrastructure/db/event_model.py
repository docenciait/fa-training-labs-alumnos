from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

BaseEvent = declarative_base()

class EventModel(BaseEvent):
    __tablename__ = "event_store"

    id = Column(Integer, primary_key=True, index=True)
    aggregate_id = Column(String, index=True)
    event_type = Column(String)
    data = Column(Text)
