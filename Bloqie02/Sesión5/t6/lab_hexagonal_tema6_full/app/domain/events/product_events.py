# ProductCreatedEvent code placeholder
# app/domain/events/product_events.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass(frozen=True)
class ProductCreatedEvent:
    product_id: UUID
    name: str
    created_at: datetime = datetime.utcnow()