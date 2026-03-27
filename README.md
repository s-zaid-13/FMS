# Community Fund Management System (FMS)

A **Django-based web application** designed to manage community financial operations such as deposits, loans, repayments, and member management. This system is ideal for community groups, cooperatives, or small financial organizations that require a secure and transparent way to handle shared funds.

---

## Project Overview

The **Community Fund Management System (FMS)** provides a complete digital solution for managing financial activities within a community. It allows members to request deposits and loans while administrators manage approvals, monitor transactions, and maintain the central fund balance.

The system ensures **financial transparency, secure transactions, and efficient administrative control**.

---

## Technology Stack

### Backend

* Python
* Django 6.0.3

### Database

* PostgreSQL (Supabase)

### Frontend

* HTML5
* Bootstrap 5
* JavaScript 

### Data Visualization

* ApexCharts

### Authentication

* Django Allauth
* Google OAuth Integration

### Email Service

* SMTP (Gmail)

### Deployment

* Vercel (Serverless Deployment)

### Security

* CSRF Protection
* Rate Limiting
* Secure Session Management
* SSL Enforcement

---

## Key Features

### 1. Authentication & User Management

* Email-based authentication (no usernames required)
* OTP verification for account activation (6-digit, 1-minute expiry)
* Role-based access control (Admin / Member)
* Google OAuth login
* Password reset via email
* Rate limiting on authentication endpoints
* Middleware to block inactive users

---

### 2. Member Management

* Automatic profile creation linked to user accounts
* Member dashboard with personal financial overview
* Admin interface for managing members
* Transaction history tracking

---

### 3. Deposit Management

* Members can submit deposit requests
* Admin approval or rejection workflow
* Fund balance automatically updated upon approval
* Email notifications for deposit status updates
* Deposit history and analytics tracking

---

### 4. Loan Management

* Members can request loans with amount, reason, and repayment period
* Admin approval with fund balance validation
* Loan repayment tracking
* Automatic remaining balance calculation
* Loan marked completed when fully repaid
* Email notifications for loan events

---

### 5. Financial Oversight

* Central fund balance tracking
* Transaction validation to prevent errors
* Protection against insufficient funds
* Full audit trail for financial operations
* Monthly financial analytics

---

### 6. Reporting & Analytics

* CSV export for deposits, loans, and members
* Interactive dashboard with ApexCharts
* Monthly cash flow visualization
* Loan distribution analytics
* Member financial summaries

---

### 7. Administrative Features

* Approve pending deposits, loans, and repayments
* Manage members
* Monitor transaction history
* System-wide financial analytics
* Data export for reporting

---

## Data Models

### User

Custom Django user model extending `AbstractUser`.

Fields include:

* Email (used for authentication)
* Role (Admin / Member)
* Active status
* OTP verification support

---

### Member

Linked one-to-one with the user.

Tracks:

* Total deposited amount
* Current loan balance
* Member financial activity

---

### Fund

Represents the **central community fund**.

Automatically updated during:

* Deposit approvals
* Loan approvals
* Loan repayments

---

### Deposit

Stores deposit requests.

Fields include:

* Member
* Amount
* Date
* Notes
* Status (Pending / Approved / Rejected)

---

### Loan

Tracks loan requests.

Fields include:

* Member
* Amount
* Repayment months
* Reason
* Status (Pending / Approved / Rejected / Completed)
* Remaining balance

---

### LoanPayment

Tracks loan repayments.

Fields include:

* Loan reference
* Payment amount
* Date
* Status

---

## Security Features

The system includes multiple security layers:

* Environment-based configuration using `.env`
* Secure session cookies
* CSRF protection on all forms
* XSS protection
* Rate limiting on authentication endpoints
* SSL redirection in production
* Input validation and sanitization

---

## User Experience

The system provides a modern and responsive user interface:

* Responsive Bootstrap 5 design
* Mobile-friendly layout
* AJAX-powered forms
* Real-time notifications
* Modal-based workflows
* Interactive financial charts

---

## Project Structure

```
project-root
│
├── apps
│   ├── accounts
│   ├── members
│   ├── deposits
│   ├── loans
│   ├── dashboard
│   ├── reports
│   ├── notifications
│   └── core
│
├── config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static
├── templates
├── media
├── manage.py
└── requirements.txt
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/community-fund-system.git
cd community-fund-system
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

---

### 5. Run migrations

```bash
python manage.py migrate
```

---

### 6. Create superuser

```bash
python manage.py createsuperuser
```

---

### 7. Run development server

```bash
python manage.py runserver
```

---

## Deployment

This project can be deployed using:

* **Vercel** for serverless hosting
* **Supabase PostgreSQL** for database

Deployment includes:

* Environment variable configuration
* Static file serving
* Production security settings

---

## Business Logic

The system ensures financial integrity through:

* Preventing loans exceeding available funds
* Transaction atomicity for safe database operations
* Complete audit trail for financial transactions
* Protection against multiple active loans per member
* Automated notifications for major financial events

---

## Scalability

The system architecture supports future expansion:

* Modular Django apps
* Optimized database queries
* Aggregated analytics queries
* REST API foundation for mobile applications
* Potential background job processing

---

## Future Improvements

Possible enhancements include:

* Mobile application integration
* Payment gateway integration
* SMS notifications
* Automated scheduled reports
* Background task processing (Celery)
* Advanced financial analytics

---

## License

This project is licensed under the **MIT License**.

---

## Author

Developed by **Samama Zaid**
