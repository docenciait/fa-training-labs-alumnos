from typing import Dict, List
from app.domain.ports.event_store import EventStore
from app.domain.events import Event

class InMemoryEventStore(EventStore):
    def __init__(self):
        self.events: Dict[str, List[Event]] = {}

    def append(self, order_id: str, events: List[Event]):
        if order_id not in self.events:
            self.events[order_id] = []
        self.events[order_id].extend(events)

    def get_events(self, order_id: str) -> List[Event]:
        return self.events.get(order_id, [])