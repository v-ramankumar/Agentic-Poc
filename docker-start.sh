#!/bin/bash

echo "Starting Preauth Agent with Docker Compose..."
echo "=========================================="

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Wait a moment for services to start
echo "Waiting for services to start..."
sleep 10

# Show service status
echo ""
echo "Service Status:"
docker-compose ps

echo ""
echo "=========================================="
echo "Services Started Successfully!"
echo "=========================================="
echo ""
echo "🚀 Preauth Agent API: http://localhost:8001"
echo "📖 API Documentation: http://localhost:8001/docs"
echo "🔍 Health Check: http://localhost:8001/health"
echo "🍃 MongoDB: mongodb://localhost:27017"
echo "🗄️  MongoDB Admin: http://localhost:8081 (admin/admin123)"
echo ""
echo "To view logs: docker-compose logs -f preauth-api"
echo "To stop services: docker-compose down"
echo "=========================================="
