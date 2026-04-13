from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:
    @staticmethod
    def create(db: Session, source: str, payload_str: str, headers_str: str, ip: str) -> Event:
        event = Event(
            source=source,
            payload=payload_str,
            headers=headers_str,
            ip=ip,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_all(db: Session, source: str | None = None, limit: int = 50, offset: int = 0) -> list[Event]:
        query = db.query(Event)
        if source:
            query = query.filter(Event.source == source)
        return query.order_by(Event.received_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Event | None:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def delete(db: Session, event: Event) -> None:
        db.delete(event)
        db.commit()

    @staticmethod
    def get_stats(db: Session) -> list:
        return (
            db.query(Event.source, func.count(Event.id).label("count"))
            .group_by(Event.source)
            .order_by(text("count DESC"))
            .all()
        )
