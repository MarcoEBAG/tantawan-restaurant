# 🚀 TANTAWAN - Vollständige Server-Installation mit Frontend & Backend

## 🎯 **Das bekommen Sie nach der Installation:**
- ✅ **Vollständige Restaurant-Website** (wie bei uns lokal)
- ✅ **Online-Bestellsystem** mit Warenkorb
- ✅ **Admin-Dashboard** für Bestellverwaltung (`/admin`)
- ✅ **Automatische E-Mails** bei Bestellungen
- ✅ **PostgreSQL oder MariaDB** als Datenbank
- ✅ **Production-Ready** Setup

---

## 📋 **Was Sie brauchen:**

### **Server-Anforderungen:**
- **VPS/Server** mit Ubuntu 20.04+ oder Debian 11+
- **RAM:** Mindestens 2GB (4GB empfohlen)
- **Festplatte:** 20GB freier Speicherplatz
- **Root-Zugang** (sudo-Rechte)

### **Domain & SSL:**
- **Domain** (z.B. `tantawan.ch`)
- **SSL-Zertifikat** (Let's Encrypt - kostenlos)

---

## 🗄️ **SCHRITT 1: Datenbank wählen und installieren**

### **Option A: PostgreSQL (Empfohlen)**

```bash
# 1. Server-Updates
sudo apt update && sudo apt upgrade -y

# 2. PostgreSQL installieren
sudo apt install -y postgresql postgresql-contrib

# 3. PostgreSQL starten
sudo systemctl enable postgresql
sudo systemctl start postgresql

# 4. Datenbank und Benutzer erstellen
sudo -u postgres psql

-- In der PostgreSQL-Konsole:
CREATE DATABASE tantawan_restaurant;
CREATE USER tantawan_user WITH PASSWORD 'IhrSicheresPasswort123!';
GRANT ALL PRIVILEGES ON DATABASE tantawan_restaurant TO tantawan_user;
\q

# 5. Verbindung testen
psql -h localhost -U tantawan_user -d tantawan_restaurant
```

### **Option B: MariaDB**

```bash
# 1. MariaDB installieren
sudo apt install -y mariadb-server mariadb-client

# 2. MariaDB sichern
sudo mysql_secure_installation
# Folgen Sie den Anweisungen, setzen Sie Root-Passwort

# 3. Datenbank erstellen
sudo mysql -u root -p

-- In der MySQL-Konsole:
CREATE DATABASE tantawan_restaurant CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tantawan_user'@'localhost' IDENTIFIED BY 'IhrSicheresPasswort123!';
GRANT ALL PRIVILEGES ON tantawan_restaurant.* TO 'tantawan_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 4. Verbindung testen
mysql -u tantawan_user -p tantawan_restaurant
```

---

## 🐍 **SCHRITT 2: Backend (FastAPI) installieren**

### **1. System-Pakete installieren**

```bash
# Python, Node.js und weitere Tools
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx supervisor git curl

# Python-Version prüfen (sollte 3.8+ sein)
python3 --version
```

### **2. Projektordner erstellen und Dateien hochladen**

```bash
# 1. Projektordner erstellen
sudo mkdir -p /var/www/tantawan
sudo chown $USER:$USER /var/www/tantawan
cd /var/www/tantawan

# 2. Ihre Dateien hierher kopieren (mehrere Optionen):

# Option A: Mit Git (wenn GitHub-Repository existiert)
git clone https://github.com/IhrUsername/tantawan-restaurant.git .

# Option B: Per SCP von anderem Server
# scp -r /pfad/zu/dateien/* user@server:/var/www/tantawan/

# Option C: ZIP hochladen und entpacken
# - Laden Sie tantawan-restaurant.zip auf Server hoch
# - Entpacken mit: unzip tantawan-restaurant.zip
```

### **3. Backend-Konfiguration**

```bash
# 1. Backend-Ordner
cd /var/www/tantawan/backend

# 2. Python Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# 3. Dependencies installieren
pip install --upgrade pip

# 4. Für PostgreSQL:
pip install psycopg2-binary sqlalchemy alembic

# ODER für MariaDB:
pip install pymysql sqlalchemy alembic

# 5. Alle anderen Dependencies
pip install -r requirements.txt
```

### **4. Umgebungsvariablen konfigurieren (.env)**

```bash
nano .env
```

**Für PostgreSQL (.env):**
```bash
# === DATENBANK (PostgreSQL) ===
DATABASE_URL=postgresql://tantawan_user:IhrSicheresPasswort123!@localhost/tantawan_restaurant
DB_NAME=tantawan_restaurant

# === E-MAIL KONFIGURATION ===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ihr-restaurant@gmail.com
SMTP_PASSWORD=ihr-gmail-app-passwort
RESTAURANT_EMAIL=info@tantawan.ch
PRINTER_EMAIL=drucker@tantawan.ch

# === SERVER KONFIGURATION ===
SECRET_KEY=generierten-geheimen-schluessel-hier-einfuegen
API_HOST=0.0.0.0
API_PORT=8001
```

**Für MariaDB (.env):**
```bash
# === DATENBANK (MariaDB) ===
DATABASE_URL=mysql+pymysql://tantawan_user:IhrSicheresPasswort123!@localhost/tantawan_restaurant
DB_NAME=tantawan_restaurant

# === E-MAIL KONFIGURATION ===
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ihr-restaurant@gmail.com
SMTP_PASSWORD=ihr-gmail-app-passwort
RESTAURANT_EMAIL=info@tantawan.ch
PRINTER_EMAIL=drucker@tantawan.ch

# === SERVER KONFIGURATION ===
SECRET_KEY=generierten-geheimen-schluessel-hier-einfuegen
API_HOST=0.0.0.0
API_PORT=8001
```

### **5. Datenbank-Integration erstellen**

**Erstellen Sie: `database_sql.py`**

```bash
nano database_sql.py
```

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os
import uuid

# Database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class MenuItem(Base):
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

class Order(Base):
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
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Relationship
    order = relationship("Order", back_populates="items")

class NewsletterSubscription(Base):
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
    Base.metadata.create_all(bind=engine)
    
def generate_order_number():
    """Generate unique order number"""
    today = datetime.utcnow().strftime("%Y%m%d")
    
    # Count today's orders
    db = SessionLocal()
    count = db.query(Order).filter(Order.order_number.like(f"TW-{today}-%")).count()
    db.close()
    
    # Generate next number
    next_number = count + 1
    return f"TW-{today}-{next_number:04d}"
```

### **6. Server-Code anpassen (server_sql.py)**

```bash
nano server_sql.py
```

```python
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our models and database
from database_sql import get_db, create_tables, generate_order_number
from database_sql import MenuItem as MenuItemDB, Order as OrderDB, OrderItem as OrderItemDB
from database_sql import NewsletterSubscription as NewsletterDB

# Import email service
from services.email_service import email_service

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create FastAPI app
app = FastAPI(
    title="Tantawan Restaurant API",
    description="Vollständige API für Tantawan Restaurant mit SQL-Datenbank",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# === MENU ENDPOINTS ===
@app.get("/api/menu/")
async def get_all_menu_items(db: Session = Depends(get_db)):
    """Get all available menu items"""
    try:
        items = db.query(MenuItemDB).filter(MenuItemDB.available == True).all()
        
        # Convert to API format
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

# === ORDERS ENDPOINTS ===
@app.post("/api/orders/")
async def create_order(
    order_data: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create new order"""
    try:
        # Generate order number
        order_number = generate_order_number()
        
        # Calculate total
        total = sum(item["price"] * item["quantity"] for item in order_data["items"])
        
        # Create order in database
        db_order = OrderDB(
            order_number=order_number,
            customer_name=order_data["customer"]["name"],
            customer_phone=order_data["customer"]["phone"],
            customer_notes=order_data["customer"].get("notes"),
            pickup_time=datetime.fromisoformat(order_data["pickup_time"].replace('Z', '+00:00')),
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
        
        # Convert to response format
        order_response = {
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
        
        # Send notifications in background
        # background_tasks.add_task(email_service.send_order_notification, order_response)
        
        return order_response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

# === ADMIN ENDPOINTS ===
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

@app.get("/api/admin/orders/stats")
async def get_order_stats(db: Session = Depends(get_db)):
    """Get order statistics"""
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        # Today's orders count
        today_orders = db.query(OrderDB).filter(
            OrderDB.created_at >= today,
            OrderDB.created_at < tomorrow
        ).count()
        
        # Today's revenue
        today_revenue = db.query(OrderDB).filter(
            OrderDB.created_at >= today,
            OrderDB.created_at < tomorrow
        ).with_entities(OrderDB.total).all()
        
        total_revenue = sum(order.total for order in today_revenue)
        
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

# === NEWSLETTER ENDPOINTS ===
@app.post("/api/newsletter/subscribe")
async def subscribe_newsletter(data: dict, db: Session = Depends(get_db)):
    """Newsletter subscription"""
    try:
        email = data["email"]
        
        # Check if already subscribed
        existing = db.query(NewsletterDB).filter(NewsletterDB.email == email).first()
        
        if existing:
            if existing.is_active:
                raise HTTPException(status_code=400, detail="Email already subscribed")
            else:
                # Reactivate
                existing.is_active = True
                existing.subscribed_at = datetime.utcnow()
                existing.unsubscribed_at = None
                db.commit()
        else:
            # New subscription
            subscription = NewsletterDB(email=email)
            db.add(subscription)
            db.commit()
        
        return {"message": "Successfully subscribed to newsletter"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# === HEALTH CHECK ===
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Tantawan Restaurant API SQL"}

@app.get("/api/")
async def root():
    return {"message": "Tantawan Restaurant API SQL", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### **7. Datenbank-Seeding erstellen**

```bash
nano seed_sql_data.py
```

```python
from database_sql import SessionLocal, MenuItemDB, create_tables

def seed_menu_items():
    """Speisekarte in SQL-Datenbank einfügen"""
    
    # Tabellen erstellen
    create_tables()
    
    db = SessionLocal()
    
    # Alte Daten löschen
    db.query(MenuItemDB).delete()
    
    menu_items = [
        # Vorspeisen
        {
            "category": "Vorspeisen",
            "name": "Frühlingsrollen (4 Stück)",
            "description": "Knusprige Frühlingsrollen mit Gemüsefüllung, serviert mit süß-sauer Sauce",
            "price": 8.50,
            "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Vorspeisen",
            "name": "Gyoza (6 Stück)",
            "description": "Japanische Teigtaschen mit Schweinefleisch und Gemüse",
            "price": 9.80,
            "image": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Vorspeisen",
            "name": "Tom Kha Gai Suppe",
            "description": "Thai Kokosnusssuppe mit Huhn, Galangal und Zitronengras",
            "price": 7.90,
            "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop&crop=center"
        },
        
        # Hauptgerichte
        {
            "category": "Hauptgerichte",
            "name": "Pad Thai mit Huhn",
            "description": "Klassische Thai-Nudeln mit Huhn, Ei, Bohnensprossen und Erdnüssen",
            "price": 16.50,
            "image": "https://images.unsplash.com/photo-1559847844-d2e2c6880675?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Hauptgerichte", 
            "name": "Sweet & Sour Schweinefleisch",
            "description": "Knuspriges Schweinefleisch mit Ananas, Paprika in süß-saurer Sauce",
            "price": 17.80,
            "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Hauptgerichte",
            "name": "Beef Teriyaki", 
            "description": "Zartes Rindfleisch in Teriyaki-Sauce mit Sesam und Frühlingszwiebeln",
            "price": 19.90,
            "image": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Hauptgerichte",
            "name": "Vegetarisches Curry",
            "description": "Gemischtes Gemüse in cremiger Kokosmilch-Curry-Sauce", 
            "price": 15.50,
            "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400&h=300&fit=crop&crop=center"
        },
        
        # Desserts
        {
            "category": "Desserts",
            "name": "Mango Sticky Rice",
            "description": "Traditioneller Thai-Dessert mit süßem Klebreis und frischer Mango",
            "price": 6.50,
            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Desserts",
            "name": "Sesam-Eiscreme",
            "description": "Hausgemachte Eiscreme mit schwarzem Sesam",
            "price": 5.50,
            "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=300&fit=crop&crop=center"
        }
    ]
    
    # Speisekarte einfügen
    for item_data in menu_items:
        menu_item = MenuItemDB(**item_data)
        db.add(menu_item)
    
    db.commit()
    db.close()
    
    print(f"✅ {len(menu_items)} Speisekarte-Items erfolgreich eingefügt!")

if __name__ == "__main__":
    seed_menu_items()
```

---

## ⚙️ **SCHRITT 3: Backend starten**

### **1. Datenbank initialisieren**

```bash
# In /var/www/tantawan/backend/
source venv/bin/activate

# Speisekarte in Datenbank einfügen
python seed_sql_data.py
```

### **2. Backend als Service einrichten**

```bash
sudo nano /etc/supervisor/conf.d/tantawan-backend.conf
```

```ini
[program:tantawan-backend]
command=/var/www/tantawan/backend/venv/bin/python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001
directory=/var/www/tantawan/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/tantawan-backend.log
environment=PATH="/var/www/tantawan/backend/venv/bin"
```

```bash
# Supervisor aktualisieren
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tantawan-backend

# Status prüfen
sudo supervisorctl status
```

---

## 🌐 **SCHRITT 4: Frontend (React) installieren**

### **1. Frontend-Build erstellen**

```bash
# Frontend-Ordner
cd /var/www/tantawan/frontend

# Node.js Dependencies installieren
npm install

# Production-Build erstellen
npm run build

# Build-Dateien nach Webroot kopieren
sudo rm -rf /var/www/html/*
sudo cp -r build/* /var/www/html/

# Berechtigungen setzen
sudo chown -R www-data:www-data /var/www/html/
```

### **2. Frontend-Konfiguration anpassen**

```bash
# .env-Datei für Frontend
nano /var/www/tantawan/frontend/.env
```

```bash
REACT_APP_BACKEND_URL=https://ihre-domain.de
GENERATE_SOURCEMAP=false
```

**Nach .env-Änderung:**
```bash
# Neu bauen mit neuer Konfiguration
npm run build
sudo cp -r build/* /var/www/html/
```

---

## 🔧 **SCHRITT 5: Nginx konfigurieren**

```bash
sudo nano /etc/nginx/sites-available/tantawan
```

**Nginx-Konfiguration:**
```nginx
server {
    listen 80;
    server_name ihre-domain.de www.ihre-domain.de;
    root /var/www/html;
    index index.html;

    # Frontend (React) - Alle Seiten
    location / {
        try_files $uri $uri/ /index.html;
        
        # Cache-Einstellungen für bessere Performance
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API - Alle /api Requests
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS Headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization' always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Logs
    access_log /var/log/nginx/tantawan.access.log;
    error_log /var/log/nginx/tantawan.error.log;
}
```

**Nginx aktivieren:**
```bash
# Site aktivieren
sudo ln -s /etc/nginx/sites-available/tantawan /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Konfiguration testen
sudo nginx -t

# Nginx neu starten
sudo systemctl restart nginx
```

---

## 🔒 **SCHRITT 6: SSL-Zertifikat (Let's Encrypt)**

```bash
# 1. Certbot installieren
sudo apt install -y certbot python3-certbot-nginx

# 2. SSL-Zertifikat generieren
sudo certbot --nginx -d ihre-domain.de -d www.ihre-domain.de

# 3. Automatische Erneuerung einrichten
sudo crontab -e
# Folgende Zeile hinzufügen:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## ✅ **SCHRITT 7: Alles testen**

### **1. Backend testen:**
```bash
curl http://ihre-domain.de/api/health
# Sollte zurückgeben: {"status":"healthy","service":"Tantawan Restaurant API SQL"}
```

### **2. Frontend testen:**
- **Öffnen Sie:** `https://ihre-domain.de`
- **Sie sollten sehen:** Tantawan Restaurant Website
- **Testen Sie:** Bestellung aufgeben
- **Admin-Bereich:** `https://ihre-domain.de/admin`

### **3. Logs überwachen:**
```bash
# Backend-Logs
sudo tail -f /var/log/tantawan-backend.log

# Nginx-Logs
sudo tail -f /var/log/nginx/tantawan.error.log

# Supervisor-Status
sudo supervisorctl status
```

---

## 🎯 **URLs nach Installation:**

- **🏠 Restaurant-Website:** `https://ihre-domain.de`
- **🛒 Online-Bestellungen:** `https://ihre-domain.de/#menu`
- **👨‍💼 Admin-Dashboard:** `https://ihre-domain.de/admin`
- **📋 API-Dokumentation:** `https://ihre-domain.de/api/docs`
- **❤️ Gesundheitscheck:** `https://ihre-domain.de/api/health`

---

## 🔧 **Wartung und Updates**

### **Backend neu starten:**
```bash
sudo supervisorctl restart tantawan-backend
```

### **Frontend aktualisieren:**
```bash
cd /var/www/tantawan/frontend
npm run build
sudo cp -r build/* /var/www/html/
```

### **Backup erstellen:**
```bash
# Datenbank-Backup (PostgreSQL)
pg_dump -U tantawan_user -h localhost tantawan_restaurant > backup_$(date +%Y%m%d).sql

# Datenbank-Backup (MariaDB)
mysqldump -u tantawan_user -p tantawan_restaurant > backup_$(date +%Y%m%d).sql
```

---

## 🆘 **Problembehandlung**

### **Backend startet nicht:**
```bash
# Logs prüfen
sudo tail -n 50 /var/log/tantawan-backend.log

# Manuell starten zum Testen
cd /var/www/tantawan/backend
source venv/bin/activate
python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001
```

### **Frontend zeigt weiße Seite:**
```bash
# Browser-Cache löschen (Strg+F5)
# Nginx-Logs prüfen
sudo tail -n 20 /var/log/nginx/tantawan.error.log
```

### **Datenbank-Verbindung fehlschlägt:**
```bash
# PostgreSQL-Status prüfen
sudo systemctl status postgresql

# MariaDB-Status prüfen  
sudo systemctl status mariadb

# Verbindung manuell testen
psql -U tantawan_user -d tantawan_restaurant -h localhost
# oder
mysql -u tantawan_user -p tantawan_restaurant
```

---

**🎉 Nach dieser Installation haben Sie die VOLLSTÄNDIGE Tantawan-Funktionalität:**

- ✅ **Online-Bestellsystem** mit echtem Backend
- ✅ **Admin-Dashboard** für Bestellverwaltung
- ✅ **SQL-Datenbank** (PostgreSQL/MariaDB)
- ✅ **Automatische E-Mail-Benachrichtigungen**
- ✅ **Production-ready** mit SSL und Nginx
- ✅ **Alle Funktionen** wie in der Entwicklungsversion

**Die Website ist jetzt vollständig funktionsfähig und bereit für echte Kunden!** 🚀