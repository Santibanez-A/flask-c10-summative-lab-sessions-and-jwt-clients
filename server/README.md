# Productivity Task API

## Description

A Flask REST API that allows users to securely manage their personal tasks. Users can sign up, log in, create, update, delete, and view only their own tasks. Passwords are encrypted using Bcrypt and authentication is handled with Flask sessions.

## Installation

```bash
pipenv install
pipenv shell
```

## Database Setup

From the server directory:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

## Run

From the server directory:

```bash
python app.py
```

The application runs on:

```
http://localhost:5555
```

## Endpoints

### Authentication

- `POST /signup` - Register a new user
- `POST /login` - Log in
- `GET /check_session` - Check current logged in user
- `DELETE /logout` - Log out

### Tasks

- `GET /tasks` - Get paginated tasks for the logged-in user
- `POST /tasks` - Create a new task
- `PATCH /tasks/<id>` - Update one of your tasks
- `DELETE /tasks/<id>` - Delete one of your tasks