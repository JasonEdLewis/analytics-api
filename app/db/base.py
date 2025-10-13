# Import all models here so Alembic can detect them from app.db.session import Base
from app.models.tenant import Tenant
from app.models.user import User
from app.models.event import Event 
from app.models.api_key import APIKey