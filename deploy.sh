#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Build and start containers
echo "Building and starting containers..."
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d

# Run migrations
echo "Running database migrations..."
docker-compose -f docker-compose.yml exec web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --noinput

# Restart services
echo "Restarting services..."
docker-compose -f docker-compose.yml restart

echo "Deployment completed successfully!" 