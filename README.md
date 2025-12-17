# Sanaap Document Management System API

A Django-based REST API for document management with role-based access control (RBAC). The system allows users to upload, retrieve, modify, and delete documents with different permission levels based on their roles.

## Features

- **Document Management**: Upload, retrieve, modify, and delete documents
- **Object Storage**: MinIO integration for scalable document storage
- **Authentication**: JWT-based authentication system
- **RBAC**: Role-based access control with three default roles (normal, staff, admin)
- **Caching**: Redis integration for improved performance
- **API Documentation**: OpenAPI/Swagger documentation via drf-spectacular
- **Type Safety**: Full type checking with Pyright

## Prerequisites

- Python 3.13+
- Docker and Docker Compose (for containerized setup)
- PostgreSQL (if running locally without Docker)
- MinIO (if running locally without Docker)
- Redis (if running locally without Docker)

## Installation

### 1. Install uv

`uv` is a fast Python package installer and resolver. Install it using pip:

```bash
pip install uv
```

Or on macOS/Linux using the standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows, use PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, visit the [uv documentation](https://github.com/astral-sh/uv).

### 2. Clone the Repository

```bash
git clone https://github.com/mxpadidar/sanaap-backend-challenge-api.git
cd sanaap-backend-challenge-api
```

### 3. Install Dependencies

Use the Makefile to install all dependencies:

```bash
make install
```

This command runs `uv sync` which:
- Creates a virtual environment (`.venv`)
- Installs all project dependencies
- Installs development dependencies

### 4. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file according to your setup:

#### For Docker Compose Setup (Default)

The default `.env.example` file is configured for Docker Compose. Keep these values as-is:

```env
POSTGRES_HOST=sanaap-db
MINIO_ENDPOINT=sanaap-s3:9000
REDIS_HOST=sanaap-cache
```

#### For Local Development (Without Docker Backend Services)

If you want to run the Django application locally while using local instances of PostgreSQL, MinIO, and Redis, you need to comment out or modify these host settings:

```env
# Comment these lines or change to localhost
# POSTGRES_HOST=sanaap-db
POSTGRES_HOST=localhost  # Uses default from envs.py

# MINIO_ENDPOINT=sanaap-s3:9000
MINIO_ENDPOINT=localhost:9000  # Uses default from envs.py

# REDIS_HOST=sanaap-cache
REDIS_HOST=localhost  # Uses default from envs.py
```

**Note**: The `sanaap/core/envs.py` file provides these defaults:
- `POSTGRES_HOST`: `localhost`
- `MINIO_ENDPOINT`: `localhost:9000`
- `REDIS_HOST`: `localhost`

When these environment variables are not set or commented out, the application will use the defaults from `envs.py`, which are configured for local development.

**Important**: Don't forget to update other credentials in `.env`:

```env
DJANGO_SECRET=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
POSTGRES_PASSWORD=secure-password
MINIO_ROOT_PASSWORD=secure-password
```

## Running the Application

You have two options for running the application:

### Option 1: Full Docker Compose Setup (Recommended for Quick Start)

This option runs the entire stack (PostgreSQL, MinIO, Redis, and the Django backend) in Docker containers:

```bash
make compose-up
```

This command:
- Starts all services defined in `compose.yaml`
- Automatically runs database migrations
- Sets up RBAC roles
- Creates default users
- Starts the Django development server on `http://localhost:8000`

To stop all services:

```bash
make compose-down
```

### Option 2: Local Django Development (With Dockerized Dependencies)

This option runs only the infrastructure services (PostgreSQL, MinIO, Redis) in Docker, while running the Django application locally for faster development iteration.

#### Step 1: Start Infrastructure Services Only

First, modify `compose.yaml` to comment out the `backend` service, or start only the required services:

```bash
# Start only infrastructure services
docker compose up -d postgres minio redis
```

Or edit `compose.yaml` to comment out the backend service:

```yaml
# Comment out or remove the backend service
# backend:
#   build: .
#   container_name: sanaap-api
#   env_file:
#     - .env
#   depends_on:
#     - postgres
#     - minio
#     - redis
#   ports:
#     - 8000:8000
```

#### Step 2: Configure Environment for Local Django

Update your `.env` file to use the Docker service names (since infrastructure is in Docker):

```env
POSTGRES_HOST=sanaap-db      # Docker container name
MINIO_ENDPOINT=sanaap-s3:9000
REDIS_HOST=sanaap-cache
```

Wait, actually if the Django app runs locally (not in Docker), it needs to connect to the Docker containers via localhost. Let me correct this:

Update your `.env` file:

```env
POSTGRES_HOST=localhost      # Connect to Docker via localhost
MINIO_ENDPOINT=localhost:9000
REDIS_HOST=localhost
```

#### Step 3: Run Database Migrations

```bash
make migrate
```

#### Step 4: Setup RBAC and Users

Run these custom Django commands to set up the system:

```bash
make rbac   # Create roles and permissions
make users  # Create default users
```

#### Step 5: Start Django Development Server

```bash
make run
```

The API will be available at `http://localhost:8000`.

## Custom Django Management Commands

The application provides two custom management commands for initial setup:

### `rbac` - Setup Role-Based Access Control

```bash
make rbac
# or
uv run manage.py rbac
```

This command creates three user groups with specific permissions:

- **normal**: Read-only access to documents
  - Permissions: `read_document`
- **staff**: Read and write access to documents
  - Permissions: `read_document`, `write_document`
- **admin**: Full access to documents
  - Permissions: `read_document`, `write_document`, `delete_document`

The command is idempotent - it can be run multiple times safely without duplicating groups.

### `users` - Create Default Users

```bash
make users
# or
uv run manage.py users
```

This command creates three default users for testing and development:

| Username | Password | Role  | Superuser |
|----------|----------|-------|-----------|
| admin    | admin    | admin | Yes       |
| staff    | staff    | staff | No        |
| normal   | normal   | normal| No        |

**Note**: This command requires that the `rbac` command has been run first. It will fail if the required groups don't exist.

**Security Warning**: Change these default passwords in production environments!

## Development Workflow

### Database Migrations

Create new migrations:

```bash
make migrations
```

Apply migrations:

```bash
make migrate
```

### Code Quality

Run linter (Ruff) to format code:

```bash
make lint
```

Check code style:

```bash
make format
```

Type checking with Pyright:

```bash
make type-check
```

### Testing

Run tests:

```bash
make test
```

### All Quality Checks

Run all checks (install, lint, type-check, test):

```bash
make all
```

### Database Access

Access PostgreSQL console (when using Docker Compose):

```bash
make psql
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## Project Structure

```
sanaap-backend-challenge-api/
├── sanaap/                          # Main application package
│   ├── api/                         # API layer (views, serializers, permissions)
│   │   ├── auth.py                  # JWT authentication
│   │   ├── permissions.py           # Custom permissions
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # API viewsets
│   │   └── exc_handler.py           # Custom exception handler
│   ├── core/                        # Django project settings
│   │   ├── settings.py              # Django settings
│   │   ├── envs.py                  # Environment configuration
│   │   └── urls.py                  # URL routing
│   ├── docs/                        # Document app
│   │   ├── models.py                # Document model
│   │   ├── enums.py                 # Document enums (status)
│   │   └── management/commands/     # Custom management commands
│   │       ├── rbac.py              # RBAC setup command
│   │       └── users.py             # User creation command
│   ├── handlers/                    # Business logic handlers
│   │   ├── login_handler.py         # Login logic
│   │   ├── signup_handler.py        # Signup logic
│   │   ├── doc_upload_handler.py    # Document upload
│   │   ├── doc_modify_handler.py    # Document modification
│   │   └── doc_delete_handler.py    # Document deletion
│   ├── services/                    # External service integrations
│   │   ├── jwt_service.py           # JWT token handling
│   │   └── storage_service.py       # MinIO storage operations
│   ├── container.py                 # Dependency injection container
│   └── exceptions.py                # Custom exceptions
├── tests/                           # Test suite
│   ├── api/                         # API tests
│   ├── handlers/                    # Handler tests
│   ├── services/                    # Service tests
│   └── conftest.py                  # Pytest configuration
├── Makefile                         # Development commands
├── compose.yaml                     # Docker Compose configuration
├── dockerfile                       # Docker image definition
├── pyproject.toml                   # Project dependencies and config
├── .env.example                     # Example environment variables
└── README.md                        # This file
```

## Technology Stack

- **Framework**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL 18.1
- **Cache**: Redis 8.4.0
- **Object Storage**: MinIO
- **Authentication**: JWT
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Dependency Injection**: Punq
- **Package Management**: uv
- **Type Checking**: Pyright
- **Linting**: Ruff
- **Testing**: pytest + pytest-django

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Application environment (dev/prod) | `dev` | No |
| `DJANGO_SECRET` | Django secret key | Random | Yes (prod) |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts list | `["localhost", "127.0.0.1"]` | No |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` | No |
| `POSTGRES_USER` | PostgreSQL username | `postgres` | No |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` | Yes |
| `POSTGRES_DB` | PostgreSQL database name | `postgres` | No |
| `POSTGRES_PORT` | PostgreSQL port | `5432` | No |
| `MINIO_ROOT_USER` | MinIO access key | `minio` | Yes |
| `MINIO_ROOT_PASSWORD` | MinIO secret key | `minio` | Yes |
| `MINIO_ENDPOINT` | MinIO endpoint | `localhost:9000` | No |
| `MINIO_SSL` | Use SSL for MinIO | `false` | No |
| `MINIO_URL_TTL_SEC` | Presigned URL TTL | `600` | No |
| `REDIS_HOST` | Redis host | `localhost` | No |
| `REDIS_PORT` | Redis port | `6379` | No |
| `JWT_SECRET` | JWT signing secret | Random | Yes (prod) |
| `JWT_TTL_SEC` | JWT token TTL in seconds | `600` | No |

## Common Issues and Troubleshooting

### Connection Errors with Docker Services

If you're running Django locally and getting connection errors to PostgreSQL/MinIO/Redis:

1. Ensure Docker services are running: `docker compose ps`
2. Check that you're using `localhost` (not container names) in `.env`
3. Verify ports are correctly exposed in `compose.yaml`

### Permission Denied Errors

If you encounter permission errors when running commands:

```bash
# Ensure the virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Or always use `uv run` prefix for commands.

### Migration Errors

If migrations fail:

```bash
# Reset database (WARNING: destroys all data)
docker compose down -v
docker compose up -d postgres
make migrate
make rbac
make users
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run all quality checks: `make all`
5. Submit a pull request

## License

This project is part of the Sanaap backend challenge.
