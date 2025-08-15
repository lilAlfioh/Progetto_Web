from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, min_length=1)
    name: str = Field(min_length=1)
    email: EmailStr

class UserCreate(SQLModel):
    username: str
    name: str
    email: EmailStr

class UserRead(SQLModel):
    username: str
    name: str
    email: EmailStr