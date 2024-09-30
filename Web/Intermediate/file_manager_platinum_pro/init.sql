
-- Connect to your database
\c database;

-- Create the read-only user
CREATE USER ro_user WITH PASSWORD '3270fff1041c43f4b083b28b66c589ae';

-- Grant connection privileges
GRANT CONNECT ON DATABASE database TO ro_user;

-- Grant usage on the schema
GRANT USAGE ON SCHEMA public TO ro_user;

-- Grant select on all current tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ro_user;
