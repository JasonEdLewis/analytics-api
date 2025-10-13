from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker 
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create async engine
# This is THE connection to your database
# Think of this as the "phone line" to your pantry
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_size=settings.DATABASE_POOL_SIZE, max_overflow=settings.DATABASE_MAX_OVERFLOW, pool_pre_ping=True,
                             future=True)
# Session factory
# Each request gets its own "phone call" to the database
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
Base = declarative_base()

async def get_db() -> AsyncSession:
  """
  Dependency that provides a database session.
  This is used in FastAPI endpoints with Depends(get_db) 
  """
  async with AsyncSessionLocal() as session:
      try:
          yield session
          await session.commit()
      except Exception as e:
          await session.rollback()
          raise e
      finally:
          await session.close()