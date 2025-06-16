from abc import ABC, abstractmethod
from typing import Any

class EventStorePort(ABC):
    @abstractmethod
    def save_event(self, aggregate_id: str, event_type: str, data: dict) -> None:
        pass

    @abstractmethod
    def get_events(self, aggregate_id: str) -> list[dict]:
        pass
