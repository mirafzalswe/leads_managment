# Lead Management Application

A comprehensive Django-based application for managing prospective client leads. This system provides a public interface for prospects to submit their information along with internal tools for attorneys to manage and track leads through different stages of the client acquisition process.

## 🚀 Features

### Public Features
- **Public Lead Submission Form**: Prospects can submit their information without authentication
- **File Upload Support**: Secure resume/CV upload functionality
- **Automatic Email Notifications**: Sends confirmation emails to prospects and notification emails to attorneys
- **Input Validation**: Comprehensive validation for all required fields

### Internal Features
- **Lead Management Dashboard**: View and manage all submitted leads
- **Lead Status Tracking**: Track leads through PENDING and REACHED_OUT states
- **Secure File Access**: Download and view uploaded resumes with proper authentication
- **User Authentication**: Token-based authentication system for attorneys
- **User Management**: Create and manage attorney accounts

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Public API    │    │  Internal API   │    │  Admin Panel    │
│  (No Auth)      │    │ (Auth Required) │    │ (Staff Only)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Django Application                │
         │  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
         │  │    Leads    │  │    Auth     │  │  Email  │ │
         │  │   Module    │  │   Module    │  │ Service │ │
         │  └─────────────┘  └─────────────┘  └─────────┘ │
         └─────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              PostgreSQL Database               │
         │    ┌─────────┐  ┌─────────┐  ┌─────────────┐   │
         │    │  Leads  │  │  Users  │  │ Auth Tokens │   │
         │    │  Table  │  │  Table  │  │    Table    │   │
         │    └─────────┘  └─────────┘  └─────────────┘   │
         └─────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Django 4.2, Django REST Framework 3.14
- **Database**: PostgreSQL 14
- **Authentication**: Token-based authentication
- **File Storage**: Django file handling with secure access
- **Email**: Django email backend (configurable)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with Django integration

## 📁 Project Structure

```
lead_management_app/
├── lead_management_app/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI application
│   └── asgi.py                  # ASGI application
├── leads/                       # Lead management app
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Lead data model
│   ├── serializers.py           # API serializers
│   ├── views.py                 # API views and business logic
│   ├── urls.py                  # Lead-specific URLs
│   └── tests.py                 # Unit tests
├── authentication/              # Authentication app
│   ├── __init__.py
│   ├── apps.py                  # Auth app configuration
│   ├── views.py                 # Authentication views
│   └── urls.py                  # Authentication URLs
├── media/                       # Uploaded files (resumes)
├── staticfiles/                 # Static files
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
└── README.md                    # This file
```

## 🔗 API Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/leads/` | Submit a new lead |

### Internal Endpoints (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leads/` | List all leads |
| GET | `/api/leads/{id}/` | Get specific lead details |
| PATCH | `/api/leads/{id}/` | Update lead state |
| GET | `/api/leads/{id}/resume/` | Download lead's resume |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login and get token |
| POST | `/api/auth/logout/` | Logout (invalidate token) |
| POST | `/api/auth/token/` | Get token (DRF built-in) |
| POST | `/api/auth/change-password/` | Change user password |
| GET | `/api/auth/user-info/` | Get current user info |
| POST | `/api/auth/create-user/` | Create new user (admin only) |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lead-management-app.git
   cd lead-management-app
   ```

2. **Environment Configuration (Optional)**
   
   Create a `.env` file in the project root:
   ```env
   # Database
   POSTGRES_DB=lead_management
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password
   
   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@yourcompany.com
   ATTORNEY_EMAIL=attorney@yourcompany.com
   
   # Django
   SECRET_KEY=your-very-secure-secret-key-here
   DEBUG=False
   ```

3. **Build and start the application**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser account**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - API Base URL: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

## 📚 Usage Guide

### For Prospects (Public Access)

Submit a lead through the public API:

```bash
curl -X POST http://localhost:8000/api/leads/ \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "email=john.doe@example.com" \
  -F "resume=@/path/to/resume.pdf"
