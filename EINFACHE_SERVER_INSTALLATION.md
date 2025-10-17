# 🚀 TANTAWAN - Einfache Server-Installation

## 🎯 Sie haben WordPress auf Ihrem Server und wollen Tantawan installieren

### ✅ **Was Sie brauchen:**
- Einen Server mit WordPress (✓ haben Sie bereits)
- FTP-Zugang oder Dateimanager im Hosting-Panel
- 15 Minuten Zeit

---

## 📥 **SCHRITT 1: Dateien herunterladen**

### **Option A: Von GitHub herunterladen (Einfach)**

1. **Gehen Sie zu GitHub:**
   - Öffnen Sie: `https://github.com/IhrUsername/tantawan-restaurant`
   - (Falls noch nicht hochgeladen, verwenden Sie Option B)

2. **Dateien herunterladen:**
   - Klicken Sie auf den grünen Button **"< > Code"**
   - Wählen Sie **"Download ZIP"**
   - Speichern Sie `tantawan-restaurant-main.zip`

### **Option B: ZIP-Datei direkt verwenden**

Falls GitHub noch nicht funktioniert, können Sie die ZIP-Datei verwenden, die ich erstellt habe:
- `tantawan-restaurant.zip` (bereits vorhanden)

---

## 📁 **SCHRITT 2: ZIP-Datei entpacken**

1. **Auf Ihrem Computer:**
   - Rechtsklick auf die ZIP-Datei
   - Wählen Sie **"Hier extrahieren"** oder **"Entpacken nach..."**

2. **Sie erhalten einen Ordner mit:**
   ```
   tantawan-restaurant/
   ├── frontend/          ← React Website-Dateien
   ├── backend/           ← Server-Code (Optional)
   ├── README.md          ← Projektbeschreibung
   ├── INSTALLATIONSANLEITUNG.md
   └── ...
   ```

---

## 🌐 **SCHRITT 3: WordPress-Theme erstellen**

### **A) Theme-Ordner erstellen**

1. **Gehen Sie zu Ihrem Server:**
   - Per FTP (FileZilla) oder
   - Dateimanager im Hosting-Panel (cPanel, Plesk, etc.)

2. **Navigieren Sie zu:**
   ```
   /public_html/wp-content/themes/
   ```

3. **Neuen Ordner erstellen:**
   - Name: `tantawan-restaurant`

### **B) Theme-Dateien erstellen**

**Sie müssen 4 wichtige Dateien erstellen:**

#### 📄 **1. style.css**

1. **Neue Datei erstellen:** `style.css`
2. **Folgenden Inhalt einfügen:**

