from sqlalchemy import Column, Integer, String, DateTime, Boolean 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Tenant(Base):
  '''
    Represents a customer company using the analytics service. Each tenant's data is isolated from other tenants.
  '''
  __tablename__ = "tenants"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(255), nullable=False)
  slug = Column(String(100), unique=True, nullable=False, index=True) 
  is_active = Column(Boolean, default=True, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now()) 
  updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  
  # Relationships
  users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
  events = relationship("Event", back_populates="tenant", cascade="all, delete-orphan")
  api_keys = relationship("APIKey", back_populates="tenant", cascade="all, delete-orphan")
  def __repr__(self):
    return f"<Tenant {self.name}>"