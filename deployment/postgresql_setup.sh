#!/bin/bash

# PostgreSQL Setup Script for Emotion Detection App
# Configures PostgreSQL database and user

set -e

echo "🐘 Setting up PostgreSQL for Emotion Detection App..."

# Generate secure password
DB_PASSWORD=$(openssl rand -base64 32)
echo "Generated database password: $DB_PASSWORD"

# Switch to postgres user and configure database
sudo -u postgres psql << EOF
-- Create database
CREATE DATABASE emotion_detection;

-- Create user
CREATE USER emotion_user WITH PASSWORD '$DB_PASSWORD';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE emotion_detection TO emotion_user;

-- Connect to the database and grant schema privileges
\c emotion_detection;
GRANT ALL ON SCHEMA public TO emotion_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO emotion_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO emotion_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO emotion_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO emotion_user;

\q
EOF

# Configure PostgreSQL for localhost connections
echo "🔧 Configuring PostgreSQL access..."

# Find PostgreSQL version directory
PG_VERSION=$(ls /etc/postgresql/ | head -1)
PG_CONFIG_DIR="/etc/postgresql/$PG_VERSION/main"

# Backup original pg_hba.conf
sudo cp $PG_CONFIG_DIR/pg_hba.conf $PG_CONFIG_DIR/pg_hba.conf.backup

# Configure pg_hba.conf for localhost connections
sudo tee $PG_CONFIG_DIR/pg_hba.conf > /dev/null << 'EOF'
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
EOF

# Configure postgresql.conf for better performance
echo "⚙️ Optimizing PostgreSQL configuration..."
sudo tee -a $PG_CONFIG_DIR/postgresql.conf > /dev/null << 'EOF'

# Custom settings for emotion detection app
max_connections = 100
shared_buffers = 128MB
effective_cache_size = 512MB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
EOF

# Restart PostgreSQL
echo "🔄 Restarting PostgreSQL..."
sudo systemctl restart postgresql

# Test connection
echo "🧪 Testing database connection..."
PGPASSWORD="$DB_PASSWORD" psql -h localhost -U emotion_user -d emotion_detection -c "SELECT version();"

# Create .env file with database configuration
echo "📝 Creating environment configuration..."
cat > ~/app/.env << EOF
# AWS Configuration
AWS_DEFAULT_REGION=us-east-1

# Database Configuration
DATABASE_URL=postgresql://emotion_user:$DB_PASSWORD@localhost:5432/emotion_detection

# Application Configuration
DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)

# If using IAM user credentials (uncomment and fill):
# AWS_ACCESS_KEY_ID=your_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_here
EOF

echo "✅ PostgreSQL setup completed successfully!"
echo ""
echo "📋 Database Information:"
echo "   Database: emotion_detection"
echo "   User: emotion_user"
echo "   Password: $DB_PASSWORD"
echo "   Host: localhost"
echo "   Port: 5432"
echo ""
echo "🔐 Password saved to ~/app/.env file"
echo ""
echo "Next steps:"
echo "1. Upload application code"
echo "2. Setup Python environment"
echo "3. Test database connection"
echo ""
echo "Run: ./deployment/upload_code.sh"
