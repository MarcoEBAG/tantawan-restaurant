# 🔧 .env Problem lösen - SECRET_KEY & DATABASE_URL

## ❌ **Das Problem:**
```
DATABASE_URL ist None - die .env-Datei wird nicht gelesen
```

## ✅ **Die Lösung - Schritt für Schritt:**

---

## **SCHRITT 1: .env-Datei richtig erstellen**

```bash
# 1. In den Backend-Ordner gehen
cd /var/www/tantawan/backend

# 2. Prüfen ob .env-Datei existiert
ls -la .env

# 3. .env-Datei erstellen (falls nicht vorhanden)
nano .env
```

**📝 Kopieren Sie EXAKT folgenden Inhalt in die .env-Datei:**

```bash
# === DATENBANK KONFIGURATION ===
DATABASE_URL=postgresql://tantawan_user:IsurThgT@localhost/tantawan_restaurant
DB_NAME=tantawan_restaurant

# === SICHERHEIT ===
SECRET_KEY=BAWB-C2iLZ0N1bNLrj6lEw1kHC0GGcetQvBGfLElNnc

# === E-MAIL KONFIGURATION ===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ihr-restaurant@gmail.com
SMTP_PASSWORD=ihr-gmail-app-passwort
RESTAURANT_EMAIL=info@tantawan.ch
PRINTER_EMAIL=drucker@tantawan.ch

# === SERVER KONFIGURATION ===
API_HOST=0.0.0.0
API_PORT=8001
```

**💾 Speichern:**
- Drücken Sie `Ctrl+X`
- Dann `Y` für "Yes"
- Dann `Enter`

---

## **SCHRITT 2: .env-Datei testen**

```bash
# 1. Prüfen ob Datei korrekt gespeichert wurde
cat .env

# 2. Umgebungsvariablen testen
python3 -c "
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv('.env')
print('DATABASE_URL:', os.environ.get('DATABASE_URL'))
print('SECRET_KEY:', os.environ.get('SECRET_KEY'))
"
```

**✅ Erwartete Ausgabe:**
```
DATABASE_URL: postgresql://tantawan_user:IsurThgT@localhost/tantawan_restaurant  
SECRET_KEY: BAWB-C2iLZ0N1bNLrj6lEw1kHC0GGcetQvBGfLElNnc
```

---

## **SCHRITT 3: python-dotenv installieren (falls fehlt)**

```bash
# 1. Virtual Environment aktivieren
source venv/bin/activate

# 2. python-dotenv installieren
pip install python-dotenv

# 3. Alle Dependencies nochmal installieren
pip install -r requirements.txt
```

---

## **SCHRITT 4: Feste Database-URL verwenden (Notlösung)**

**Falls .env immer noch Probleme macht, erstellen Sie:**

```bash
nano database_direct.py
```

**📝 Inhalt:**

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import uuid

# === DIREKTE DATABASE_URL (Ihre Credentials) ===
DATABASE_URL = "postgresql://tantawan_user:IsurThgT@localhost/tantawan_restaurant"
SECRET_KEY = "BAWB-C2iLZ0N1bNLrj6lEw1kHC0GGcetQvBGfLElNnc"

print(f"🔗 Connecting to database: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Database engine created successfully!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
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
        print("🏗️ Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection test successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def generate_order_number():
    """Generate unique order number"""
    today = datetime.utcnow().strftime("%Y%m%d")
    
    # Count today's orders
    db = SessionLocal()
    try:
        count = db.query(OrderDB).filter(OrderDB.order_number.like(f"TW-{today}-%")).count()
        db.close()
        
        # Generate next number
        next_number = count + 1
        return f"TW-{today}-{next_number:04d}"
    except Exception as e:
        print(f"Error generating order number: {e}")
        db.close()
        return f"TW-{today}-0001"

# Main execution
if __name__ == "__main__":
    print("🧪 Testing Tantawan Database Connection...")
    
    # Test connection
    if test_connection():
        # Create tables
        if create_tables():
            print("🎉 Database setup completed successfully!")
        else:
            print("❌ Failed to create tables")
    else:
        print("❌ Database connection failed")
        print("\n🔧 Troubleshooting:")
        print("1. Check if PostgreSQL is running: sudo systemctl status postgresql")
        print("2. Check if database exists: psql -U tantawan_user -d tantawan_restaurant")
        print("3. Check credentials in DATABASE_URL")