from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, auth

router = APIRouter()

@router.post("/events/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db), current_user: schemas.TokenData = Depends(auth.get_current_user)):
    # Using model_dump() for pydantic v2
    new_event = models.Event(**event.model_dump(), owner_id=current_user.user_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events/", response_model=List[schemas.EventResponse])
def get_events(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events

@router.get("/events/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event_update: schemas.EventUpdate, db: Session = Depends(database.get_db), current_user: schemas.TokenData = Depends(auth.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    return event

@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(database.get_db), current_user: schemas.TokenData = Depends(auth.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    db.delete(event)
    db.commit()
    return None
