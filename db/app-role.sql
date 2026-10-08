-- app-role.sql — a least-privilege role for the /api/feedback function.
--
-- The function previously connected as neondb_owner, which can DROP and
-- TRUNCATE every table and CREATE databases. The review bar only ever needs to
-- read and write three tables, so give it exactly that: a SQL-injection bug or
-- a leaked string then costs comments, not the schema.
--
-- Note there is no DELETE grant. Removing a comment is a soft delete, i.e. an
-- UPDATE that sets deleted_at, so DELETE is genuinely never needed.
--
--   psql "$DATABASE_URL" -v pw="$(openssl rand -base64 24)" -f db/app-role.sql
-- Then point Vercel's DATABASE_URL at review_app instead of neondb_owner.

\if :{?pw}
\else
  \echo 'Pass a password:  psql ... -v pw="$(openssl rand -base64 24)" -f db/app-role.sql'
  \quit
\endif

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'review_app') THEN
    CREATE ROLE review_app LOGIN;
  END IF;
END $$;

ALTER ROLE review_app WITH PASSWORD :'pw';

GRANT CONNECT ON DATABASE neondb TO review_app;
GRANT USAGE ON SCHEMA public TO review_app;
GRANT SELECT, INSERT, UPDATE ON comments, edits, counters TO review_app;
-- Edits are ephemeral text overrides and the bar offers an explicit "undo all",
-- so they really are deleted. Comments are the durable record and are only ever
-- soft-deleted, so DELETE on comments stays revoked.
GRANT DELETE ON edits TO review_app;

-- Explicitly withhold the destructive ones.
REVOKE DELETE, TRUNCATE, REFERENCES, TRIGGER ON comments FROM review_app;
REVOKE TRUNCATE, REFERENCES, TRIGGER ON edits, counters FROM review_app;
REVOKE DELETE ON counters FROM review_app;
REVOKE CREATE ON SCHEMA public FROM review_app;
