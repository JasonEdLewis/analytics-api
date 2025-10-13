from pydantic import BaseModel, Field 
from datetime import datetime
from typing import Optional


class APIKeyBase(BaseModel):
  """Shared properties"""
  name: str = Field(..., min_length=1, max_length=255)
  
class APIKeyCreate(APIKeyBase):
  """Properties to receive on API key creation""" 
  tenant_id: int
  
  
class APIKeyInDB(APIKeyBase): 
  """Properties stored in DB""" 
  
  id: int
  tenant_id: int
  key: str
  is_active: bool
  created_at: datetime
  last_used_at: Optional[datetime] = None
  model_config = {"from_attributes": True}
  
class APIKey(APIKeyInDB): 
  """Properties to return to client""" 
  pass