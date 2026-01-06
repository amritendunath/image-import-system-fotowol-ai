CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    google_drive_id VARCHAR(255),
    size BIGINT,
    mime_type VARCHAR(100),
    storage_path TEXT NOT NULL,
    source VARCHAR(50) DEFAULT 'google_drive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_source ON images(source);
CREATE INDEX IF NOT EXISTS idx_created_at ON images(created_at);
