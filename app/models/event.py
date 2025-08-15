from datetime import datetime
from sqlmodel import SQLModel, Field

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str

class EventCreate(SQLModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    date: datetime
    location: str = Field(min_length=1)

class EventRead(SQLModel):
    title: str
    description: str
    date: datetime
    location: str
    id: int