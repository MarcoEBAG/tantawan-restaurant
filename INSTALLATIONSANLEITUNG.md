# 🍜 Tantawan Restaurant - Vollständige Installationsanleitung

## 📋 Inhaltsverzeichnis
1. [WordPress Installation](#wordpress-installation)
2. [Raspberry Pi Installation](#raspberry-pi-installation)
3. [E-Mail & Drucker Konfiguration](#e-mail--drucker-konfiguration)
4. [Problembehandlung](#problembehandlung)

---

## 🌐 WordPress Installation

### ⚠️ Wichtiger Hinweis
Das Tantawan Restaurant System ist eine moderne React/FastAPI-Anwendung. Für WordPress gibt es zwei Optionen:

#### Option A: Statisches WordPress Theme (Empfohlen für einfache Websites)
#### Option B: WordPress mit separatem Backend (Für vollständige Funktionalität)

---

### 📦 Option A: Statisches WordPress Theme

#### Schritt 1: Dateien vorbereiten
```bash
# 1. React Build erstellen
cd /app/frontend
npm run build

# 2. WordPress Theme-Ordner erstellen
mkdir tantawan-theme
cd tantawan-theme
```

#### Schritt 2: WordPress Theme-Struktur erstellen
```
tantawan-theme/
├── style.css
├── index.php
├── functions.php
├── header.php
├── footer.php
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── menu.php
    ├── contact.php
    └── admin.php
```

#### Schritt 3: Theme-Dateien erstellen

**style.css:**
```css
/*
Theme Name: Tantawan Restaurant
Description: Asiatisches Restaurant Theme mit Online-Bestellung
Version: 1.0
Author: Ihr Name
*/

/* Hier den CSS-Inhalt aus /app/frontend/src/App.css einfügen */
```

**functions.php:**
```php
<?php
function tantawan_enqueue_scripts() {
    wp_enqueue_style('tantawan-style', get_stylesheet_uri());
    wp_enqueue_script('tantawan-main', get_template_directory_uri() . '/assets/js/main.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'tantawan_enqueue_scripts');

// Menu Support
function tantawan_setup() {
    add_theme_support('menus');
    register_nav_menus(array(
        'primary' => 'Primary Menu'
    ));
}
add_action('after_setup_theme', 'tantawan_setup');
?>
```

**index.php:**
```php
<?php get_header(); ?>

<!-- Hier den HTML-Inhalt aus der React-Build einfügen -->
<div id="tantawan-root">
    <!-- Hero Section -->
    <section class="hero-section" style="background: linear-gradient(to bottom right, #ECEC75, #e6e67c);">
        <div class="container">
            <h1>Tantawan</h1>
            <p>Authentische Asiatische Küche</p>
            <p>Frisch gekocht • Extrem fein • Günstige Preise</p>
        </div>
    </section>
    
    <!-- Menu Section -->
    <section class="menu-section">
        <?php include 'templates/menu.php'; ?>
    </section>
    
    <!-- Contact Section -->
    <section class="contact-section">
        <?php include 'templates/contact.php'; ?>
    </section>
</div>

<?php get_footer(); ?>
```

#### Schritt 4: WordPress Installation
```bash
# 1. Theme in WordPress hochladen
# - WordPress Admin → Design → Themes → Theme hinzufügen → ZIP hochladen

# 2. Theme aktivieren
# - Hochgeladenes Theme auswählen und aktivieren

# 3. Menu konfigurieren
# - WordPress Admin → Design → Menüs → Neues Menü erstellen
```

---

### 🔧 Option B: WordPress + Separates Backend (Vollständige Funktionalität)

#### Voraussetzungen
- WordPress Website (läuft bereits)
- Separater Server/VPS für Backend
- Domain oder Subdomain für Backend (z.B. api.ihr-restaurant.de)

#### Schritt 1: Backend auf separatem Server installieren
```bash
# 1. Server vorbereiten (Ubuntu/Debian)
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip mongodb nodejs npm nginx -y

# 2. Projekt klonen/hochladen
mkdir /var/www/tantawan-backend
cd /var/www/tantawan-backend

# Backend-Dateien hochladen (server.py, models.py, etc.)
```

#### Schritt 2: Backend konfigurieren
```bash
# 1. Python-Umgebung einrichten
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Umgebungsvariablen einrichten
nano .env
```

**.env Datei:**
```bash
MONGO_URL=mongodb://localhost:27017
DB_NAME=tantawan_restaurant
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ihr-email@gmail.com
SMTP_PASSWORD=ihr-passwort
RESTAURANT_EMAIL=restaurant@tantawan.ch
PRINTER_EMAIL=drucker@tantawan.ch
```

#### Schritt 3: Nginx konfigurieren
```bash
sudo nano /etc/nginx/sites-available/tantawan-api
```

**Nginx Konfiguration:**
```nginx
server {
    listen 80;
    server_name api.ihr-restaurant.de;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Nginx konfigurieren
sudo ln -s /etc/nginx/sites-available/tantawan-api /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### Schritt 4: Backend als Service einrichten
```bash
sudo nano /etc/systemd/system/tantawan.service
```

**Service Datei:**
```ini
[Unit]
Description=Tantawan Restaurant API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tantawan-backend
Environment=PATH=/var/www/tantawan-backend/venv/bin
ExecStart=/var/www/tantawan-backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service starten
sudo systemctl daemon-reload
sudo systemctl enable tantawan
sudo systemctl start tantawan
```

#### Schritt 5: WordPress-Plugin erstellen

**tantawan-plugin.php:**
```php
<?php
/*
Plugin Name: Tantawan Restaurant Bestellsystem
Description: Integration für das Tantawan Restaurant Bestellsystem
Version: 1.0
*/

// Shortcode für Bestellformular
function tantawan_order_form() {
    ob_start();
    ?>
    <div id="tantawan-order-app"></div>
    <script>
        // JavaScript für API-Integration
        const API_BASE = 'https://api.ihr-restaurant.de/api';
        
        // Bestellformular laden
        fetch(`${API_BASE}/menu/`)
            .then(response => response.json())
            .then(data => {
                // Menu-Daten verarbeiten und anzeigen
                renderMenu(data);
            });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode('tantawan_order', 'tantawan_order_form');
?>
```

---

## 🥧 Raspberry Pi Installation

### 📋 Hardware-Anforderungen
- Raspberry Pi 4 (4GB RAM empfohlen)
- MicroSD-Karte (32GB+)
- Ethernet/WiFi-Verbindung
- Optional: Drucker für Bestellungen

### Schritt 1: Raspberry Pi OS Installation

```bash
# 1. Raspberry Pi Imager herunterladen
# https://www.raspberrypi.org/software/

# 2. Raspberry Pi OS Lite (64-bit) auf SD-Karte flashen

# 3. SSH aktivieren (leere Datei 'ssh' auf Boot-Partition erstellen)

# 4. WiFi konfigurieren (wpa_supplicant.conf auf Boot-Partition)
```

**wpa_supplicant.conf:**
```
country=CH
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="IhrWiFiName"
    psk="IhrWiFiPasswort"
}
```

### Schritt 2: System vorbereiten

```bash
# 1. SSH-Verbindung zum Pi
ssh pi@raspberry-pi-ip

# 2. System aktualisieren
sudo apt update && sudo apt upgrade -y

# 3. Benötigte Pakete installieren
sudo apt install -y python3 python3-pip python3-venv nodejs npm mongodb git nginx supervisor
```

### Schritt 3: MongoDB einrichten

```bash
# 1. MongoDB starten und aktivieren
sudo systemctl enable mongodb
sudo systemctl start mongodb

# 2. Datenbank erstellen
mongo
> use tantawan_restaurant
> db.createCollection("menu_items")
> db.createCollection("orders")
> db.createCollection("newsletter_subscriptions")
> exit
```

### Schritt 4: Tantawan-Anwendung installieren

```bash
# 1. Projektordner erstellen
sudo mkdir /var/www/tantawan
sudo chown pi:pi /var/www/tantawan
cd /var/www/tantawan

# 2. Dateien hochladen (per SCP oder Git)
# Alle Backend-Dateien von /app/backend/* hierher kopieren
# Alle Frontend-Dateien von /app/frontend/* nach frontend/ kopieren
```

### Schritt 5: Backend konfigurieren

```bash
# 1. Python-Umgebung einrichten
cd /var/www/tantawan
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Umgebungsvariablen konfigurieren
nano .env
```

**.env für Raspberry Pi:**
```bash
MONGO_URL=mongodb://localhost:27017
DB_NAME=tantawan_restaurant
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=restaurant@gmail.com
SMTP_PASSWORD=ihr-app-passwort
RESTAURANT_EMAIL=tantawan@ihr-domain.ch
PRINTER_EMAIL=drucker@ihr-domain.ch
```

### Schritt 6: Frontend vorbereiten

```bash
# 1. Node.js-Abhängigkeiten installieren
cd /var/www/tantawan/frontend
npm install

# 2. Frontend-Build erstellen
npm run build

# 3. Build-Dateien für Nginx vorbereiten
sudo cp -r build/* /var/www/html/
```

### Schritt 7: Nginx konfigurieren

```bash
sudo nano /etc/nginx/sites-available/tantawan
```

**Nginx Konfiguration:**
```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/html;
    index index.html;

    # Frontend (React)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin Dashboard
    location /admin {
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Nginx aktivieren
sudo ln -s /etc/nginx/sites-available/tantawan /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

### Schritt 8: Supervisor für Prozessmanagement

```bash
sudo nano /etc/supervisor/conf.d/tantawan-backend.conf
```

**Supervisor Konfiguration:**
```ini
[program:tantawan-backend]
command=/var/www/tantawan/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
directory=/var/www/tantawan
user=pi
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/tantawan-backend.log
```

```bash
# Supervisor neu laden
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tantawan-backend
```

### Schritt 9: Datenbank mit Menü-Daten füllen

```bash
cd /var/www/tantawan
source venv/bin/activate
python seed_data.py
```

### Schritt 10: Firewall konfigurieren (Optional)

```bash
# UFW installieren und konfigurieren
sudo apt install ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

---

## 📧 E-Mail & Drucker Konfiguration

### E-Mail-Konfiguration

#### Gmail verwenden:
1. **App-Passwort erstellen:**
   - Google-Konto → Sicherheit → 2-Faktor-Authentifizierung → App-Passwörter
   - Neues App-Passwort für "Tantawan Restaurant" erstellen

2. **.env-Datei aktualisieren:**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ihr-restaurant@gmail.com
SMTP_PASSWORD=generiertes-app-passwort
RESTAURANT_EMAIL=ihr-restaurant@gmail.com
```

#### Andere E-Mail-Anbieter:
```bash
# Outlook/Hotmail
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587

# Eigener SMTP-Server
SMTP_SERVER=mail.ihre-domain.ch
SMTP_PORT=587
```

### Drucker-Integration

#### Option 1: E-Mail-to-Print Service
```bash
# PrinterShare oder ähnlichen Service verwenden
PRINTER_EMAIL=unique-printer-id@printershare.com
```

#### Option 2: Direkter Netzwerkdrucker
```bash
# Zusätzliches Python-Paket installieren
pip install python-escpos

# In email_service.py erweitern:
from escpos.printer import Network

def print_order_directly(order):
    # Direkter Druck über Netzwerk
    printer = Network("192.168.1.100")  # Drucker-IP
    printer.text(format_order_for_print(order))
    printer.cut()
```

#### Option 3: USB-Drucker am Raspberry Pi
```bash
# CUPS installieren
sudo apt-get install cups cups-client

# Drucker einrichten
sudo lpadmin -p ThermalPrinter -E -v usb://Brother/QL-570 -m brother-ql-570.ppd

# Python-Druckfunktion
import subprocess

def print_to_usb(order_text):
    with open('/tmp/order.txt', 'w') as f:
        f.write(order_text)
    subprocess.run(['lp', '/tmp/order.txt'])
```

---

## 🔧 Problembehandlung

### Häufige Probleme und Lösungen

#### Problem: "Connection refused" beim Backend
```bash
# 1. Service-Status prüfen
sudo systemctl status tantawan
# oder
sudo supervisorctl status tantawan-backend

# 2. Logs prüfen
sudo journalctl -u tantawan -f
# oder
sudo tail -f /var/log/tantawan-backend.log

# 3. Port prüfen
sudo netstat -tlnp | grep 8001
```

#### Problem: MongoDB-Verbindungsfehler
```bash
# 1. MongoDB-Status prüfen
sudo systemctl status mongodb

# 2. MongoDB neu starten
sudo systemctl restart mongodb

# 3. Logs prüfen
sudo tail -f /var/log/mongodb/mongodb.log
```

#### Problem: E-Mails werden nicht gesendet
```bash
# 1. SMTP-Einstellungen prüfen
# 2. App-Passwort bei Gmail verwenden
# 3. Firewall-Einstellungen für Port 587 prüfen
sudo ufw status
```

#### Problem: Frontend lädt nicht
```bash
# 1. Nginx-Status prüfen
sudo systemctl status nginx

# 2. Nginx-Logs prüfen
sudo tail -f /var/log/nginx/error.log

# 3. Frontend-Build neu erstellen
cd /var/www/tantawan/frontend
npm run build
sudo cp -r build/* /var/www/html/
```

### Nützliche Befehle

```bash
# Alle Services neu starten
sudo systemctl restart nginx mongodb
sudo supervisorctl restart tantawan-backend

# Logs in Echtzeit verfolgen
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/tantawan-backend.log

# Datenbank-Backup erstellen
mongodump --db tantawan_restaurant --out /backup/$(date +%Y%m%d)

# System-Ressourcen prüfen (Raspberry Pi)
htop
df -h
free -h
```

### Performance-Optimierung (Raspberry Pi)

```bash
# 1. Swap-Datei vergrößern
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# 2. GPU-Memory reduzieren
sudo nano /boot/config.txt
# gpu_mem=16

# 3. Unnötige Services deaktivieren
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

---

## 🎯 URLs nach der Installation

- **Restaurant-Website:** `http://raspberry-pi-ip/`
- **Admin-Dashboard:** `http://raspberry-pi-ip/admin`
- **API-Dokumentation:** `http://raspberry-pi-ip/api/docs`
- **Gesundheitscheck:** `http://raspberry-pi-ip/api/health`

---

## 📞 Support und Wartung

### Regelmäßige Wartung
```bash
# Wöchentlich ausführen
sudo apt update && sudo apt upgrade -y
mongodump --db tantawan_restaurant --out /backup/weekly

# Monatlich
sudo journalctl --vacuum-time=30d
sudo apt autoremove -y
```

### Monitoring
```bash
# System-Monitor installieren
sudo apt install htop iotop

# Log-Rotation konfigurieren
sudo nano /etc/logrotate.d/tantawan
```

**Logrotate-Konfiguration:**
```
/var/log/tantawan-backend.log {
    daily
    rotate 7
    compress
    delaycompress
    create 644 pi pi
}
```

---

**🎉 Ihre Tantawan Restaurant-Website ist jetzt einsatzbereit!**

Bei Fragen oder Problemen können Sie die Logs überprüfen oder die Konfigurationsdateien anpassen. Das System ist so konzipiert, dass es stabil und wartungsarm läuft.