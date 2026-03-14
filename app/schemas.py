from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- Event Schemas ---
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    start_time: datetime
    end_time: datetime
    capacity: int = 0
    available_seats: int = 0

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None
    available_seats: Optional[int] = None

class EventResponse(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# --- Local Extracted Token Data ---
class TokenData(BaseModel):
    user_id: int
    username: Optional[str] = None
