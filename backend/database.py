from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db.database = db.client[os.environ["DB_NAME"]]
    
    # Create indexes for better performance
    await create_indexes()


async def close_mongo_connection():
    """Close database connection"""
    db.client.close()


async def create_indexes():
    """Create database indexes for optimal performance"""
    try:
        # Menu items indexes
        await db.database.menu_items.create_index("category")
        await db.database.menu_items.create_index("available")
        
        # Orders indexes
        await db.database.orders.create_index("status")
        await db.database.orders.create_index("created_at")
        await db.database.orders.create_index("order_number", unique=True)
        await db.database.orders.create_index("customer.phone")
        
        # Newsletter subscriptions indexes
        await db.database.newsletter_subscriptions.create_index("email", unique=True)
        await db.database.newsletter_subscriptions.create_index("is_active")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not create indexes: {e}")


async def generate_order_number():
    """Generate unique order number in format TW-YYYYMMDD-XXXX"""
    today = datetime.utcnow().strftime("%Y%m%d")
    
    # Count today's orders
    count = await db.database.orders.count_documents({
        "order_number": {"$regex": f"^TW-{today}-"}
    })
    
    # Generate next number
    next_number = count + 1
    return f"TW-{today}-{next_number:04d}"