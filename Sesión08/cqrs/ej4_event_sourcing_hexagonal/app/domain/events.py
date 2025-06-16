from pydantic import BaseModel
from typing import Dict, Any
import datetime

class Event(BaseModel):
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime.datetime = datetime.datetime.utcnow()

class OrderCreated(Event):
    event_type = "OrderCreated"

class OrderShipped(Event):
    event_type = "OrderShipped"

class PaymentReceived(Event):
    event_type = "PaymentReceived"