-- Create the vault table
CREATE TABLE IF NOT EXISTS vault (
    id SERIAL PRIMARY KEY,
    page_id VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    symbol_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on page_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_vault_page_id ON vault (page_id);

-- Create an index on symbol_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_vault_symbol_id ON vault (symbol_id);
