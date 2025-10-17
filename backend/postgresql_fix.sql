-- ========================================
-- POSTGRESQL BERECHTIGUNGEN REPARIEREN
-- Tantawan Restaurant Database Setup
-- ========================================

-- 1. Als postgres-Superuser verbinden
-- sudo -u postgres psql

-- 2. Zur Tantawan-Datenbank wechseln
\c tantawan_restaurant;

-- 3. Alle notwendigen Berechtigungen vergeben
GRANT ALL PRIVILEGES ON DATABASE tantawan_restaurant TO tantawan_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO tantawan_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tantawan_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tantawan_user;

-- 4. Standardberechtigungen für zukünftige Objekte setzen
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tantawan_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tantawan_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO tantawan_user;

-- 5. Schema-Owner ändern (empfohlen)
ALTER SCHEMA public OWNER TO tantawan_user;

-- 6. Verbindung testen
SELECT 'Berechtigungen erfolgreich gesetzt!' as status;

-- 7. PostgreSQL verlassen
\q