from pydantic import BaseModel, Field 
from datetime import datetime, timezone
from typing import Optional

class TenantBase(BaseModel):
  name: str = Field(min_length=1,max_length=255, example="Tenant Name")

class TenantCreate(TenantBase):
  pass

class TenantUpdate(TenantBase):
  """Properties to receive on tenant update"""
  name: Optional[str] = Field(None, min_length=1, max_length=255)
  is_active: Optional[bool] = None
 
class TenantInDB(TenantBase):
  """Properties stored in DB"""
  id: int
  is_active: bool
  created_at: datetime
  updated_at: Optional[datetime] = None
  model_config = {"from_attributes" : True}
  
  
class Tenant(TenantInDB): 
  """Properties to return to client""" 
  pass