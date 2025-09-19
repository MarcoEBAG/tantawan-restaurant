# 🍜 Tantawan Restaurant - Vollständiges Management System

Ein modernes, vollständiges Restaurant-Management-System mit Online-Bestellungen, automatischen Benachrichtigungen und Admin-Dashboard.

![Tantawan Restaurant](https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=400&fit=crop&crop=center)

## ✨ Features

### 🌐 Restaurant Website
- **Moderne React-Frontend** mit lime-gelbem Design
- **Online-Bestellsystem** mit Warenkorb und Abholzeit-Auswahl
- **Newsletter-Anmeldung** mit E-Mail-Validierung
- **Responsive Design** für alle Geräte
- **Mehrsprachig** (Deutsch) mit lokalen Schweizer Formaten

### 🍳 Küchen-Management
- **Admin Dashboard** unter `/admin` Route
- **Echtzeit-Bestellübersicht** als ToDo-Liste
- **Status-Management**: Pending → Confirmed → Preparing → Ready → Completed
- **Automatische Updates** alle 30 Sekunden
- **Statistiken** mit Umsatz und Bestellanzahl

### 📧 Automatische Benachrichtigungen
- **E-Mail-Benachrichtigungen** bei neuen Bestellungen
- **Automatischer Druck** für Küchenzettel
- **HTML & Text-Format** für professionelle E-Mails
- **Background Tasks** für optimale Performance

### 🚀 Technische Highlights
- **Backend**: FastAPI mit MongoDB
- **Frontend**: React mit modernen Hooks
- **Database**: Automatische Indizierung und Optimierung
- **API**: RESTful mit automatischer Dokumentation
- **Security**: Input-Validierung und Error-Handling

## 📖 Vollständige Installationsanleitung

**👉 [Komplette Installationsanleitung](INSTALLATIONSANLEITUNG.md)**

Die Anleitung enthält:
- ✅ **WordPress-Integration** (2 Optionen)
- ✅ **Raspberry Pi Setup** (Schritt-für-Schritt)
- ✅ **E-Mail & Drucker-Konfiguration**
- ✅ **Problembehandlung und Support**

## 📋 Installationsoptionen

| Option | Beschreibung | Komplexität | Funktionalität |
|--------|-------------|-------------|----------------|
| **WordPress** | Statisches Theme oder Plugin | 🟢 Einfach | ⭐⭐⭐ Basis |
| **Raspberry Pi** | Vollständige Installation | 🟡 Mittel | ⭐⭐⭐⭐⭐ Komplett |
| **Cloud/VPS** | Production-Ready Setup | 🟡 Mittel | ⭐⭐⭐⭐⭐ Komplett |

## 🚀 Schnellstart

### Voraussetzungen
- Node.js 16+ und Python 3.8+
- MongoDB
- SMTP-Zugang für E-Mails

### Lokale Entwicklung
```bash
# Repository klonen
git clone https://github.com/IhrUsername/tantawan-restaurant.git
cd tantawan-restaurant

# Backend starten
cd backend
pip install -r requirements.txt
python seed_data.py
uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend starten (neues Terminal)
cd frontend
npm install
npm start
```

## 📁 Projektstruktur

```
tantawan-restaurant/
├── 📖 INSTALLATIONSANLEITUNG.md  # Vollständige Anleitung
├── 📄 README.md                  # Diese Datei
├── 📄 contracts.md               # API-Verträge
├── 🖥️ backend/                   # FastAPI Backend
│   ├── server.py                 # Hauptserver
│   ├── models.py                 # Datenmodelle
│   ├── database.py               # DB-Verbindung
│   ├── routes/                   # API-Routen
│   ├── services/                 # E-Mail & Services
│   └── requirements.txt          # Python-Abhängigkeiten
├── 🌐 frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/           # React-Komponenten
│   │   ├── services/             # API-Services
│   │   └── data/                 # Mock-Daten
│   └── package.json              # Node-Abhängigkeiten
└── 🧪 tests/                     # Tests
```

## 🔧 Konfiguration

### Umgebungsvariablen (.env)
```bash
# Datenbank
MONGO_URL=mongodb://localhost:27017
DB_NAME=tantawan_restaurant

# E-Mail (Gmail-Beispiel)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=restaurant@gmail.com
SMTP_PASSWORD=ihr-app-passwort
RESTAURANT_EMAIL=info@tantawan.ch

# Drucker (Optional)
PRINTER_EMAIL=drucker@printershare.com
```

## 📞 Support

### Häufige Probleme
- **Backend startet nicht**: `sudo systemctl status tantawan`
- **E-Mails nicht gesendet**: App-Passwort bei Gmail verwenden
- **Database-Fehler**: `sudo systemctl restart mongodb`

---

**Made with ❤️ für Tantawan Restaurant**

*Ein modernes, vollständiges Restaurant-Management-System - von der Bestellung bis zur Küche.*