```css
/*
Theme Name: Tantawan Restaurant
Description: Asiatisches Restaurant mit Online-Bestellung
Version: 1.0
Author: Ihr Name
*/

/* === TANTAWAN RESTAURANT STYLES === */

:root {
  --lime-yellow: #ECEC75;
  --lime-dark: #e6e67c;
  --black: #0f172a;
  --white: #ffffff;
  --gray: #64748b;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  line-height: 1.6;
  color: var(--black);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
.site-header {
  background: var(--white);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  padding: 1rem 0;
}

.site-header h1 {
  font-family: 'Crimson Text', serif;
  font-size: 2rem;
  color: var(--black);
}

.site-header nav ul {
  list-style: none;
  display: flex;
  gap: 2rem;
}

.site-header nav a {
  text-decoration: none;
  color: var(--gray);
  font-weight: 500;
  transition: color 0.3s ease;
}

.site-header nav a:hover {
  color: var(--black);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, var(--lime-yellow) 0%, var(--lime-dark) 100%);
  padding: 150px 0 100px;
  text-align: center;
  min-height: 70vh;
  display: flex;
  align-items: center;
}

.hero-content h1 {
  font-family: 'Crimson Text', serif;
  font-size: 4rem;
  font-weight: 700;
  color: var(--black);
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: var(--gray);
  margin-bottom: 1rem;
}

.hero-description {
  font-size: 1.2rem;
  color: var(--gray);
  margin-bottom: 2rem;
}

/* Buttons */
.btn-primary {
  background: var(--black);
  color: var(--white);
  padding: 15px 30px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  margin: 0 10px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  color: var(--white);
}

.btn-secondary {
  background: transparent;
  color: var(--black);
  border: 2px solid var(--black);
  padding: 13px 28px;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  margin: 0 10px;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: var(--black);
  color: var(--white);
}

/* Sections */
.section {
  padding: 80px 0;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-header h2 {
  font-family: 'Crimson Text', serif;
  font-size: 3rem;
  color: var(--black);
  margin-bottom: 1rem;
}

.section-header p {
  font-size: 1.2rem;
  color: var(--gray);
  max-width: 600px;
  margin: 0 auto;
}

/* Menu Styling */
.menu-section {
  background: #f8fafc;
}

.menu-category {
  margin-bottom: 3rem;
}

.menu-category h3 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--black);
  text-align: center;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: var(--white);
  padding: 2rem;
  margin-bottom: 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: transform 0.3s ease;
}

.menu-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.menu-item-info h4 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: var(--black);
}

.menu-item-info p {
  color: var(--gray);
  line-height: 1.6;
}

.menu-item-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--black);
  background: var(--lime-yellow);
  padding: 8px 15px;
  border-radius: 6px;
}

/* Contact Section */
.contact-section {
  background: var(--white);
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  margin-top: 3rem;
}

.contact-item {
  margin-bottom: 2rem;
}

.contact-item h4 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: var(--black);
}

.contact-item p {
  color: var(--gray);
}

.contact-item a {
  color: var(--black);
  text-decoration: none;
}

.contact-item a:hover {
  color: var(--lime-dark);
}

/* Opening Hours */
.hours-list {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid var(--lime-yellow);
}

.hours-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.hours-item:last-child {
  border-bottom: none;
}

/* Footer */
.site-footer {
  background: var(--black);
  color: var(--white);
  padding: 3rem 0 1rem;
  margin-top: 4rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-content h3,
.footer-content h4 {
  color: var(--lime-yellow);
  margin-bottom: 1rem;
}

.footer-content p,
.footer-content a {
  color: #cbd5e1;
  line-height: 1.8;
}

.footer-content a {
  text-decoration: none;
}

.footer-content a:hover {
  color: var(--lime-yellow);
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #374151;
  color: #9ca3af;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .section-header h2 {
    font-size: 2rem;
  }
  
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .menu-item {
    flex-direction: column;
    gap: 1rem;
  }
  
  .menu-item-price {
    align-self: flex-start;
  }
}

/* WordPress-spezifische Klassen */
.aligncenter {
  text-align: center;
}

.alignwide {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.wp-block-group {
  margin-bottom: 2rem;
}

/* Hide admin bar adjustment */
.admin-bar .site-header {
  top: 32px;
}

@media screen and (max-width: 782px) {
  .admin-bar .site-header {
    top: 46px;
  }
}
```

#### 📄 **2. index.php**

