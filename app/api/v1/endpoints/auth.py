from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.security import verify_password, create_access_token 
from app.db.session import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel): 
  access_token: str 
  token_type: str
  
@router.post("/login", response_model=Token) 
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db) ):
  """
  OAuth2 compatible token login. Returns JWT access token.
  """
  
  result = await db.execute(
  select(User).where(User.email == form_data.username) )
  user = result.scalar_one_or_none()
  # Verify user and password
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"},)
  if not user.is_active:
    raise HTTPException(status_code=400, detail="Inactive user")
  
  # Create access token
  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
  access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
  return {
    "access_token": access_token, 
    "token_type": "bearer"
  }