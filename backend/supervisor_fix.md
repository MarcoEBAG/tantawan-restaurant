# 🔧 Supervisor-Problem lösen - Tantawan Backend

## ❌ **Fehler:** `supervisor: ERROR (spawn error)`

## 🔍 **SCHRITT 1: Logs überprüfen**

```bash
# Supervisor-Logs anschauen
sudo tail -n 20 /var/log/supervisor/supervisord.log

# Spezifische Backend-Logs
sudo tail -n 20 /var/log/tantawan-backend.log
```

---

## 🔧 **SCHRITT 2: Supervisor-Konfiguration reparieren**

### **Alte Konfiguration löschen:**
```bash
sudo rm -f /etc/supervisor/conf.d/tantawan-backend.conf
```

### **Neue, funktionierende Konfiguration erstellen:**

```bash
sudo nano /etc/supervisor/conf.d/tantawan.conf
```

**📝 Kopieren Sie EXAKT folgenden Inhalt:**

```ini
[program:tantawan-backend]
command=/var/www/tantawan/backend/venv/bin/python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001
directory=/var/www/tantawan/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/tantawan.log
stderr_logfile=/var/log/tantawan.log
environment=PATH="/var/www/tantawan/backend/venv/bin"
startsecs=10
startretries=3
```

---

## 🔧 **SCHRITT 3: Berechtigungen und Pfade überprüfen**

```bash
# 1. Ordner-Berechtigungen setzen
sudo chown -R www-data:www-data /var/www/tantawan
sudo chmod -R 755 /var/www/tantawan

# 2. Prüfen ob alle Dateien existieren
ls -la /var/www/tantawan/backend/
ls -la /var/www/tantawan/backend/venv/bin/python
ls -la /var/www/tantawan/backend/server_sql.py

# 3. Virtual Environment prüfen
/var/www/tantawan/backend/venv/bin/python --version
```

---

## 🚀 **SCHRITT 4: Backend manuell testen**

**Bevor wir Supervisor verwenden, testen wir das Backend manuell:**

```bash
# 1. In Backend-Ordner
cd /var/www/tantawan/backend

# 2. Virtual Environment aktivieren
source venv/bin/activate

# 3. Manuell starten (zum Testen)
python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001

# 4. In anderem Terminal testen:
# curl http://localhost:8001/api/health
```

**✅ Falls das funktioniert:** Backend läuft korrekt, Supervisor-Problem
**❌ Falls Fehler:** Backend hat Probleme, zuerst das reparieren

---

## 🔧 **SCHRITT 5: Supervisor neu starten**

```bash
# 1. Supervisor-Konfiguration neu laden
sudo supervisorctl reread
sudo supervisorctl update

# 2. Service starten
sudo supervisorctl start tantawan-backend

# 3. Status prüfen
sudo supervisorctl status

# 4. Logs in Echtzeit verfolgen
sudo tail -f /var/log/tantawan.log
```

---

## 🆘 **ALTERNATIVE: Systemd verwenden (falls Supervisor Probleme macht)**

### **Systemd-Service erstellen:**

```bash
sudo nano /etc/systemd/system/tantawan.service
```

**📝 Service-Datei:**

```ini
[Unit]
Description=Tantawan Restaurant Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/tantawan/backend
Environment=PATH=/var/www/tantawan/backend/venv/bin
EnvironmentFile=/var/www/tantawan/backend/.env
ExecStart=/var/www/tantawan/backend/venv/bin/python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

# Logs
StandardOutput=append:/var/log/tantawan.log
StandardError=append:/var/log/tantawan.log

[Install]
WantedBy=multi-user.target
```

### **Systemd-Service verwenden:**

```bash
# 1. Service aktivieren und starten
sudo systemctl daemon-reload
sudo systemctl enable tantawan
sudo systemctl start tantawan

# 2. Status prüfen
sudo systemctl status tantawan

# 3. Logs verfolgen
sudo journalctl -u tantawan -f
```

---

## 🔍 **SCHRITT 6: Häufige Probleme & Lösungen**

### **Problem 1: Python-Pfad falsch**
```bash
# Korrekten Python-Pfad finden
which python
/var/www/tantawan/backend/venv/bin/python --version
```

### **Problem 2: server_sql.py nicht gefunden**
```bash
# Prüfen ob Datei existiert
ls -la /var/www/tantawan/backend/server_sql.py

# Falls nicht vorhanden, erstellen Sie sie aus der Anleitung
```

### **Problem 3: Dependencies fehlen**
```bash
cd /var/www/tantawan/backend
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### **Problem 4: Port bereits in Verwendung**
```bash
# Prüfen was Port 8001 verwendet
sudo lsof -i :8001

# Falls belegt, anderen Port verwenden (z.B. 8002)
```

---

## ✅ **ERFOLG-Test:**

**Nach der Reparatur sollten Sie sehen:**

```bash
sudo supervisorctl status
# tantawan-backend    RUNNING   pid 12345, uptime 0:00:05

curl http://localhost:8001/api/health
# {"status":"healthy","service":"Tantawan Restaurant API SQL"}
```

---

## 🎯 **Schnelle Notlösung (falls alles fehlschlägt):**

**Führen Sie das Backend im Hintergrund aus:**

```bash
cd /var/www/tantawan/backend
source venv/bin/activate
nohup python -m uvicorn server_sql:app --host 0.0.0.0 --port 8001 > /var/log/tantawan.log 2>&1 &

# Status prüfen
jobs
curl http://localhost:8001/api/health
```

---

**💡 Folgen Sie diesen Schritten der Reihe nach - eines davon wird das Problem lösen!** 

Lassen Sie mich wissen, was die Logs zeigen oder bei welchem Schritt Sie Hilfe brauchen! 🤝