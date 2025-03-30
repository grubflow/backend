# GrubFlow Backend

The offical backend for GrubFlow's Tender application. This application is built using the Django reset framework and uses postgreSQL.

## Prerequisites

- [UV](https://github.com/astral-sh/uv)
- PostgreSQL 14

## Installation

- Clone the repository

  ```bash
  git clone git@github.com:grubflow/backend.git
  cd backend
  ```

- Setup PostgreSQL local server and create a database

  ```bash
  psql -U postgres
  CREATE DATABASE grubflow_local owner postgres;
  \q
  ```

- Install the dependencies and activate the Python virtual environment

  ```bash
  uv sync
  source .venv/bin/activate
  ```

- Create a `.env` file in the root directory, see `.env.example`

- Run the migrations

  ```bash
  python manage.py migrate
  ```

- Run the server
  ```bash
  python manage.py runserver
  ```

## Migrations

When you make changes to the models, you will need to create and apply migrations. Here’s how to do that:

1. **Create Migrations**: After making changes to your models, run the following command to create migration files:

   ```bash
   python manage.py makemigrations
   ```

   This will generate migration files based on the changes detected in your models.

2. **Apply Migrations**: Once the migration files are created, you need to apply them to your database. Run the following command:

   ```bash
    python manage.py migrate
   ```

   This will apply all pending migrations to your database, ensuring that your database schema is up to date with your models.

## Adding Tests

- Create a new test file in the appropriate app directory, following the naming convention `<app>/tests/<app>_tests.py`.

- Write your test cases using `pytest` and `pytest-django`. For example:

  ```python
  import pytest
  from django.urls import reverse

  @pytest.mark.django_db
  def test_example_view(client):
      response = client.get(reverse('example_view'))
      assert response.status_code == 200
  ```

- Ensure your tests are isolated and do not depend on external state.

- You can use fixtures to set up any necessary database state or mock objects. See `conftest.py` for examples on how to create fixtures.

## Running Tests

To run the tests, use the following command in your terminal:

```bash
# Make sure you are in the root directory of the project
pytest -v
```

Or to run tests in a specific app, you can specify the path to the test file:

```bash
# Run tests for a specific app
pytest -v path/to/your/app/tests/app_tests.py
```

This will execute all the test cases in the specified file and provide a verbose output of the results.
