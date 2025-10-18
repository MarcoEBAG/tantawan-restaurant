#!/usr/bin/env python3
"""
FUNKTIONIERENDER Tantawan Server mit korrekter .env-Ladung
"""

import os
import sys
from pathlib import Path

# === .ENV-DATEI KORREKT LADEN ===
# Ermittelt das tatsächliche Script-Verzeichnis (nicht working directory!)
SCRIPT_DIR = Path(__file__).parent.absolute()
ENV_FILE = SCRIPT_DIR / '.env'

print(f"🔍 Script läuft von: {SCRIPT_DIR}")
print(f"🔍 Suche .env-Datei: {ENV_FILE}")

if ENV_FILE.exists():
    # .env manuell laden
    with open(ENV_FILE, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    print(f"✅ .env-Datei manuell geladen!")
else:
    print(f"❌ .env-Datei nicht gefunden: {ENV_FILE}")
    sys.exit(1)

# Jetzt Umgebungsvariablen prüfen
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

print(f"🔗 DATABASE_URL: {DATABASE_URL}")
print(f"🔐 SECRET_KEY: {'✅ Gesetzt' if SECRET_KEY else '❌ Fehlt'}")

if not DATABASE_URL:
    print("❌ DATABASE_URL nicht gefunden!")
    sys.exit(1)

# Jetzt erst die anderen Imports
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, Integer, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List, Dict, Any
from datetime import datetime, timedelta
import uuid

# Database Setup
try:
    print("🔌 Erstelle Datenbank-Engine...")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Datenbank-Engine erfolgreich erstellt!")
except Exception as e:
    print(f"❌ Datenbankverbindung fehlgeschlagen: {e}")
    sys.exit(1)

Base = declarative_base()

# === DATABASE MODELS ===
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

class OrderItemDB(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

class NewsletterDB(Base):
    __tablename__ = "newsletter_subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime, nullable=True)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_order_number():
    """Generate unique order number"""
    today = datetime.utcnow().strftime("%Y%m%d")
    
    # Count today's orders
    db = SessionLocal()
    try:
        count = db.query(OrderDB).filter(OrderDB.order_number.like(f"TW-{today}-%")).count()
        next_number = count + 1
        return f"TW-{today}-{next_number:04d}"
    finally:
        db.close()

# === FASTAPI APP ===
app = FastAPI(
    title="Tantawan Restaurant API",
    description="SQL-basierte API für Tantawan Restaurant",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === STARTUP ===
@app.on_event("startup")
async def startup_event():
    try:
        print("🏗️ Erstelle Datenbank-Tabellen...")
        Base.metadata.create_all(bind=engine)
        print("✅ Startup erfolgreich!")
    except Exception as e:
        print(f"❌ Startup-Fehler: {e}")

# === ENDPOINTS ===
@app.get("/")
async def root():
    return {"message": "Tantawan Restaurant API SQL", "version": "2.0.0", "status": "healthy"}

@app.get("/api/")
async def api_root():
    return {"message": "Tantawan Restaurant API SQL", "version": "2.0.0", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    try:
        # Test database connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected", "service": "Tantawan Restaurant API SQL"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.get("/api/menu/")
async def get_all_menu_items(db: Session = Depends(get_db)):
    """Get all available menu items"""
    try:
        items = db.query(MenuItemDB).filter(MenuItemDB.available == True).all()
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "category": item.category,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "image": item.image,
                "available": item.available,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/menu/{category}")
async def get_menu_items_by_category(category: str, db: Session = Depends(get_db)):
    """Get menu items by category"""
    try:
        items = db.query(MenuItemDB).filter(
            MenuItemDB.category == category,
            MenuItemDB.available == True
        ).all()
        
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "category": item.category,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "image": item.image,
                "available": item.available
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/orders/")
async def create_order(order_data: Dict[Any, Any], db: Session = Depends(get_db)):
    """Create new order"""
    try:
        # Generate order number
        order_number = generate_order_number()
        
        # Calculate total
        total = sum(item["price"] * item["quantity"] for item in order_data["items"])
        
        # Parse pickup time
        pickup_time_str = order_data["pickup_time"]
        if pickup_time_str.endswith('Z'):
            pickup_time_str = pickup_time_str[:-1] + '+00:00'
        pickup_time = datetime.fromisoformat(pickup_time_str)
        
        # Create order
        db_order = OrderDB(
            order_number=order_number,
            customer_name=order_data["customer"]["name"],
            customer_phone=order_data["customer"]["phone"],
            customer_notes=order_data["customer"].get("notes"),
            pickup_time=pickup_time,
            total=total,
            status="pending"
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Create order items
        for item_data in order_data["items"]:
            order_item = OrderItemDB(
                order_id=db_order.id,
                menu_item_id=item_data["menu_item_id"],
                name=item_data["name"],
                price=item_data["price"],
                quantity=item_data["quantity"]
            )
            db.add(order_item)
        
        db.commit()
        
        # Response format
        return {
            "id": db_order.id,
            "order_number": db_order.order_number,
            "customer": {
                "name": db_order.customer_name,
                "phone": db_order.customer_phone,
                "notes": db_order.customer_notes
            },
            "pickup_time": db_order.pickup_time.isoformat(),
            "total": db_order.total,
            "status": db_order.status,
            "created_at": db_order.created_at.isoformat(),
            "items": order_data["items"]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@app.get("/api/admin/orders/pending")
async def get_pending_orders(db: Session = Depends(get_db)):
    """Get pending orders for kitchen"""
    try:
        orders = db.query(OrderDB).filter(
            OrderDB.status.in_(["pending", "confirmed", "preparing"])
        ).order_by(OrderDB.created_at).all()
        
        result = []
        for order in orders:
            # Get order items
            items = db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
            
            result.append({
                "id": order.id,
                "order_number": order.order_number,
                "customer": {
                    "name": order.customer_name,
                    "phone": order.customer_phone,
                    "notes": order.customer_notes
                },
                "pickup_time": order.pickup_time.isoformat(),
                "total": order.total,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "items": [{
                    "name": item.name,
                    "price": item.price,
                    "quantity": item.quantity
                } for item in items]
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/admin/orders/today")
async def get_todays_orders(db: Session = Depends(get_db)):
    """Get today's orders"""
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        orders = db.query(OrderDB).filter(
            OrderDB.created_at >= today,
            OrderDB.created_at < tomorrow
        ).order_by(OrderDB.created_at.desc()).all()
        
        result = []
        for order in orders:
            items = db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
            
            result.append({
                "id": order.id,
                "order_number": order.order_number,
                "customer": {
                    "name": order.customer_name,
                    "phone": order.customer_phone,
                    "notes": order.customer_notes
                },
                "pickup_time": order.pickup_time.isoformat(),
                "total": order.total,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "items": [{
                    "name": item.name,
                    "price": item.price,
                    "quantity": item.quantity
                } for item in items]
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/admin/orders/stats")
async def get_order_stats(db: Session = Depends(get_db)):
    """Get order statistics"""
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        # Today's orders
        today_orders = db.query(OrderDB).filter(
            OrderDB.created_at >= today,
            OrderDB.created_at < tomorrow
        ).count()
        
        # Today's revenue
        today_revenue_result = db.query(OrderDB).filter(
            OrderDB.created_at >= today,
            OrderDB.created_at < tomorrow
        ).all()
        
        total_revenue = sum(order.total for order in today_revenue_result)
        
        # Pending orders
        pending_orders = db.query(OrderDB).filter(
            OrderDB.status.in_(["pending", "confirmed", "preparing"])
        ).count()
        
        return {
            "today": {
                "orders": today_orders,
                "revenue": round(total_revenue, 2)
            },
            "pending_orders": pending_orders,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/api/admin/orders/{order_id}/status")
async def update_order_status(order_id: str, status_data: Dict[str, str], db: Session = Depends(get_db)):
    """Update order status"""
    try:
        order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = status_data["status"]
        order.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "updated_at": order.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/newsletter/subscribe")
async def subscribe_newsletter(data: Dict[str, str], db: Session = Depends(get_db)):
    """Newsletter subscription"""
    try:
        email = data["email"]
        
        # Check if already exists
        existing = db.query(NewsletterDB).filter(NewsletterDB.email == email).first()
        
        if existing:
            if existing.is_active:
                raise HTTPException(status_code=400, detail="Email is already subscribed to newsletter")
            else:
                # Reactivate
                existing.is_active = True
                existing.subscribed_at = datetime.utcnow()
                existing.unsubscribed_at = None
        else:
            # New subscription
            subscription = NewsletterDB(email=email)
            db.add(subscription)
        
        db.commit()
        
        return {
            "message": "Successfully subscribed to newsletter",
            "subscription": {
                "email": email,
                "subscribed_at": datetime.utcnow().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/newsletter/subscriptions/count")
async def get_subscription_count(db: Session = Depends(get_db)):
    """Get newsletter subscription count"""
    try:
        count = db.query(NewsletterDB).filter(NewsletterDB.is_active == True).count()
        return {"active_subscriptions": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# === STARTUP TEST ===
@app.on_event("startup")
async def startup_event():
    try:
        print("🚀 Tantawan API startet...")
        
        # Test database connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Datenbankverbindung erfolgreich!")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tabellen erstellt/überprüft!")
        
        print("🎉 Tantawan API bereit!")
        
    except Exception as e:
        print(f"❌ Startup-Fehler: {e}")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starte Tantawan Restaurant API...")
    print(f"🌐 Server läuft auf: http://0.0.0.0:8001")
    print(f"📋 API Docs: http://0.0.0.0:8001/docs")
    print("🔴 Zum Beenden: Ctrl+C drücken")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        log_level="info"
    )