from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index 
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Event(Base):
  """
  Stores analytics events from tenant applications. Properties field uses JSONB for flexible schema.
      Example event: {
      "event_name": "page_view",
        "properties": {
            "page": "/dashboard", 
            "referrer": "google.com", 
            "user_id": "user_123", 
            "session_id": "session_abc"
        } 
      }
  """
  __tablename__ = "events"
  id = Column(Integer, primary_key=True, index=True)
  tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False) 
  event_name = Column(String(255), nullable=False, index=True)
  
  # JSONB allows flexible properties without rigid schema
  # This is POWERFUL for analytics where properties vary by event type
  properties = Column(JSONB, nullable=False, default={})

  # Timestamps
  created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  # Relationships
  tenant = relationship("Tenant", back_populates="events")

  # Composite index for common query pattern
  __table_args__ = (
      Index('idx_tenant_event_created', 'tenant_id', 'event_name', 'created_at'),
      Index('idx_tenant_created', 'tenant_id', 'created_at'),
      # GIN index for JSONB queries
      Index('idx_event_properties', 'properties', postgresql_using='gin'),
  )

def __repr__(self):
    return f"<Event {self.event_name} at {self.created_at}>"