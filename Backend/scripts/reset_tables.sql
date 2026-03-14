-- Drop UniAid tables so the app can recreate them with the correct schema.
-- Run with: psql "postgresql://user:password@localhost:5432/uniaid" -f scripts/reset_tables.sql
-- Then restart the backend server.
-- Order matters: users has FKs to mentors and mentee.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS mentee;
DROP TABLE IF EXISTS mentors;
