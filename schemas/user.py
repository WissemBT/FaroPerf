from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: Optional[str] = "User"


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
