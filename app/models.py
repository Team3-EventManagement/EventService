from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    available_seats = Column(Integer, nullable=False, default=0)

    # Store the user ID from the external Authentication microservice
    owner_id = Column(Integer, index=True, nullable=False)
