# django-backend

Django Backend to support

- CRUD for users
- Authentication with JWT

### Prerequisites

- Python 3.10+
- pip / pipenv
- PostgreSQL (optional)
- Git

### How to start

- Create a virtual environment

  - `python -m venv venv`
  - `source venv/bin/activate`

- Install dependencies
  - `pip install -r requirements.txt`
- Creating the env

  - `DATABASE_NAME=potgres
DATABASE_USER=potgres
DATABASE_PASSWORD=potgres
DATABASE_HOST=potgres
DATABASE_PORT=5432`

- Run Migrations

  - `python manage.py migrate`

- Run Server
  - `python manage.py runserver`
