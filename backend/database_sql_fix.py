from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables properly
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Database URL from environment with fallback
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in environment variables")
    print("📋 Please check your .env file:")
    print("   DATABASE_URL=postgresql://tantawan_user:IsurThgT@localhost/tantawan_restaurant")
    exit(1)

print(f"✅ Using database: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("💡 Please check:")
    print("   1. PostgreSQL is running: sudo systemctl status postgresql")
    print("   2. Database exists: psql -U tantawan_user -d tantawan_restaurant")
    print("   3. Credentials are correct")
    exit(1)

Base = declarative_base()

# Database Models
class MenuItemDB(Base):
    __tablename__ = "menu_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class OrderDB(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = Column(String, unique=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_notes = Column(Text, nullable=True)
    pickup_time = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to order items
    items = relationship("OrderItemDB", back_populates="order")

class OrderItemDB(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Relationship
    order = relationship("OrderDB", back_populates="items")

class NewsletterDB(Base):
    __tablename__ = "newsletter_subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime, nullable=True)

# Database functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def generate_order_number():
    """Generate unique order number"""
    today = datetime.utcnow().strftime("%Y%m%d")
    
    # Count today's orders
    db = SessionLocal()
    count = db.query(OrderDB).filter(OrderDB.order_number.like(f"TW-{today}-%")).count()
    db.close()
    
    # Generate next number
    next_number = count + 1
    return f"TW-{today}-{next_number:04d}"

# Test database connection
if __name__ == "__main__":
    try:
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("🎉 Database connection successful!")
        
        # Create tables
        create_tables()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")