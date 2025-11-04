import asyncio
import sys
from pathlib import Path
# Add parent directory to path 
sys.path.append(str(Path(__file__).parent.parent))
from sqlalchemy import select
from faker import Faker
from datetime import datetime, timedelta, timezone
import random
from app.db.session import AsyncSessionLocal
from app.models.tenant import Tenant as TenantModel 
from app.models.user import User as UserModel
from app.models.event import Event as EventModel
from app.models.api_key import APIKey as APIKeyModel 
from app.core.security import get_password_hash
import secrets

fake = Faker()

async def create_test_tenant():
  """Create a test tenant with user and API key.""" 
  async with AsyncSessionLocal() as db:
    # Create tenant
    tenant = TenantModel(
    name="Test Company", slug="test-company", is_active=True
    ) 
    db.add(tenant) 
    await db.flush()
    # Create user
    user = UserModel(
    tenant_id=tenant.id,
    email="admin@test.com", hashed_password=get_password_hash("password123"), full_name="Test Admin",
    is_active=True,
    is_superuser=True )
    
    db.add(user)
    
    # Create API key
    api_key = APIKeyModel(
    tenant_id=tenant.id, key=secrets.token_urlsafe(32), name="Production Key", is_active=True
    ) 
    db.add(api_key)
    await db.commit()
    await db.refresh(tenant) 
    await db.refresh(user) 
    await db.refresh(api_key)
    print(f" ✅Created tenant: {tenant.name}")
    print(f" User Email: {user.email} ")
    print(f" Password: password123 ")
    print(f" API-key: {api_key.key} ")
    return tenant, user, api_key
  
async def load_events(tenant_id: int, count: int = 10000):
    """Load test events for a tenant."""
    
    # Event types with realistic properties 
    event_templates = [
      {
      "name": "page_view", "properties": lambda: {
      "page": random.choice(["/", "/dashboard", "/settings", "/profile", "/pricing"]), "referrer": random.choice(["google.com", "direct", "facebook.com", "twitter.com"]), "user_id": f"user_{random.randint(1, 1000)}",
      "session_id": fake.uuid4()
      } },
      {
      "name": "button_click", "properties": lambda: {
      "button_id": random.choice(["signup", "login", "purchase", "share", "like"]), "page": random.choice(["/", "/dashboard", "/settings"]),
      "user_id": f"user_{random.randint(1, 1000)}"
      } },
      {
      "name": "purchase", "properties": lambda: {
      "amount": round(random.uniform(10, 500), 2), "currency": "USD",
      "product_id": f"prod_{random.randint(1, 50)}", "user_id": f"user_{random.randint(1, 1000)}"
      } },
      {
      "name": "signup", "properties": lambda: {
      "source": random.choice(["organic", "google_ads", "facebook_ads", "referral"]), "plan": random.choice(["free", "pro", "enterprise"]),
      "email_domain": fake.domain_name()
      } },
      {
      "name": "video_play", "properties": lambda: {
      "video_id": f"video_{random.randint(1, 100)}", "duration": random.randint(30, 600),
      "user_id": f"user_{random.randint(1, 1000)}"
      } }
      ]
    
    print(f"Loading {count} events...")
    
    async with AsyncSessionLocal() as db: 
      batch_size = 1000
    for i in range(0, count, batch_size):
      events = []
      for j in range(batch_size): 
        if i + j >= count:
          break
        # Pick random event template
        template = random.choice(event_templates)
        # Create event with timestamp in the last 30 days
        days_ago = random.uniform(0, 365)
        created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
        event = EventModel( tenant_id=tenant_id, event_name=template["name"], properties=template["properties"](), created_at=created_at
        ) 
        events.append(event)
        db.add_all(events) 
        await db.commit()
        print(f" Loaded {min(i + batch_size, count)}/{count} events...") 
    print(f" ✅ loaded {count} events successfully!")
    
async def main():
  """Main function to load all test data."""
  print(" Loading test data...\n")
  # Check if tenant already exists
  async with AsyncSessionLocal() as db:
    result = await db.execute( select(TenantModel).where(TenantModel.slug == "test-company"))
    tenant = result.scalar_one_or_none()
    if tenant:
      print("Test Company exist already")
      result = await db.execute(select(APIKeyModel).where(APIKeyModel.tenant_id == tenant.id) )
      api_key = result.scalar_one_or_none()
      print(f" API Key: {api_key.key if api_key else 'Not found'}")
    else:
      tenant, user, api_key = await create_test_tenant()
      
    # Load events
    await load_events(tenant.id, count=10000) 
    print("\n ✅ Test data loading complete!") 
    print(f"\n📊 Summary:")
    print("- API running at: http://localhost:8000")
    print("- API docs at: http://localhost:8000/docs")
    print(f"- Test with API Key: {api_key.key if 'api_key' in locals() else 'See above'}")
      
if __name__ == '__main__':
  asyncio.run(main())