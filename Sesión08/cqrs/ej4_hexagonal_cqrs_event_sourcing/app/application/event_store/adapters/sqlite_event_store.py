import json
from sqlalchemy.orm import Session
from app.application.event_store.ports.event_store_port import EventStorePort
from app.infrastructure.db.event_model import EventModel, BaseEvent
from app.infrastructure.db.models import engine

BaseEvent.metadata.create_all(bind=engine)

class SQLiteEventStore(EventStorePort):
    def __init__(self):
        from app.infrastructure.db.models import SessionLocal
        self.db: Session = SessionLocal()

    def save_event(self, aggregate_id: str, event_type: str, data: dict) -> None:
        event = EventModel(
            aggregate_id=aggregate_id,
            event_type=event_type,
            data=json.dumps(data)
        )
        self.db.add(event)
        self.db.commit()

    def get_events(self, aggregate_id: str) -> list[dict]:
        events = self.db.query(EventModel).filter_by(aggregate_id=aggregate_id).all()
        return [json.loads(event.data) for event in events]
