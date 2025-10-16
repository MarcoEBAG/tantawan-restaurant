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

#### Schritt 3: Theme-Dateien erstellen (Ausführliche Anleitung)

### 📝 **1. style.css erstellen und speichern**

**Schritt-für-Schritt:**

1. **Texteditor öffnen** (Notepad++, VSCode, oder einfachen Texteditor)
2. **Neues Dokument erstellen**
3. **Folgenden Code einfügen:**

```css
/*
Theme Name: Tantawan Restaurant
Description: Asiatisches Restaurant Theme mit Online-Bestellung
Version: 1.0
Author: Ihr Name
Text Domain: tantawan
*/

/* === TANTAWAN RESTAURANT STYLES === */

/* CSS-Variablen für Farben */
:root {
  --color-primary: #ECEC75; /* Lime-Gelb */
  --color-primary-dark: #e6e67c;
  --color-black: #0f172a;
  --color-white: #ffffff;
  --color-gray-50: #f8fafc;
  --color-gray-600: #64748b;
}

/* Basis-Styling */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  line-height: 1.6;
  color: var(--color-black);
  margin: 0;
  padding: 0;
}

/* Header Styling */
.site-header {
  background: var(--color-white);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 120px 20px 80px;
  text-align: center;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content h1 {
  font-family: 'Crimson Text', serif;
  font-size: 4rem;
  font-weight: 700;
  color: var(--color-black);
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.5rem;
  color: var(--color-gray-600);
  margin-bottom: 2rem;
}

/* Button Styling */
.btn-primary {
  background: var(--color-black);
  color: var(--color-white);
  padding: 15px 30px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Menu Section */
.menu-section {
  padding: 80px 20px;
  background: var(--color-gray-50);
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.menu-item {
  background: var(--color-white);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.menu-item:hover {
  transform: translateY(-5px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .hero-content p {
    font-size: 1.2rem;
  }
  
  .menu-grid {
    grid-template-columns: 1fr;
  }
}

/* Container für Inhalt */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* WordPress-spezifische Klassen */
.wp-block-group {
  margin-bottom: 2rem;
}

.aligncenter {
  text-align: center;
}

.alignwide {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}
```

4. **Datei speichern:**
   - **Datei** → **Speichern unter...**
   - **Dateiname:** `style.css`
   - **Dateityp:** "Alle Dateien" oder "CSS"
   - **Speicherort:** Ihr Theme-Ordner `tantawan-theme/`

### 📝 **2. functions.php erstellen und speichern**

1. **Neues Dokument im Texteditor**
2. **Folgenden PHP-Code einfügen:**

