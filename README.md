

# Connect to PostgreSQL BASH
  psql postgres
# Inside psql:
  # create database
  CREATE DATABASE <db-name>;
  CREATE USER <username> WITH PASSWORD '<password>';
  GRANT ALL PRIVILEGES ON DATABASE <db-name> TO postgres;
  # example
  CREATE DATABASE analytics_api;
  CREATE USER postgres WITH PASSWORD 'postgres';
  GRANT ALL PRIVILEGES ON DATABASE analytics_api TO postgres;
# Exit psql 
  \q

# IN .env file
  DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<db-name>
  # example
  DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/analytics_api

  postgresql+asyncpg://postgres:postgres@localhost:5432/analytics_api
    │                    │        │        │         │    │
    │                    │        │        │         │    └─ Database name
    │                    │        │        │         └────── Port
    │                    │        │        └──────────────── Host
    │                    │        └───────────────────────── Password
    │                    └────────────────────────────────── Username
    └─────────────────────────────────────────────────────── Driver

  # Production
    DATABASE_URL=postgresql+asyncpg://admin:SecurePass123@localhost:5432/analytics_api
                                      ^^^^^  ^^^^^^^^^^^^^
                                      USER   PASSWORD

  # On local Mac (no password)
    DATABASE_URL=postgresql+asyncpg://your_username@localhost:5432/analytics_api
                                      ^^^^^^^^^^^^^
                                      (no password needed)
  # Docker
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/analytics_api
                                      ^^^^^^^^ ^^^^^^^^ ^^
                                      USER     PASSWORD HOST changes to "db"!

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

# API swagger docs
http://localhost:8000/docs