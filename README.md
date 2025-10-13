

# Run Analytics API DB
psql analytics_api


# To start postgres in general 
psql postgres

# trouble  shooting
# Check if PostgreSQL is installed
brew list | grep postgresql

# Start PostgreSQL
brew services start postgresql@16

# If that doesn't work, try:
brew services start postgresql

# Verify it's running
brew services list | grep postgresql



# If permission issues In psql, run:
ALTER USER postgres WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE analytics_api TO postgres;


# Connect to database Bash
psql analytics_api

# check to see tables
\dt

# Check specific table
\d <tableName>
\d events


# Run server FROM ROOT
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000