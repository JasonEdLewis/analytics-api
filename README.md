

# Running and getting errors 
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