# BlogHub - REST API

BlogHub is a fully-featured, secure, and modular REST API built using Django and Django REST Framework. It allows users to register, authenticate, and perform full CRUD (Create, Read, Update, Delete) operations on blog posts. This project demonstrates clean architecture, industry-level practices, and RESTful design principles.
---


## Features

### Authentication System
- User registration with strong password validation and custom username/email rules
- JWT-based authentication using SimpleJWT
- Login and logout functionality
- Secure access using access and refresh tokens



### Blog Post Management

#### Authenticated Users Can:
- Create new blog posts  
- Update their own posts  
- Soft delete (mark as deleted) their own posts  

#### Any User (Including Unauthenticated) Can:
- View all blog posts (paginated)  
- Retrieve individual post details  


### Permissions
- Only authenticated users can create posts
- Only the author can edit or delete their post
- Public can read posts freely

### Extras
- Pagination support for post listing
- Custom success and error response formatting for clarity
- Modular utility and validation files for better code maintainability


### Tech Stack
- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Auth: JWT (SimpleJWT)
- Tools: Postman, Git, GitHub

---


## ⚙️ How to Set Up

### Clone the repository

```bash
https://github.com/Shamilnk812/BlogHub-REST-API.git
```

### Navigate to root directory

```bash
cd bloghub
```

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate #linux
venv/scripts/activate  # windows
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Create a .env file in the root directory and add your environment variables

```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=*

DB_NAME=readstack_db
DB_USER=readstack_user
DB_PASSWORD=strong_dummy_password
DB_HOST=localhost
DB_PORT=5432
```

### Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the development server 

```bash
python manage.py runserver
```

- Open your browser and go to http://localhost:8000
