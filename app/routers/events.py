from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, File
from sqlmodel import select
from pathlib import Path
import os
import shutil

from app.data.db import SessionDep
from app.models.event import Event, EventCreate, EventRead
from app.models.user import User, UserCreate
from app.models.registration import Registration
from app.config import config

router = APIRouter(tags=["events"])

def to_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

@router.get("/events", response_model=list[EventRead])
def list_events(session: SessionDep):
    return session.exec(select(Event)).all()

@router.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: SessionDep):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/events", response_model=EventRead, status_code=201)
def create_event(data: EventCreate, session: SessionDep):
    if to_utc(data.date) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Date must be in the future")
    event = Event(**data.model_dump())
    session.add(event)
    session.commit()
    session.refresh(event)
    return "Event successfully added" 

@router.put("/events/{event_id}", response_model=EventRead)
def update_event(event_id: int, data: EventCreate, session: SessionDep):
    if to_utc(data.date) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Date must be in the future")
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    for k, v in data.model_dump().items():
        setattr(event, k, v)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@router.delete("/events/{event_id}")
def delete_event(event_id: int, session: SessionDep):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return {"message": f"Event {event_id} deleted"}

@router.delete("/events")
def delete_all_events(session: SessionDep):
    events = session.exec(select(Event)).all()
    for e in events:
        session.delete(e)
    session.commit()
    return {"message": f"Deleted {len(events)} events"}

@router.post("/events/{event_id}/register", status_code=201)
def register_to_event(event_id: int, payload: UserCreate, session: SessionDep):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(User, payload.username)
    if not user:
        user = User(**payload.model_dump())
        session.add(user)
        session.commit()

    if session.get(Registration, (user.username, event_id)):
        raise HTTPException(status_code=409, detail="Already registered")

    session.add(Registration(username=user.username, event_id=event_id))
    session.commit()
    return {"message": f"User {user.username} registered to event {event_id}"}
