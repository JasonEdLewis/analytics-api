from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Header 
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.security import verify_token 
from app.db.session import get_db
from app.models.user import User
from app.models.api_key import APIKey 
from app.models.tenant import Tenant
from sqlalchemy.sql import func

# OAuth2 scheme for JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)) -> User:
  """
  Validate JWT token and return current user. Used with Depends() in protected endpoints. 
  """
  credentials_exception = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
  )
  # Verify and decode token 
  user_id = verify_token(token) 
  if user_id is None:
    raise credentials_exception

   #Get user from database
  result = await db.execute(select(User).where(User.id == int(user_id))) 
  user = result.scalar_one_or_none()
  
  if user is None:
    raise credentials_exception
  if not user.is_active:
    raise HTTPException(status_code=400, detail='User is not active')
  return user

async def get_current_tenant(current_user:User = Depends(get_current_user)) -> Tenant:
  """Get the tenant of the current user."""
  return current_user.tenant

async def verify_api_key(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db)) -> Tenant:
  """
  Verify API key and return associated tenant. Used for server-to-server event ingestion. 
  """
  result = await db.execute(select(APIKey).where(APIKey.key == x_api_key) .where(APIKey.is_active == True))
  api_key = result.scalar_one_or_none()
  if not api_key:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
  # Update last_used_at   
  api_key.last_used_at = func.now() 
  await db.commit()
  
  return  api_key