```php
<?php
/**
 * Tantawan Restaurant WordPress Theme Functions
 */

// Sicherheit: Direkten Zugriff verhindern
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Theme Setup
 */
function tantawan_setup() {
    // Theme-Unterstützung hinzufügen
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
    
    // Menu-Unterstützung
    register_nav_menus(array(
        'primary' => 'Hauptmenü',
        'footer'  => 'Footer-Menü',
    ));
}
add_action('after_setup_theme', 'tantawan_setup');

/**
 * Scripts und Styles einbinden
 */
function tantawan_enqueue_scripts() {
    // Theme-Stylesheet
    wp_enqueue_style(
        'tantawan-style',
        get_stylesheet_uri(),
        array(),
        '1.0.0'
    );
    
    // Google Fonts
    wp_enqueue_style(
        'tantawan-fonts',
        'https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap',
        array(),
        null
    );
    
    // JavaScript (falls benötigt)
    wp_enqueue_script(
        'tantawan-main',
        get_template_directory_uri() . '/assets/js/main.js',
        array('jquery'),
        '1.0.0',
        true
    );
    
    // AJAX-URL für JavaScript verfügbar machen
    wp_localize_script('tantawan-main', 'tantawan_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce'    => wp_create_nonce('tantawan_nonce'),
    ));
}
add_action('wp_enqueue_scripts', 'tantawan_enqueue_scripts');

/**
 * Widget-Bereiche registrieren
 */
function tantawan_widgets_init() {
    register_sidebar(array(
        'name'          => 'Footer Widget Bereich',
        'id'            => 'footer-widgets',
        'description'   => 'Widgets für den Footer-Bereich',
        'before_widget' => '<div class="footer-widget">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}
add_action('widgets_init', 'tantawan_widgets_init');

/**
 * Bestellformular Shortcode
 */
function tantawan_order_form_shortcode($atts) {
    ob_start();
    ?>
    <div id="tantawan-order-form" class="order-form-container">
        <div class="order-form-header">
            <h2>Online Bestellen</h2>
            <p>Wählen Sie Ihre Gerichte und holen Sie sie ab!</p>
        </div>
        
        <div class="menu-categories">
            <button class="category-btn active" data-category="vorspeisen">Vorspeisen</button>
            <button class="category-btn" data-category="hauptgerichte">Hauptgerichte</button>
            <button class="category-btn" data-category="desserts">Desserts</button>
        </div>
        
        <div id="menu-items" class="menu-items-grid">
            <!-- Menu-Items werden hier dynamisch geladen -->
        </div>
        
        <div id="cart-summary" class="cart-summary">
            <h3>Warenkorb</h3>
            <div id="cart-items"></div>
            <div class="cart-total">
                <strong>Gesamt: CHF <span id="total-price">0.00</span></strong>
            </div>
        </div>
        
        <div class="order-form">
            <h3>Bestellinformationen</h3>
            <form id="tantawan-order" method="post">
                <div class="form-group">
                    <label for="customer-name">Name *</label>
                    <input type="text" id="customer-name" name="customer_name" required>
                </div>
                
                <div class="form-group">
                    <label for="customer-phone">Telefon *</label>
                    <input type="tel" id="customer-phone" name="customer_phone" required>
                </div>
                
                <div class="form-group">
                    <label for="pickup-time">Abholzeit *</label>
                    <select id="pickup-time" name="pickup_time" required>
                        <option value="">Bitte wählen...</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="order-notes">Notizen (optional)</label>
                    <textarea id="order-notes" name="order_notes" rows="3"></textarea>
                </div>
                
                <button type="submit" class="btn-primary btn-order">
                    Bestellung aufgeben
                </button>
            </form>
        </div>
    </div>
    
    <script>
    // Einfache JavaScript-Implementierung
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Tantawan Order Form loaded');
        
        // Hier würde die Bestelllogik implementiert werden
        // Für WordPress ist dies eine vereinfachte Version
    });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode('tantawan_order', 'tantawan_order_form_shortcode');

/**
 * Speisekarte Shortcode
 */
function tantawan_menu_shortcode($atts) {
    $atts = shortcode_atts(array(
        'category' => 'all',
    ), $atts);
    
    ob_start();
    ?>
    <div class="tantawan-menu">
        <div class="menu-header">
            <h2>Unsere Speisekarte</h2>
            <p>Frisch zubereitet • Günstige Preise • Authentisch asiatisch</p>
        </div>
        
        <div class="menu-grid">
            <!-- Vorspeisen -->
            <div class="menu-category">
                <h3>Vorspeisen</h3>
                
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
                <h3>Hauptgerichte</h3>
                
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
                <h3>Desserts</h3>
                
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
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('tantawan_menu', 'tantawan_menu_shortcode');

/**
 * Custom Post Type für Speisekarte (Optional)
 */
function tantawan_create_menu_post_type() {
    register_post_type('menu_item',
        array(
            'labels' => array(
                'name' => 'Speisekarte',
                'singular_name' => 'Gericht',
            ),
            'public' => true,
            'has_archive' => true,
            'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
            'menu_icon' => 'dashicons-food',
        )
    );
}
add_action('init', 'tantawan_create_menu_post_type');
?>
```

3. **Datei speichern:**
   - **Dateiname:** `functions.php`
   - **Dateityp:** "PHP" oder "Alle Dateien"
   - **Wichtig:** Achten Sie darauf, dass keine Leerzeichen vor `<?php` oder nach `?>` stehen!

### 📝 **3. index.php erstellen und speichern**

1. **Neues Dokument erstellen**
2. **Vollständigen HTML/PHP-Code einfügen:**

