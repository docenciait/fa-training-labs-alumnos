from abc import ABC, abstractmethod
from typing import List
from app.domain.events import Event

class EventStore(ABC):
    @abstractmethod
    def append(self, order_id: str, events: List[Event]):
        pass

    @abstractmethod
    def get_events(self, order_id: str) -> List[Event]:
        pass