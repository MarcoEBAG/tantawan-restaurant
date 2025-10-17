#!/usr/bin/env python3
"""
Repariertes Seed-Script für Tantawan Restaurant
Lädt .env-Datei korrekt und füllt die Datenbank mit Speisekarte
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# WICHTIG: .env-Datei laden BEVOR andere Imports
ROOT_DIR = Path(__file__).parent
print(f"🔍 Suche .env-Datei in: {ROOT_DIR}")

# .env-Datei laden
env_file = ROOT_DIR / '.env'
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ .env-Datei gefunden und geladen: {env_file}")
else:
    print(f"❌ .env-Datei nicht gefunden: {env_file}")
    sys.exit(1)

# Umgebungsvariablen prüfen
DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

print(f"🔗 DATABASE_URL: {DATABASE_URL}")
print(f"🔐 SECRET_KEY: {'✅ Gesetzt' if SECRET_KEY else '❌ Fehlt'}")

if not DATABASE_URL:
    print("\n❌ FEHLER: DATABASE_URL nicht gefunden!")
    print("💡 Bitte prüfen Sie Ihre .env-Datei:")
    print("   nano .env")
    print("   DATABASE_URL=postgresql://tantawan_user:IsurThgT@localhost/tantawan_restaurant")
    sys.exit(1)

# Jetzt SQLAlchemy importieren
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Database Setup
try:
    print("🔌 Verbinde zur Datenbank...")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Datenbank-Engine erstellt!")
except Exception as e:
    print(f"❌ Datenbankverbindung fehlgeschlagen: {e}")
    print("\n🔧 Lösungsschritte:")
    print("1. PostgreSQL läuft? sudo systemctl status postgresql")
    print("2. Benutzer/Passwort korrekt? psql -U tantawan_user -d tantawan_restaurant")
    print("3. Datenbank existiert?")
    sys.exit(1)

Base = declarative_base()

# Menu Item Model
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

def create_tables():
    """Tabellen erstellen"""
    try:
        print("🏗️ Erstelle Datenbank-Tabellen...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabellen erfolgreich erstellt!")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Erstellen der Tabellen: {e}")
        return False

def test_connection():
    """Datenbankverbindung testen"""
    try:
        print("🧪 Teste Datenbankverbindung...")
        db = SessionLocal()
        result = db.execute("SELECT 1").fetchone()
        db.close()
        print(f"✅ Datenbankverbindung erfolgreich! Ergebnis: {result}")
        return True
    except Exception as e:
        print(f"❌ Datenbankverbindungstest fehlgeschlagen: {e}")
        return False

def seed_menu_items():
    """Speisekarte in Datenbank einfügen"""
    
    menu_items_data = [
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
        {
            "category": "Hauptgerichte",
            "name": "Gebratene Nudeln mit Ente",
            "description": "Breite Reisnudeln mit knuspriger Ente und chinesischem Brokkoli",
            "price": 21.50,
            "image": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=400&h=300&fit=crop&crop=center"
        },
        {
            "category": "Hauptgerichte",
            "name": "Kung Pao Huhn",
            "description": "Scharfes Huhn mit Erdnüssen, Chili und Szechuan-Pfefferkörner",
            "price": 18.20,
            "image": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&crop=center"
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
    
    try:
        print("🍽️ Füge Speisekarte in Datenbank ein...")
        
        db = SessionLocal()
        
        # Alte Menu-Items löschen
        deleted = db.query(MenuItemDB).delete()
        print(f"🗑️ {deleted} alte Menu-Items gelöscht")
        
        # Neue Menu-Items einfügen
        for i, item_data in enumerate(menu_items_data, 1):
            menu_item = MenuItemDB(**item_data)
            db.add(menu_item)
            print(f"➕ {i}/{len(menu_items_data)}: {item_data['name']} - CHF {item_data['price']}")
        
        # Speichern
        db.commit()
        db.close()
        
        print(f"\n🎉 {len(menu_items_data)} Speisekarte-Items erfolgreich eingefügt!")
        print("✅ Seeding abgeschlossen!")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Seeding: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

# Main Execution
if __name__ == "__main__":
    print("🌱 Tantawan Restaurant - Database Seeding")
    print("=" * 50)
    
    # Schritt 1: Verbindung testen
    if not test_connection():
        print("\n🆘 HILFE:")
        print("1. PostgreSQL läuft? sudo systemctl status postgresql")
        print("2. Datenbank erstellt? sudo -u postgres psql")
        print("   CREATE DATABASE tantawan_restaurant;")
        print("3. Benutzer erstellt? CREATE USER tantawan_user WITH PASSWORD 'IsurThgT';")
        print("4. Rechte vergeben? GRANT ALL PRIVILEGES ON DATABASE tantawan_restaurant TO tantawan_user;")
        sys.exit(1)
    
    # Schritt 2: Tabellen erstellen
    if not create_tables():
        print("❌ Tabellen-Erstellung fehlgeschlagen")
        sys.exit(1)
    
    # Schritt 3: Speisekarte einfügen
    if not seed_menu_items():
        print("❌ Speisekarte-Seeding fehlgeschlagen")
        sys.exit(1)
    
    print("\n🎊 ERFOLGREICH! Die Datenbank ist bereit!")
    print("🔥 Starten Sie jetzt den Server mit:")
    print("   python3 server_sql.py")