```php
<?php
/**
 * Tantawan Restaurant - Haupttemplate
 * 
 * Das ist die Hauptseite Ihres Tantawan Restaurant Themes
 */

// Sicherheit
if (!defined('ABSPATH')) {
    exit;
}

get_header(); ?>

<main id="main" class="site-main">
    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="hero-content">
                <h1>Tantawan</h1>
                <p class="hero-subtitle">Authentische Asiatische Küche</p>
                <p class="hero-description">Frisch gekocht • Extrem fein • Günstige Preise</p>
                <div class="hero-buttons">
                    <a href="#menu" class="btn-primary">Jetzt Bestellen</a>
                    <a href="#about" class="btn-secondary">Mehr erfahren</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Über uns Section -->
    <section id="about" class="about-section">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h2>Willkommen bei Tantawan</h2>
                    <p>Seit der Eröffnung in Frauenfeld verwöhnen wir unsere Gäste mit authentischer asiatischer Küche. Unser Name "Tantawan" steht für Qualität, Frische und erschwinglichen Genuss.</p>
                    <p>Wir kombinieren traditionelle Kochkunst mit modernem Service. Bestellen Sie einfach online und holen Sie Ihr frisch zubereitetes Essen ab - schnell, bequem und immer köstlich.</p>
                    
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number">1000+</div>
                            <div class="stat-label">Zufriedene Kunden</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">15-30</div>
                            <div class="stat-label">Min Zubereitungszeit</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/restaurant-interior.jpg" 
                         alt="Tantawan Restaurant Interior" 
                         class="about-image">
                </div>
            </div>
        </div>
    </section>

    <!-- Speisekarte Section -->
    <section id="menu" class="menu-section">
        <div class="container">
            <div class="section-header">
                <h2>Unsere Speisekarte</h2>
                <p>Entdecken Sie unsere Auswahl an frisch zubereiteten asiatischen Gerichten. Alle Preise verstehen sich für Takeaway.</p>
            </div>
            
            <?php 
            // Speisekarte-Shortcode anzeigen
            echo do_shortcode('[tantawan_menu]'); 
            ?>
        </div>
    </section>

    <!-- Bestellformular Section -->
    <section id="order" class="order-section">
        <div class="container">
            <div class="section-header">
                <h2>Online Bestellen</h2>
                <p>Bestellen Sie bequem online und holen Sie Ihr Essen ab!</p>
            </div>
            
            <?php 
            // Bestellformular-Shortcode anzeigen
            echo do_shortcode('[tantawan_order]'); 
            ?>
        </div>
    </section>

    <!-- Newsletter Section -->
    <section class="newsletter-section">
        <div class="container">
            <div class="newsletter-content">
                <h2>Newsletter</h2>
                <p>Bleiben Sie auf dem Laufenden mit unserem Newsletter!</p>
                
                <form class="newsletter-form" method="post" action="<?php echo admin_url('admin-post.php'); ?>">
                    <input type="hidden" name="action" value="tantawan_newsletter">
                    <?php wp_nonce_field('tantawan_newsletter_nonce'); ?>
                    
                    <div class="form-row">
                        <input type="email" name="newsletter_email" placeholder="Ihre E-Mail-Adresse" required>
                        <button type="submit" class="btn-primary">Anmelden</button>
                    </div>
                </form>
            </div>
        </div>
    </section>

    <!-- Kontakt Section -->
    <section id="contact" class="contact-section">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h2>Kontakt & Standort</h2>
                    
                    <div class="contact-info">
                        <div class="contact-item">
                            <h4>📍 Adresse</h4>
                            <p>Zürcherstrasse 232<br>8500 Frauenfeld</p>
                        </div>
                        
                        <div class="contact-item">
                            <h4>📞 Telefon</h4>
                            <p><a href="tel:+41527212222">+41 52 721 22 22</a></p>
                        </div>
                        
                        <div class="contact-item">
                            <h4>✉️ E-Mail</h4>
                            <p><a href="mailto:info@tantawan.ch">info@tantawan.ch</a></p>
                        </div>
                    </div>
                    
                    <div class="opening-hours">
                        <h4>🕐 Öffnungszeiten</h4>
                        <div class="hours-list">
                            <div class="hours-item">
                                <span>Montag - Donnerstag</span>
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
                
                <div class="col-md-6">
                    <div class="map-container">
                        <!-- Google Maps Einbettung -->
                        <iframe 
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2701.234567890123!2d8.901234567890123!3d47.556789012345678!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sZ%C3%BCrcherstrasse%20232%2C%208500%20Frauenfeld!5e0!3m2!1sde!2sch!4v1234567890123!5m2!1sde!2sch" 
                            width="100%" 
                            height="300" 
                            style="border:0;" 
                            allowfullscreen="" 
                            loading="lazy" 
                            referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                    
                    <div class="takeaway-info">
                        <h4>🍜 Takeaway Service</h4>
                        <p>Bestellen Sie online und holen Sie Ihr Essen einfach ab. Kein Lieferservice - aber immer frisch zubereitet!</p>
                        <p><strong>Zubereitungszeit:</strong> 15-30 Minuten je nach Bestellmenge</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <?php
    // WordPress Loop für Posts (falls vorhanden)
    if (have_posts()) :
        echo '<section class="blog-section"><div class="container">';
        echo '<h2>Neuigkeiten</h2>';
        
        while (have_posts()) : the_post(); ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
                <div class="post-meta">
                    <span>📅 <?php the_date(); ?></span>
                    <span>👤 <?php the_author(); ?></span>
                </div>
                <div class="post-content">
                    <?php the_excerpt(); ?>
                </div>
                <a href="<?php the_permalink(); ?>" class="read-more">Weiterlesen →</a>
            </article>
        <?php endwhile;
        
        echo '</div></section>';
    endif;
    ?>

</main>

<?php get_footer(); ?>
```

