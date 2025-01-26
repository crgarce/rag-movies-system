CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    image TEXT NOT NULL,
    plot TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'idx_embedding' AND n.nspname = 'public'
    ) THEN
        CREATE INDEX idx_embedding ON movies USING ivfflat (embedding) WITH (lists = 100);
    END IF;
END
$$;