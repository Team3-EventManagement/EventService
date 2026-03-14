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

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    title: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class EventResponse(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# --- Local Extracted Token Data ---
class TokenData(BaseModel):
    user_id: int
    username: Optional[str] = None
