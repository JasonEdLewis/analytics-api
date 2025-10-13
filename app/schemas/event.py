from pydantic import BaseModel, Field 
from datetime import datetime
from typing import Dict, Any, Optional


class EventBase(BaseModel):
  """Shared properties"""
  
  event_name: str = Field(..., min_length=1, max_length=255) 
  properties: Dict[str, Any] = Field(default_factory=dict)
  
class EventCreate(EventBase):
  """Properties to receive on event creation"""
  
  pass

class EventInDB(EventBase): 
  """Properties stored in DB""" 
  
  id: int
  tenant_id: int
  created_at: datetime
  model_config = {"from_attributes": True}
  
class Event(EventInDB): 
  """Properties to return to client""" 
  pass

class EventQuery(BaseModel):
  """Query parameters for event filtering""" 
  
  event_name: Optional[str] = None 
  start_date: Optional[datetime] = None 
  end_date: Optional[datetime] = None 
  limit: int = Field(default=100, le=1000) 
  offset: int = Field(default=0, ge=0)