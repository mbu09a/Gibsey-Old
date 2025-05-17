-- Initialize PostgreSQL with pgvector and required schemas

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create pages table
CREATE TABLE IF NOT EXISTS pages (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create vault table for storing user interactions
CREATE TABLE IF NOT EXISTS vault (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID DEFAULT '00000000-0000-0000-0000-000000000000', -- anon for now
  page_id BIGINT REFERENCES pages(id) ON DELETE CASCADE,
  question TEXT,
  answer TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_vault_user_ts ON vault(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pages_embedding ON pages USING ivfflat (embedding vector_cosine_ops);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for updating updated_at
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_pages_updated_at') THEN
        CREATE TRIGGER update_pages_updated_at
        BEFORE UPDATE ON pages
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    END IF;
END
$$;
