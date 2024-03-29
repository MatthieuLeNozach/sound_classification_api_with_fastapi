# Define the default target that runs when you just type 'make'
all: up

# Target for starting up the application with building images
up:
	@echo "Building and starting up services..."
	CREATE_SUPERUSER=false docker-compose up --build

# Target for starting up the application with superuser creation
up-superuser:
	@echo "Building and starting up services with superuser creation..."
	CREATE_SUPERUSER=true docker-compose up --build

# Target for shutting down the application
down:
	@echo "Shutting down services..."
	docker-compose down

# Target to view logs
logs:
	docker-compose logs

# Use this target to force a rebuild of your Docker containers
rebuild:
	@echo "Rebuilding and starting up services..."
	docker-compose up -d --build

# Add a help command to list available commands
help:
	@echo "Available commands:"
	@echo "  make up            - Build (if necessary) and start up services"
	@echo "  make up-superuser  - Build (if necessary) and start up services with superuser creation"
	@echo "  make down          - Shut down services"
	@echo "  make logs          - View logs"
	@echo "  make rebuild       - Force a rebuild and restart services"

.PHONY: all up up-superuser down logs rebuild help