```php
<?php get_header(); ?>

<main id="main" class="site-main">
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1>Tantawan</h1>
                <p class="hero-subtitle">Authentische Asiatische Küche</p>
                <p class="hero-description">Frisch gekocht • Extrem fein • Günstige Preise<br>
                <strong>Jetzt online bestellen für Takeaway!</strong></p>
                <div class="hero-buttons">
                    <a href="#menu" class="btn-primary">Jetzt Bestellen</a>
                    <a href="#contact" class="btn-secondary">Kontakt</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Speisekarte Section -->
    <section id="menu" class="menu-section section">
        <div class="container">
            <div class="section-header">
                <h2>Unsere Speisekarte</h2>
                <p>Entdecken Sie unsere Auswahl an frisch zubereiteten asiatischen Gerichten. Alle Preise für Takeaway.</p>
            </div>
            
            <!-- Vorspeisen -->
            <div class="menu-category">
                <h3>🥟 Vorspeisen</h3>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Frühlingsrollen (4 Stück)</h4>
                        <p>Knusprige Frühlingsrollen mit Gemüsefüllung, serviert mit süß-sauer Sauce</p>
                    </div>
                    <div class="menu-item-price">CHF 8.50</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Gyoza (6 Stück)</h4>
                        <p>Japanische Teigtaschen mit Schweinefleisch und Gemüse</p>
                    </div>
                    <div class="menu-item-price">CHF 9.80</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Tom Kha Gai Suppe</h4>
                        <p>Thai Kokosnusssuppe mit Huhn, Galangal und Zitronengras</p>
                    </div>
                    <div class="menu-item-price">CHF 7.90</div>
                </div>
            </div>
            
            <!-- Hauptgerichte -->
            <div class="menu-category">
                <h3>🍜 Hauptgerichte</h3>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Pad Thai mit Huhn</h4>
                        <p>Klassische Thai-Nudeln mit Huhn, Ei, Bohnensprossen und Erdnüssen</p>
                    </div>
                    <div class="menu-item-price">CHF 16.50</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Sweet & Sour Schweinefleisch</h4>
                        <p>Knuspriges Schweinefleisch mit Ananas, Paprika in süß-saurer Sauce</p>
                    </div>
                    <div class="menu-item-price">CHF 17.80</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Beef Teriyaki</h4>
                        <p>Zartes Rindfleisch in Teriyaki-Sauce mit Sesam und Frühlingszwiebeln</p>
                    </div>
                    <div class="menu-item-price">CHF 19.90</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Vegetarisches Curry</h4>
                        <p>Gemischtes Gemüse in cremiger Kokosmilch-Curry-Sauce</p>
                    </div>
                    <div class="menu-item-price">CHF 15.50</div>
                </div>
            </div>
            
            <!-- Desserts -->
            <div class="menu-category">
                <h3>🍨 Desserts</h3>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Mango Sticky Rice</h4>
                        <p>Traditioneller Thai-Dessert mit süßem Klebreis und frischer Mango</p>
                    </div>
                    <div class="menu-item-price">CHF 6.50</div>
                </div>
                
                <div class="menu-item">
                    <div class="menu-item-info">
                        <h4>Sesam-Eiscreme</h4>
                        <p>Hausgemachte Eiscreme mit schwarzem Sesam</p>
                    </div>
                    <div class="menu-item-price">CHF 5.50</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Kontakt Section -->
    <section id="contact" class="contact-section section">
        <div class="container">
            <div class="section-header">
                <h2>Kontakt & Standort</h2>
                <p>Besuchen Sie uns in Frauenfeld oder bestellen Sie telefonisch.</p>
            </div>
            
            <div class="contact-grid">
                <div class="contact-info">
                    <div class="contact-item">
                        <h4>📍 Adresse</h4>
                        <p>Zürcherstrasse 232<br>8500 Frauenfeld, Schweiz</p>
                    </div>
                    
                    <div class="contact-item">
                        <h4>📞 Telefon</h4>
                        <p><a href="tel:+41527212222">+41 52 721 22 22</a></p>
                    </div>
                    
                    <div class="contact-item">
                        <h4>✉️ E-Mail</h4>
                        <p><a href="mailto:info@tantawan.ch">info@tantawan.ch</a></p>
                    </div>
                    
                    <div class="contact-item">
                        <h4>🕐 Öffnungszeiten</h4>
                        <div class="hours-list">
                            <div class="hours-item">
                                <span>Mo - Do</span>
                                <span>11:00 - 14:00, 17:00 - 21:30</span>
                            </div>
                            <div class="hours-item">
                                <span>Freitag</span>
                                <span>11:00 - 14:00, 17:00 - 22:00</span>
                            </div>
                            <div class="hours-item">
                                <span>Samstag</span>
                                <span>11:00 - 22:00</span>
                            </div>
                            <div class="hours-item">
                                <span>Sonntag</span>
                                <span>17:00 - 21:30</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="takeaway-info">
                    <h4>🍜 Takeaway Service</h4>
                    <p>Bestellen Sie telefonisch und holen Sie Ihr frisch zubereitetes Essen ab. Kein Lieferservice - aber immer köstlich!</p>
                    
                    <p><strong>So bestellen Sie:</strong></p>
                    <ol>
                        <li>Rufen Sie uns an: <a href="tel:+41527212222">+41 52 721 22 22</a></li>
                        <li>Wählen Sie Ihre Gerichte aus der Speisekarte</li>
                        <li>Vereinbaren Sie eine Abholzeit (15-30 Min)</li>
                        <li>Holen Sie Ihr Essen frisch zubereitet ab</li>
                    </ol>
                    
                    <p><strong>Zubereitungszeit:</strong> 15-30 Minuten je nach Bestellmenge</p>
                    
                    <div style="margin-top: 2rem;">
                        <a href="tel:+41527212222" class="btn-primary">📞 Jetzt anrufen & bestellen</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

</main>

<?php get_footer(); ?>
```

#### 📄 **3. header.php**

```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php wp_title('|', true, 'right'); ?><?php bloginfo('name'); ?></title>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap" rel="stylesheet">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
    <header class="site-header">
        <div class="container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="site-logo">
                    <a href="<?php echo home_url(); ?>" style="text-decoration: none;">
                        <h1 style="margin: 0; color: #0f172a;">Tantawan</h1>
                    </a>
                </div>
                
                <nav class="main-navigation">
                    <ul style="display: flex; list-style: none; margin: 0; padding: 0; gap: 2rem;">
                        <li><a href="<?php echo home_url(); ?>">Home</a></li>
                        <li><a href="#menu">Speisekarte</a></li>
                        <li><a href="#contact">Kontakt</a></li>
                    </ul>
                </nav>
                
                <div class="header-actions">
                    <a href="tel:+41527212222" class="btn-primary" style="font-size: 0.9rem; padding: 10px 20px;">📞 Bestellen</a>
                </div>
            </div>
        </div>
    </header>
    
    <div style="height: 80px;"></div> <!-- Spacer für fixed header -->
```

#### 📄 **4. footer.php**

