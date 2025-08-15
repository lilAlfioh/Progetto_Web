from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.data.db import SessionDep
from app.models.registration import Registration

router = APIRouter(tags=["registrations"])

@router.get("/registrations", response_model=list[Registration])
def list_registrations(session: SessionDep):
    return session.exec(select(Registration)).all()

@router.delete("/registrations")
def delete_registration(username: str, event_id: int, session: SessionDep):
    registration = session.get(Registration, (username, event_id))
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    session.delete(registration)
    session.commit()
    return {"message": f"Unregistered {username} from event {event_id}"}