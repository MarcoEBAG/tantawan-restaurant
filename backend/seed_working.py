#!/usr/bin/env python3
"""
FUNKTIONIERENDES Seed-Script für Tantawan Restaurant
Fix für SQLAlchemy 2.0+ mit text() Funktion
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .env-Datei laden
ROOT_DIR = Path(__file__).parent
env_file = ROOT_DIR / '.env'

if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ .env-Datei geladen: {env_file}")
else:
    print(f"❌ .env-Datei nicht gefunden: {env_file}")
    sys.exit(1)

# Umgebungsvariablen prüfen
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL nicht gefunden in .env")
    sys.exit(1)

print(f"🔗 DATABASE_URL: {DATABASE_URL}")

# SQLAlchemy Imports - MIT text() für moderne Versionen
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

# Database Setup
try:
    print("🔌 Erstelle Datenbank-Engine...")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✅ Datenbank-Engine erfolgreich erstellt!")
except Exception as e:
    print(f"❌ Engine-Erstellung fehlgeschlagen: {e}")
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

def test_connection():
    """Datenbankverbindung testen - FIX für SQLAlchemy 2.0+"""
    try:
        print("🧪 Teste Datenbankverbindung...")
        db = SessionLocal()
        
        # KORREKTUR: Verwende text() für moderne SQLAlchemy
        result = db.execute(text("SELECT 1 as test")).fetchone()
        db.close()
        
        print(f"✅ Datenbankverbindung erfolgreich! Ergebnis: {result}")
        return True
    except Exception as e:
        print(f"❌ Datenbankverbindungstest fehlgeschlagen: {e}")
        return False

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
        print(f"🍽️ Füge {len(menu_items_data)} Speisekarte-Items ein...")
        
        db = SessionLocal()
        
        # Prüfen ob Tabelle existiert und Daten löschen
        try:
            deleted = db.query(MenuItemDB).delete()
            print(f"🗑️ {deleted} alte Menu-Items gelöscht")
        except Exception as e:
            print(f"ℹ️ Keine alten Menu-Items gefunden (normal beim ersten Mal): {e}")
        
        # Neue Items einfügen
        successful_inserts = 0
        for item_data in menu_items_data:
            try:
                menu_item = MenuItemDB(**item_data)
                db.add(menu_item)
                successful_inserts += 1
                print(f"   ✅ {item_data['name']} - CHF {item_data['price']:.2f}")
            except Exception as e:
                print(f"   ❌ Fehler bei {item_data['name']}: {e}")
        
        # Alle Änderungen speichern
        db.commit()
        db.close()
        
        print(f"\n🎉 {successful_inserts}/{len(menu_items_data)} Items erfolgreich eingefügt!")
        
        # Verifikation
        print("\n🔍 Verifikation - Gespeicherte Items:")
        db_verify = SessionLocal()
        items = db_verify.query(MenuItemDB).all()
        for item in items:
            print(f"   📋 {item.category}: {item.name} - CHF {item.price:.2f}")
        db_verify.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Seeding: {e}")
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass
        return False

# Main Execution
if __name__ == "__main__":
    print("🌱 Tantawan Restaurant - Database Seeding (FIXED)")
    print("=" * 60)
    
    # Schritt 1: Verbindung testen
    if not test_connection():
        print("\n🆘 DATENBANK-VERBINDUNG FEHLGESCHLAGEN!")
        print("\n🔧 Lösungsschritte:")
        print("1. PostgreSQL Status: sudo systemctl status postgresql")
        print("2. Manual DB-Test: psql -U tantawan_user -d tantawan_restaurant")
        print("3. Falls Fehler: Datenbank/Benutzer nochmal erstellen")
        sys.exit(1)
    
    # Schritt 2: Tabellen erstellen
    if not create_tables():
        print("❌ Tabellen-Erstellung fehlgeschlagen!")
        sys.exit(1)
    
    # Schritt 3: Daten einfügen
    if not seed_menu_items():
        print("❌ Speisekarte-Seeding fehlgeschlagen!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎊 SEEDING ERFOLGREICH ABGESCHLOSSEN!")
    print("🚀 Nächste Schritte:")
    print("   1. Backend starten: python3 server_sql.py")
    print("   2. Frontend bauen: cd ../frontend && npm run build")
    print("   3. Website testen: https://ihre-domain.de")
    print("=" * 60)