```php
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <h3>Tantawan</h3>
                    <p>Authentische asiatische Küche in Frauenfeld. Frisch gekocht, günstig und extrem fein - perfekt für Takeaway.</p>
                    <p><strong>📍 Zürcherstrasse 232, 8500 Frauenfeld</strong></p>
                </div>
                
                <div class="footer-contact">
                    <h4>Kontakt</h4>
                    <p>📞 <a href="tel:+41527212222">+41 52 721 22 22</a></p>
                    <p>✉️ <a href="mailto:info@tantawan.ch">info@tantawan.ch</a></p>
                    <p>🌐 <a href="<?php echo home_url(); ?>">www.tantawan.ch</a></p>
                </div>
                
                <div class="footer-hours">
                    <h4>Öffnungszeiten</h4>
                    <p>Mo-Do: 11:00-14:00, 17:00-21:30</p>
                    <p>Fr: 11:00-14:00, 17:00-22:00</p>
                    <p>Sa: 11:00-22:00</p>
                    <p>So: 17:00-21:30</p>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; <?php echo date('Y'); ?> Tantawan Restaurant. Alle Rechte vorbehalten.</p>
                <p>Ein Restaurant für authentische asiatische Küche in Frauenfeld</p>
            </div>
        </div>
    </footer>

    <?php wp_footer(); ?>
</body>
</html>
```

---

## 📤 **SCHRITT 4: Dateien auf Server hochladen**

### **Mit FTP (FileZilla):**

1. **Verbindung zum Server:**
   - Server: Ihre Domain oder IP
   - Benutzername: FTP-Benutzer
   - Passwort: FTP-Passwort

2. **Dateien hochladen:**
   - Lokaler Pfad: Ihr `tantawan-theme` Ordner
   - Server-Pfad: `/public_html/wp-content/themes/tantawan-restaurant/`
   - Alle 4 Dateien hochladen

### **Mit Hosting-Panel (cPanel/Plesk):**

1. **Dateimanager öffnen**
2. **Navigieren zu:** `public_html/wp-content/themes/`
3. **Ordner erstellen:** `tantawan-restaurant`
4. **Dateien hochladen:** Alle 4 PHP/CSS-Dateien

---

## 🎨 **SCHRITT 5: Theme in WordPress aktivieren**

1. **WordPress Admin öffnen:**
   - `https://ihre-domain.de/wp-admin`

2. **Zum Theme-Bereich:**
   - **Design** → **Themes**

3. **Tantawan Theme finden:**
   - Sie sehen "Tantawan Restaurant"
   - Klicken Sie **"Aktivieren"**

4. **Website anschauen:**
   - Besuchen Sie Ihre Website
   - Sie sehen das lime-gelbe Tantawan Design! 🎉

---

## ✅ **FERTIG! Ihre Website läuft jetzt**

### **Was Sie jetzt haben:**
- ✅ Professionelle Restaurant-Website
- ✅ Lime-gelbes Tantawan Design
- ✅ Vollständige Speisekarte
- ✅ Kontakt & Öffnungszeiten
- ✅ Telefonische Bestellfunktion
- ✅ Responsive für Handy & Desktop

### **Wichtige Links:**
- **Ihre Website:** `https://ihre-domain.de`
- **WordPress Admin:** `https://ihre-domain.de/wp-admin`

---

## 🔧 **Anpassungen vornehmen**

### **Inhalte ändern:**
1. **WordPress Admin** → **Design** → **Theme-Editor**
2. **Datei auswählen:** `index.php`
3. **Text bearbeiten:** Restaurant-Name, Adresse, Telefon
4. **Speichern**

### **Speisekarte anpassen:**
- Öffnen Sie `index.php` im Theme-Editor
- Suchen Sie die Menu-Items
- Ändern Sie Gerichte-Namen und Preise
- Speichern

### **Farben ändern:**
- Öffnen Sie `style.css`
- Suchen Sie `:root {`
- Ändern Sie die Farb-Codes
- Speichern

---

## 📞 **Hilfe benötigt?**

**Häufige Probleme:**

1. **Theme erscheint nicht:**
   - Prüfen Sie Ordner-Name: `tantawan-restaurant`
   - Prüfen Sie ob alle 4 Dateien hochgeladen sind

2. **Design sieht falsch aus:**
   - Leeren Sie Browser-Cache (Strg+F5)
   - Prüfen Sie `style.css` Datei

3. **FTP funktioniert nicht:**
   - Verwenden Sie Hosting-Panel Dateimanager
   - Kontaktieren Sie Ihren Hoster

**Bei Fragen:** Überprüfen Sie alle Schritte nochmal oder fragen Sie Ihren Hoster um Hilfe.

---

**🎉 Herzlichen Glückwunsch! Ihre Tantawan Restaurant Website ist jetzt live!**