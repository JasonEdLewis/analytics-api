import asyncio
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import secrets
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.models.api_key import APIKey
from app.core.security import get_password_hash

async def create_test_data():
    async with AsyncSessionLocal() as db:
        # Check if tenant exists
        result = await db.execute(
            select(Tenant).where(Tenant.slug == "test-company")
        )
        tenant = result.scalar_one_or_none()
        
        if not tenant:
            # Create tenant
            tenant = Tenant(
                name="Test Company",
                slug="test-company",
                is_active=True
            )
            db.add(tenant)
            await db.flush()
        
        # Check if user exists
        result = await db.execute(
            select(User).where(User.email == "admin@test.com")
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create user
            user = User(
                tenant_id=tenant.id,
                email="admin@test.com",
                hashed_password=get_password_hash("password123"),
                full_name="Test Admin",
                is_active=True,
                is_superuser=True
            )
            db.add(user)
        
        # Check if API key exists
        result = await db.execute(
            select(APIKey).where(APIKey.tenant_id == tenant.id)
        )
        api_key = result.scalar_one_or_none()
        
        if not api_key:
            # Create API key
            key = secrets.token_urlsafe(32)
            api_key = APIKey(
                tenant_id=tenant.id,
                key=key,
                name="Test API Key",
                is_active=True
            )
            db.add(api_key)
        
        await db.commit()
        
        print("✅ Test data created!")
        print(f"📧 Email: admin@test.com")
        print(f"🔑 Password: password123")
        print(f"🔐 API Key: {api_key.key}")
        print(f"\n📝 Copy the API Key above - you'll need it!")

if __name__ == "__main__":
    asyncio.run(create_test_data())
