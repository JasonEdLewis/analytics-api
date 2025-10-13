from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text, Row
from datetime import datetime, timedelta, timezone
from app.db.session import get_db
from app.models.event import Event as EventModel
from app.models.tenant import Tenant
from app.api.v1.deps import verify_api_key
from pydantic import BaseModel

router = APIRouter()


class EventCount(BaseModel):
    """Response model for event counts"""
    event_name: str
    count: int


class TimeSeriesPoint(BaseModel):
    """Response model for time series data"""
    date: str
    count: int


class PropertyBreakdown(BaseModel):
    """Response model for property value breakdown"""
    value: str
    count: int


@router.get("/events/count")
async def get_event_count(event_name: str = None, start_date: datetime = None, end_date: datetime = None, db: AsyncSession = Depends(get_db), tenant: Tenant = Depends(verify_api_key)):
    """
    Get total count of events with optional filters.
    Example: How many "purchase" events in the last 30 days?
    GET /api/v1/analytics/events/count?event_name=purchase&start_date=2025-01-01 
    """
    query = select(func.count(EventModel.id)).where(
        EventModel.tenant_id == tenant.id)

    if event_name:
        query = query.where(EventModel.event_name == event_name)

    if start_date:
        query = query.where(EventModel.start_date == start_date)

    if end_date:
        query = query.where(EventModel.end_date == end_date)

    result = await db.execute(query)
    count = result.scalar()

    return {'count': count}


@router.get("/events/breakdown", response_model=List[EventCount])
async def get_event_breakdown(
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
        tenant: Tenant = Depends(verify_api_key)):
    """
    Get breakdown of events by event name. Shows which events are most common.
    Example: What are the top 10 events in the last week? GET /api/v1/analytics/events/breakdown?limit=10 
    """

    query = select(EventModel.event_name, func.count(EventModel.id).label('count')).where(
        EventModel.tenant_id == tenant.id).group_by(EventModel.event_name).order_by(func.count(EventModel.id).desc()) .limit(limit)
    if start_date:
        query = query.where(EventModel.created_at >= start_date)

    if end_date:
        query = query.where(EventModel.end_date <= end_date)

    result = await db.execute(query)

    breakdown = [
        EventCount(event_name=row[0], count=row[1]) for row in result.all()
    ]

    return breakdown


@router.get("/events/timeseries", response_model=List[TimeSeriesPoint])
async def get_event_timeseries(
    event_name: str = None,
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
    interval: str = Query(default="day", regex="^(hour|day|week|month)$"), db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(verify_api_key)
):
    """
    Get time series data for events.
    Shows events over time (hourly, daily, weekly, monthly).
    Example: Daily "page_view" counts for last 30 days
    GET /api/v1/analytics/events/timeseries?event_name=page_view&interval=day 
    """

    if not end_date:
        end_date = datetime.now(timezone.utc())

    if not start_date:
        start_date = end_date - timedelta(days=30)

    # PostgreSQL date truncation based on interval
    trunc_func = {
        "hour": "hour",
        "day": "day",
        "week": "week",
        "month": "month"
    }[interval]

    query = (select(func.date_trunc(trunc_func, EventModel.created_at).label('date'),
                    func.count(EventModel.id).label('count')).where(EventModel.tenant_id == tenant.id).where(EventModel.created_at >= start_date).where(EventModel.created_at <= end_date).group_by(text('date')).order_by(text('date'))
             )
    if event_name:
      query = query.where(EventModel.event_name == event_name)
      
    result = await db.execute(query)
    timeseries =[
      TimeSeriesPoint(date=row[0], count=row[1]) for row in result.all()
    ]
    return timeseries
  
@router.get("/properties/breakdown", response_model=List[PropertyBreakdown])
async def get_property_breakdown(
    event_name: str,
    property_key: str,
    start_date: datetime = None,
    end_date: datetime = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db), tenant: Tenant = Depends(verify_api_key)
  ):
    """
    Get breakdown of property values for a specific event. Uses JSONB querying power!
    Example: What are the top pages viewed?
    GET /api/v1/analytics/properties/breakdown?event_name=page_view&property_key=page
    This queries the JSONB "properties" field!
    """
    query = (select( func.jsonb_extract_path_text(
      EventModel.properties,
      property_key
    ).label('value'), func.count(EventModel.id).label('count')
    ).where(EventModel.tenant_id == tenant.id)
    .where(EventModel.event_name == event_name) .where(EventModel.properties.has_key(property_key)) # Only events with this property .group_by(text('value'))
    .order_by(func.count(EventModel.id).desc())
    .limit(limit)
    )
    
    if start_date:
      query = query.where(EventModel.created_at >= start_date)
      
    if end_date:
      query = query.where(EventModel.created_at <= end_date)
      
    result = await db.execute(query)
    breakdown = [
      PropertyBreakdown(value=row[0],count=row[1]) for row in result.all()
    ]
    
    return breakdown