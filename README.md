

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


# DOCKER 
##  ⚠️ MAKE SURE DOCKER DESKTOP IS RUNNING ⚠️
docker build -t  <image_name_of_your_choosing>:<version_of_your_choosing> . # from root dont forget the '.'
# example
docker build -t analytics-api:latest .
docker images | grep <image_youre_looking_for>

docker-compose up -d --build (start in detached mode)

docker-compose down
# follow logs (live)
docker-compose logs -f

# follow only api logs (live)
docker-compose logs -f api

# follow only db logs (live)
docker-compose logs -f db

docker-compose ps


# Stop containers
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v

# Clean up
docker system prune -f

# Check for hidden characters or spaces
cat -A .env.docker

# Execute commands in docker container started with docker-compose
docker-compose exec <container_name_from_service_docker-compose_yaml, service_name> <cmd> <path/to/file.py>
# example: load test data from python script
docker-compose exec api python app/scripts/load_test_data.py
# Check total number of events from db
docker-compose exec db psql -U appuser -d analytics_api -c "SELECT COUNT(*) FROM events;"

# DOCKER NETWORKING

  # list networks
  docker network ls
  # Inspect network
  docker inspect <any_network_from_list_above>
  # example: 
  docker inspect analytics_api_analytics_network
  # get network IP Address
  docker inspect  <any_network_from_list_above> | grep IPAddress
  # example:
  docker inspect analytics_api | grep IP

  # To ping one network from the container of a connected network
  docker-compose exec -u  root <service_name> bash
  eg : docker-compose exec -u  root api bash
  #  then....
  ping -c 3 <service-name>
 # With curl
 curl -v telnet://<service_name>:<service_port>
 eg: curl -v telnet://db:5432


 ## Force Docker-compose rebuild after updating Dockerfile
  # Stop everything
    docker-compose down

  # Remove the image to force rebuild
    docker rmi analytics_api_api

  # Or remove all images
    docker-compose down --rmi all

  # Rebuild from scratch (no cache)
    docker-compose build --no-cache

  # Start
    docker-compose up -d

  # Wait for startup
    sleep 10

  # Test
    docker-compose exec -u root api bash
    nslookup db    # Should work now!
    ping -c 3 db   # Should work now!