3. **Datei speichern:**
   - **Dateiname:** `index.php`
   - **Dateityp:** "PHP" oder "Alle Dateien"
   - **Speicherort:** Ihr Theme-Ordner `tantawan-theme/`

### 📝 **4. header.php und footer.php erstellen**

**header.php:**
```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
    <header class="site-header">
        <div class="container">
            <div class="header-content">
                <div class="site-logo">
                    <a href="<?php echo home_url(); ?>">
                        <h1>Tantawan</h1>
                    </a>
                </div>
                
                <nav class="main-navigation">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'primary',
                        'menu_class'     => 'main-menu',
                        'fallback_cb'    => false,
                    ));
                    ?>
                </nav>
                
                <div class="header-actions">
                    <a href="#order" class="btn-primary btn-small">Bestellen</a>
                </div>
            </div>
        </div>
    </header>
```

**footer.php:**
```php
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <h3>Tantawan</h3>
                    <p>Authentische asiatische Küche in Frauenfeld</p>
                    <p>Zürcherstrasse 232, 8500 Frauenfeld</p>
                    <p>📞 +41 52 721 22 22</p>
                </div>
                
                <div class="footer-hours">
                    <h4>Öffnungszeiten</h4>
                    <p>Mo-Do: 11:00-14:00, 17:00-21:30</p>
                    <p>Fr: 11:00-14:00, 17:00-22:00</p>
                    <p>Sa: 11:00-22:00</p>
                    <p>So: 17:00-21:30</p>
                </div>
                
                <div class="footer-social">
                    <h4>Folgen Sie uns</h4>
                    <a href="#">Facebook</a>
                    <a href="#">Instagram</a>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; <?php echo date('Y'); ?> Tantawan Restaurant. Alle Rechte vorbehalten.</p>
            </div>
        </div>
    </footer>

    <?php wp_footer(); ?>
</body>
</html>
```

### 💾 **So speichern Sie die Dateien korrekt:**

1. **Datei speichern:**
   - Strg+S (Windows) oder Cmd+S (Mac)
   - Oder: Datei → Speichern unter...

2. **Wichtige Einstellungen beim Speichern:**
   - **Encoding:** UTF-8 (wichtig für deutsche Umlaute!)
   - **Zeilenenden:** Unix/Linux (LF) wenn möglich
   - **Dateiname:** Genau wie angegeben (z.B. `index.php`)
   - **Dateierweiterung:** Manuell hinzufügen falls nötig

3. **Ordnerstruktur nach dem Speichern:**
```
tantawan-theme/
├── style.css ✅
├── functions.php ✅
├── index.php ✅
├── header.php ✅
├── footer.php ✅
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
```

### 📁 **Dateien zu WordPress hochladen:**

1. **Theme-Ordner zippen:**
   - Rechtsklick auf `tantawan-theme` Ordner
   - "Senden an" → "ZIP-komprimierter Ordner"

2. **In WordPress hochladen:**
   - WordPress Admin → Design → Themes
   - "Theme hinzufügen" → "Theme hochladen"
   - ZIP-Datei auswählen → "Jetzt installieren"

3. **Theme aktivieren:**
   - Nach Installation → "Aktivieren"

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