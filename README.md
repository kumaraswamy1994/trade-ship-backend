# Trade & Transportation Backend

This project is a multi-service FastAPI backend for managing trade and transportation operations, running in Docker containers.

## Features
- Modular FastAPI structure
- Routers for trade, transport, and admin
- Pydantic models
- Environment configuration
- PostgreSQL database
- pgAdmin for database management
- Auto-assignment engine for goods and vehicle assignment

## Services
- **postgres-database**: PostgreSQL database for persistent storage
- **pgadmin**: Web UI for managing PostgreSQL
- **admin**: FastAPI app for admin APIs and activities
- **trade**: FastAPI app for trade APIs and activities
- **transport**: FastAPI app for transport APIs and activities
- **auto-assignment**: Engine for automatic assignment of goods and vehicles

## Getting Started
1. Build and start all services:
	```sh
	docker-compose up --build
	```
2. Access services:
	- Admin API: http://localhost:8001
	- Trade API: http://localhost:8002
	- Transport API: http://localhost:8003
	- Auto-assignment: http://localhost:8004
	- pgAdmin: http://localhost:5050 (default login: admin@admin.com / admin)

## Environment
Copy `.env.example` to `.env` in each service directory and update as needed.

## Database
The PostgreSQL database is available at `localhost:5432` (user: user, password: password, db: tradeship).
