# Lead Management System

This project is a simple lead collection and management system. It allows external users (prospects) to submit a public form. After submission, the system sends email notifications and allows internal staff to manage leads through a secure API.

## Features

- Public API to submit a lead (first name, last name, email, resume)
- Internal API (protected) to view and update leads
- Email notifications sent to both the prospect and the attorney group
- Lead status management: `PENDING` → `REACHED_OUT`

- API documentation available via Swagger (Additional)

## Tech Stack

- Python, Django, Django REST Framework
- PostgreSQL
- Celery with Redis (for background email sending)
- Docker & Docker Compose

- drf-spectacular for Swagger integration(Additional)

## Branches

- `dev`: main development branch with core functionality

- `swagger`: includes API documentation integration(Additional)

## Makefile Overview

The project includes a `Makefile` with useful commands to simplify development tasks:

| Command         | Description                             |
|----------------|-----------------------------------------|
| `make install` | Install all dependencies                |
| `make migrate` | Run Django migrations                   |
| `make run`     | Start the Django development server     |
| `make test`    | Run all tests                           |
| `make celery-worker` | Start Celery worker               |
| `make celery-beat`   | Start Celery beat scheduler       |
| `make clean`   | Remove cache files                      |
| `make docker-up` / `make docker-down` | Manage Docker containers |
| `make collectstatic` | Collect static files              |

## Getting Started

```bash
git clone https://github.com/mehmonov/lead_test.git
cd lead_tests

docker-compose build
docker-compose up
```

## Run test
```bash
make test
```
## Create superuser
```bash
make superuser
```


### PS *
- Formats code and fixes imports via isort and black
- After create superuser automatic create attorney group
