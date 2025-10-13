from typing import List
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.tenant import Tenant as TenantModel
from app.models.user import User
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate 
from app.api.v1.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=Tenant, status_code=201) 
async def create_tenant(tenant_in: TenantCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
  """
  Create a new tenant (requires superuser). 
  """
  if not current_user.is_superuser:
    raise HTTPException(status_code=403, detail="Not enough permissions")
  
  # Check if slug already exists 
  result = await db.execute(select(TenantModel).where(TenantModel.slug == tenant_in.slug))
  
  if result.scalar_one_or_none():
    raise HTTPException(status_code=400, detail="Slug already exists")
  # Create tenant
  tenant = TenantModel(**tenant_in.model_dump()) 
  db.add(tenant)
  await db.commit()
  await db.refresh(tenant)
  
  return tenant

@router.get("/", response_model=List[Tenant])
async def list_tenants(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
  """
  List all tenants (requires superuser). 
  """
  if not current_user.is_superuser:
    raise HTTPException(status_code=403, detail="Not enough permissions")
  result = await db.execute(select(TenantModel).offset(skip).limit(limit))
  tenants = result.scalars().all()
  
  return tenants

@router.get("/{tenant_id}", response_model=Tenant) 
async def get_tenant( tenant_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
  """
  Gets pecific tenant by ID.
  """
  # Users can only see their own tenant unless superuser
  if not current_user.is_superuser and current_user.tenant_id != tenant_id:
    raise HTTPException(status_code=403, detail="Not enough permissions")
  result = await db.execute( select(TenantModel).where(TenantModel.id == tenant_id)
  )
  tenant = result.scalar_one_or_none()
  if not tenant:
    raise HTTPException(status_code=404, detail="Tenant not found") 
  return tenant