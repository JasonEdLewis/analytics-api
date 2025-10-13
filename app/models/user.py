from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
  """
  Users belong to a tenant and can authenticate to access the API. 
  """
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
  email = Column(String(255), unique=True, nullable=False, index=True) 
  hashed_password = Column(String(255), nullable=False)
  full_name = Column(String(255))
  is_active = Column(Boolean, default=True, nullable=False)
  is_superuser = Column(Boolean, default=False, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now()) 
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  
  # Relationships
  tenant = relationship("Tenant", back_populates="users")
  def __repr__(self):
    return f"<User {self.email}>"