# Lets-Collab Backend

Backend for the **Lets-Collab** project, a collaborative platform built for the Permit.io 2025 DEV Challenge hackathon. This Django-based backend provides a REST API for user authentication, project/task management, and access control with audit logging, integrated with Permit.io for permissions (mocked in this implementation).

## Tech Stack
- **Django**: Web framework for building the API.
- **Django REST Framework**: For creating RESTful APIs.
- **JWT Authentication**: For secure user authentication.
- **django-cors-headers**: For handling CORS requests from the frontend.
- **SQLite**: Database (for development; can be swapped for PostgreSQL in production).

## Features
- **User Authentication**: JWT-based authentication with login endpoint.
- **Project Management**: Create and list projects with role-based access.
- **Task Management**: Create and list tasks with time-bound access control.
- **Audit Logging**: Track user actions (admin-only).
- **Access Control**: Role-based permissions (mocked integration with Permit.io).
- **CORS Support**: Allows requests from the frontend (`http://localhost:5173`).

## Prerequisites
- Python (v3.9 or higher)
- pip (v21.x.x or higher)
- Virtualenv (recommended)
- Frontend running at `http://localhost:5173` (see [Lets-Collab Frontend](#frontend-repository))

## Setup Instructions

1. **Clone the Repository**:
  ```
   git clone https://github.com/<your-username>/Lets-Collab.git
   cd Lets-Collab
  ```

 Set Up a Virtual Environment:
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:
```

pip install -r requirements.txt
```
Apply Migrations:
```

python manage.py migrate
```
Create Test Users:
```

python manage.py shell
```
Run the following in the shell:
python

from django.contrib.auth.models import User

# Create admin user
User.objects.create_superuser(username='admin', password='2025DEVChallenge', email='admin@example.com')

# Create regular user
User.objects.create_user(username='newuser', password='2025DEVChallenge', email='user@example.com')
exit()

Start the Development Server:

```
python manage.py runserver
```
The API will be available at http://localhost:8000.

API Endpoints
```
POST /api/token/: Authenticate and get JWT token.
Body: {"username": "admin", "password": "2025DEVChallenge"}

GET /api/projects/: List all projects (authenticated users).

POST /api/projects/: Create a project (authenticated users).
Body: {"name": "Project Name", "owner": 1}

GET /api/tasks/: List all tasks (authenticated users).

POST /api/tasks/: Create a task (authenticated users).
Body: {"project": 1, "title": "Task Title"}

GET /api/audit_logs/: List audit logs (admin-only).
```
Project Structure
```
lets-collab/
├── lets_collab/            # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── collab/                 # Main app
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py       # Audit logging middleware
│   ├── models.py
│   ├── permissions.py      # Mocked Permit.io integration
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py               # Django management script
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
````
Deployment

The backend is deployed on Vercel:
https://Lets-Collab-backend.vercel.app
To deploy on Vercel:
Push the repository to GitHub.

Use a platform like Render or Heroku for Django deployment (Vercel is primarily for static apps, but can be configured with a custom server).

Set up a production database (e.g., PostgreSQL).

Update CORS_ALLOWED_ORIGINS in settings.py to include the frontend URL.

 
