# LEAD MANAGEMENT APPLICATION

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
- **Asynchronous Task Processing**: Background tasks for email sending and file processing
- **Real-time Monitoring**: Monitor task queues and system health

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
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Celery Task Queue                 │
         │    ┌─────────────┐  ┌─────────────┐            │
         │    │  Workers    │  │  Beat       │            │
         │    │  (Tasks)    │  │  (Scheduler)│            │
         │    └─────────────┘  └─────────────┘            │
         └─────────────────────────────────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              Redis Message Broker              │
         │    ┌─────────────┐  ┌─────────────┐            │
         │    │  Queue      │  │  Cache      │            │
         │    │  (Tasks)    │  │  (Results)  │            │
         │    └─────────────┘  └─────────────┘            │
         └─────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Django 4.2, Django REST Framework 3.14
- **Database**: PostgreSQL 14
- **Authentication**: Token-based authentication
- **File Storage**: Django file handling with secure access
- **Email**: Custom Django email backend with SSL handling
- **Task Queue**: Celery 5.3.6 with Redis 7 as message broker
- **Caching**: Redis for task results and general caching
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with Django integration
- **Monitoring**: Health checks and Flower dashboard

## 🔄 Celery Tasks

The application uses Celery for asynchronous task processing:

- **Email Notifications**: 
  - Sends confirmation emails to prospects
  - Sends notification emails to attorneys
  - Handles email delivery retries
- **File Processing**: 
  - Handles resume file uploads and processing
  - Validates file formats
  - Manages file storage
- **Scheduled Tasks**: 
  - Daily lead status reports
  - Weekly summary emails
  - Database maintenance tasks

## 🏥 Health Checks

The application includes health check endpoints for monitoring:

- **API Health**: `http://localhost:8000/health/`
- **Celery Worker Status**: Available through Flower dashboard
- **Database Connection**: Monitored through Django's health check system
- **Redis Connection**: Monitored through Celery health checks

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
| POST | `/api/auth/create-user/` | Create new user (admin only) |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git
- Python 3.10 or higher (for local development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mirafzalswe/leads_managment.git
cd leads_managment
```

2. **Environment Configuration**
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

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Django
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
```

3. **Build and start the application**
```bash
docker-compose up -d
```

4. **Verify services are healthy**
```bash
curl http://localhost:8000/health/
```

5. **Run database migrations**
```bash
docker-compose exec web python manage.py migrate
```

6. **Create a superuser account**
```bash
docker-compose exec web python manage.py createsuperuser
```

7. **Access the application**
- API Base URL: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- Flower (Celery monitoring): http://localhost:5555/

## 📧 Email Configuration

The application uses a custom email backend to handle SSL certificate issues:

```python
# settings.py
EMAIL_BACKEND = 'leads.email_backend.CustomEmailBackend'
```

This backend automatically handles SSL certificate verification issues that may occur in development environments.

## 🔒 Security Features

- **Token-based Authentication**: Secure API access using DRF tokens
- **File Upload Security**: Validates and securely stores uploaded files
- **Input Validation**: Comprehensive validation on all API endpoints
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM prevents SQL injection attacks
- **Access Control**: Proper separation between public and private endpoints
- **SSL/TLS**: Secure email communication with SSL/TLS support

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

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Celery
CELERY_BROKER_URL=redis://:your-redis-password@your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://:your-redis-password@your-redis-host:6379/0
```

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

## 🔄 Asynchronous Tasks

The application uses Celery for handling asynchronous tasks:

### Email Tasks
- Sending confirmation emails to prospects
- Sending notification emails to attorneys
- Bulk email operations
- Email delivery retry mechanism

### File Processing Tasks
- Resume/CV processing and validation
- File format conversion
- File cleanup operations
- Secure file storage management

### Scheduled Tasks
- Daily lead status reports
- Weekly summary emails
- Database maintenance tasks
- System health checks

### Monitoring Tasks
- System health checks
- Performance metrics collection
- Error reporting
- Task queue monitoring

To monitor Celery tasks, you can use Flower:
```bash
docker-compose exec web celery -A lead_managment_app flower
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
