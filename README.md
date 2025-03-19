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
