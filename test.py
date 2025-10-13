# test_setup.py
import asyncio
from app.core.config import settings
from app.db.session import engine, Base
from sqlalchemy import text

async def test_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL: {version}")
            
            # Check if tables exist
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Analytics API Setup")
    print("=" * 50)
    print(f"\n📊 Database URL: {settings.DATABASE_URL.split('@')[1]}")  # Hide password
    print(f"🔐 Secret Key: {'*' * 20} (set)")
    print()
    
    asyncio.run(test_connection())