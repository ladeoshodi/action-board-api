![GA Logo](readme-assets/GA-logo.png)

# Action Board API

##### Task Management Board

## Overview

This project was developed independently utilising Python/Django and Django Rest Framework for the backend API and ReactJS/TypeScript for the frontend.

_You can find the [frontend deployment here](https://github.com/ladeoshodi/action-board)_

## Live Project

[Play with the live project here](https://action-board.netlify.app)

## Live Docs

- [Swagger UI here](https://action-board-api-4769d6be906d.herokuapp.com/api-docs/swagger-ui/)
- [Redoc here](https://action-board-api-4769d6be906d.herokuapp.co/api-docs/redoc/)

## Database design

![Database design](readme-assets/ActionBoard.png)

### Technologies

- Python
- Django
- Django REST framework
- PostgreSQL

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/ladeoshodi/action-board-api.git
   cd action-board-api
   ```

2. Create and activate a virtual environment:

   ```sh
   pip install --user pipenv
   pipenv shell
   ```

3. Install dependencies:

   ```sh
   pipenv install
   ```

4. Set up environment variables:

   ```sh
   touch .env
   echo SECRET_KEY=YOUR_SECRET_KEY >> .env
   echo DATABASE_NAME=YOUR_DATABASE_NAME >> .env
   echo ENVIRONMENT=DEV >> .env
   ```

5. Apply migrations:

   ```sh
   python manage.py migrate
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

- Access the admin panel at `/admin/`
- API endpoints:
  - `/api/user/` - User-related endpoints
  - `/api/tags/` - Tag-related endpoints
  - `/api/tasklists/` - Task list-related endpoints
  - `/api/tasks/` - Task-related endpoints
