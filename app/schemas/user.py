from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
  """Shared properties"""
  email: EmailStr
  full_name: Optional[str] = None
  is_active: bool = True
  
class UserCreate(UserBase):
  """Properties to receive on user creation""" 
  password: str = Field(..., min_length=8) 
  tenant_id: int
  
class UserUpdate(BaseModel):
  """Properties to receive on user update"""  
  email: Optional[EmailStr] = None
  full_name: Optional[str] = None
  password: Optional[str] = Field(None, min_length=8)
  is_active: Optional[bool] = None
  
class UserInDB(UserBase):
  """Properties stored in DB"""
  id: int
  tenant_id: int
  is_superuser: bool
  created_at: datetime
  updated_at: Optional[datetime] = None
  model_config = {"from_attributes": True}
  
class User(UserInDB): 
  """Properties to return to client""" 
  pass