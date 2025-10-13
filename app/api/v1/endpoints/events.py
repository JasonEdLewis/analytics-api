from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime
from app.db.session import get_db
from app.models.event import Event as EventModel
from app.models.tenant import Tenant
from app.schemas.event import Event, EventCreate, EventQuery 
from app.api.v1.deps import verify_api_key

router = APIRouter()


@router.post("/", response_model=Event, status_code=201) 
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(get_db), tenant: Tenant = Depends(verify_api_key)):
  """
  Create a new event (requires API key). This is the main ingestion endpoint.
  Example:
  POST /api/v1/events
  Headers: X-API-Key: your-api-key
  Body: {
    "event_name": "page_view", "properties": {
    "page": "/dashboard",
    "user_id": "user_123" }
  }
  """
  event = EventModel(tenant_id=tenant.id,**event_in.model_dump())
  db.add(event)
  await db.commit() 
  await db.refresh(event)
  
  return event

@router.get("/", response_model=List[Event]) 
async def list_events(event_name: str = None, start_date: datetime = None, end_date: datetime = None, limit: int = 100,
offset: int = 0, db: AsyncSession = Depends(get_db), tenant: Tenant = Depends(verify_api_key)):
  """
  Query events with filters.
  Example:
  GET /api/v1/events?event_name=page_view&start_date=2025-01-01T00:00:00Z&limit=50 Headers: X-API-Key: your-api-key
  """
  # Build query with filters
  query = select(EventModel).where(EventModel.tenant_id == tenant.id)
  
  if event_name:
    query = query.where(EventModel.event_name == event_name)
    
  if start_date:
    query = query.where(EventModel.created_at >= start_date)
  
  if end_date:
    query = query.where(EventModel.created_at <= end_date)
    
  # Order by newest first
  query = query.order_by(EventModel.created_at.desc())
  
  # Pagination
  query = query.offset(offset).limit(min(limit,1000))
  
  result = await db.execute(query)
  events = result.scalars().all()
  
  return events


@router.get("/{event_id}", response_model=Event) 
async def get_event(event_id: int, db: AsyncSession = Depends(get_db), tenant: Tenant = Depends(verify_api_key)):
  """
  Get a specific event by ID. 
  """
  result = await db.execute(select(EventModel).where(EventModel.id == event_id) .where(EventModel.tenant_id == tenant.id)
)
  event = result.scalar_one_or_none()
  if not event:
    raise HTTPException(status_code=400, detail='Event not found')
  
  return  event