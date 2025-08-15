from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.data.db import SessionDep
from app.models.user import User, UserCreate, UserRead
from app.models.registration import Registration


router = APIRouter(tags=["users"])

@router.get("/users", response_model=list[UserRead])
def list_users(session: SessionDep):
    return session.exec(select(User)).all()

@router.get("/users/{username}", response_model=UserRead)
def get_user(username: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, session: SessionDep):
    if session.get(User, data.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(**data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/users")
def delete_all_users(session: SessionDep):
    # Elimina tutte le registrazioni legate agli utenti
    registrations = session.exec(select(Registration)).all()
    for r in registrations:
        session.delete(r)

    users = session.exec(select(User)).all()
    for u in users:
        session.delete(u)

    session.commit()

    return {
        "message": f"Deleted {len(users)} users and {len(registrations)} registration(s)"
    }

@router.delete("/users/{username}")
def delete_user(username: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Elimina registrazioni collegate
    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()
    for r in registrations:
        session.delete(r)

    session.delete(user)
    session.commit()

    return {
        "message": f"User {username} and {len(registrations)} registration(s) deleted"
    }