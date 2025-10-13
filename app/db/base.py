# app/db/base.py
# Import Base
from app.db.session import Base

# Import all models so Alembic can detect them
from app.models.tenant import Tenant
from app.models.user import User
from app.models.api_key import APIKey
from app.models.event import Event

# This ensures all models are registered with Base.metadata