```

### For Attorneys (Authentication Required)

1. **Get an authentication token**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **List all leads**
   ```bash
   curl -X GET http://localhost:8000/api/leads/ \
     -H "Authorization: Token YOUR_TOKEN_HERE"
   ```

3. **View a specific lead**
   ```bash
   curl -X GET http://localhost:8000/api/leads/1/ \
     -H "Authorization: Token YOUR_TOKEN_HERE"
   ```

4. **Update a lead's state**
   ```bash
   curl -X PATCH http://localhost:8000/api/leads/1/ \
     -H "Authorization: Token YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"state": "REACHED_OUT"}'
   ```

5. **Download a resume**
   ```bash
   curl -X GET http://localhost:8000/api/leads/1/resume/ \
     -H "Authorization: Token YOUR_TOKEN_HERE" \
     -O -J
   ```

## 👥 User Management

### Creating Users

#### Method 1: Django Admin Interface
1. Login to http://localhost:8000/admin/
2. Navigate to Users → Add User
3. Fill in the required information

#### Method 2: Command Line
```bash
docker-compose exec web python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.create_user(
    username='attorney1',
    email='attorney1@example.com',
    password='secure_password',
    first_name='John',
    last_name='Doe'
)

token = Token.objects.create(user=user)
print(f"Token: {token.key}")
```

#### Method 3: API Endpoint (Admin Only)
```bash
curl -X POST http://localhost:8000/api/auth/create-user/ \
  -H "Authorization: Token ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "attorney2",
    "email": "attorney2@example.com",
    "password": "secure_password",
    "first_name": "Jane",
    "last_name": "Smith",
    "is_staff": false
  }'
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
docker-compose exec web python manage.py test

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

Run specific test files:

```bash
# Test only the leads app
docker-compose exec web python manage.py test leads

# Test with pytest
docker-compose exec web pytest
```

## 📧 Email Configuration

The application sends two types of emails:

1. **Prospect Confirmation**: Sent to the prospect after successful submission
2. **Attorney Notification**: Sent to the attorney when a new lead is submitted

### Development Setup
By default, emails are printed to the console. Check the Docker logs:
```bash
docker-compose logs web
```

### Production Setup
Configure SMTP settings in your environment variables or `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🔒 Security Features

- **Token-based Authentication**: Secure API access using DRF tokens
- **File Upload Security**: Validates and securely stores uploaded files
- **Input Validation**: Comprehensive validation on all API endpoints
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM prevents SQL injection attacks
- **Access Control**: Proper separation between public and private endpoints

## 🚀 Production Deployment

### Environment Variables

Set these environment variables for production:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
POSTGRES_DB=lead_management_prod
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure-production-password
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432

# Email
EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com
ATTORNEY_EMAIL=attorney@your-domain.com
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use a secure `SECRET_KEY`
- [ ] Set up HTTPS/SSL
- [ ] Configure proper email settings
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure static file serving (nginx/cloudflare)
- [ ] Set up rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 API Response Examples

### Lead Submission Response
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "resume": "/media/resumes/resume_xyz.pdf"
}
```

### Lead List Response
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john.doe@example.com",
    "state": "PENDING",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### Authentication Response
```json
{
  "token": "abc123def456ghi789",
  "user_id": 1,
  "username": "attorney1",
  "email": "attorney1@example.com"
}
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check if PostgreSQL container is running
docker-compose ps

# Check database logs
docker-compose logs db
```

**Permission Denied for File Uploads**
```bash
# Fix file permissions
docker-compose exec web chown -R www-data:www-data /app/media/
```

**Token Authentication Not Working**
- Ensure the token is included in the `Authorization` header
- Format: `Authorization: Token your-token-here`
- Check if the token exists in the database

## 📊 Monitoring and Logging

### Development Logging
```bash
# View application logs
docker-compose logs -f web

# View database logs  
docker-compose logs -f db
```

### Log Files
The application logs are configured to output to stdout/stderr, which are captured by Docker.

## 🔄 Database Management

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres lead_management > backup.sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres lead_management < backup.sql
```

### Migrations
```bash
# Create new migration
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Show migration status
docker-compose exec web python manage.py showmigrations
```
