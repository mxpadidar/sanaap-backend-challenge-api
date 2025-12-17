# SANAAP Document Management System API

A Django REST API for document management with role-based access control (RBAC), file storage using MinIO, and Redis caching.

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/release/python-31311)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- Docker & Docker Compose

### Installing UV

```bash
curl -LsSf https://astral. sh/uv/install.sh | sh

# Or using pip
pip install uv
```

## Installation

```bash
git clone https://github.com/mxpadidar/sanaap-backend-challenge-api.git
cd sanaap-backend-challenge-api

# install deps using uv
make install
```

## Running the Application

The API will be available at http://localhost:8000/docs

```bash
# Create environment file
cp .env.example .env
```

### Using Docker Compose

```bash
# Start all services (PostgreSQL, MinIO, Redis, Backend API)
make compose-up

# To stop all services:
make compose-down
```

### Local

First update `.env` and comment out the container hostnames:

```bash
# POSTGRES_HOST=sanaap-db
# MINIO_ENDPOINT=sanaap-s3:9000
# REDIS_HOST=sanaap-cache
```

Run this commands in order:

```bash
# Start infrastructure services only (PostgreSQL, MinIO, and Redis):
make infra-up

# database migrations
make migrate

# Set up RBAC roles and default users
make rbac
make users

# Run the development server
make run
```

## Custom Management Commands

- The `rbac` command must be run first (requires groups to exist)

### `rbac`: Setup required groups and permission for Document model

- Creates three permission groups: `normal`, `staff`, and `admin`
- Assigns document permissions to each group:
  - **normal**: `read_document`
  - **staff**: `read_document`, `write_document`
  - **admin**: `read_document`, `write_document`, `delete_document`

### `users` - Create Default Users

- Creates three default users and assigns them to groups:
  - **admin** (superuser): username=`admin`, password=`admin`, group=`admin`
  - **staff**: username=`staff`, password=`staff`, group=`staff`
  - **normal**: username=`normal`, password=`normal`, group=`normal`

## Running Tests

Run the test suite using pytest:

```bash
make test
```

Or run all quality checks (install dependencies, lint, type-check, and test):

```bash
make all
```

This runs:

- `make install` - Install/sync dependencies
- `make lint` - Format code with Ruff
- `make type-check` - Run Pyright static type checking
- `make test` - Run pytest test suite
