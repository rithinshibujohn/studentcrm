# Student CRM

A Django-based Student CRM (Customer Relationship Management) system developed as an interview assignment. The application enables administrators to manage student records, users, and profiles with features like Excel import, PDF export, authentication, and dashboard analytics.

## Live Demo

https://studentcrm.onrender.com

## GitHub Repository

https://github.com/rithinshibujohn/studentcrm

---

## Features

- User Authentication (Login/Logout)
- Dashboard
- Student Management (CRUD)
- User Management
- Profile Management
- Change Password
- Student Photo Upload
- Excel Bulk Import
- PDF Export
- Responsive SB Admin 2 Interface
- PostgreSQL Database (Production)
- SQLite Database (Development)

---

## Technologies Used

### Backend
- Python
- Django 5

### Frontend
- HTML
- CSS
- Bootstrap
- SB Admin 2

### Database
- SQLite (Development)
- PostgreSQL (Production)

### Libraries
- openpyxl
- pandas
- reportlab
- Pillow
- WhiteNoise
- Gunicorn

### Deployment
- Render

---

## Installation

Clone the repository

```bash
git clone https://github.com/rithinshibujohn/studentcrm.git
```

Navigate into the project

```bash
cd studentcrm
```

Create a virtual environment

```bash
python -m venv env
```

Activate the environment

Windows

```bash
env\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the server

```bash
python manage.py runserver
```

---

## Screenshots


- Dashboard
- Student List
- Student Details
- Student_form
- Profile
- Change_password

---

## Project Structure

```
studentcrm/
│
├── accounts/
├── students/
├── static/
├── templates/
├── media/
├── student_crm/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Known Limitation

The application supports student photo uploads during development.

On the free Render hosting plan, uploaded media files are not persistently served. In a production deployment, this would typically be solved using cloud storage such as Cloudinary or Amazon S3.

---

## Author

**Rithin Shibu John**

Python Full Stack Developer

GitHub:
https://github.com/rithinshibujohn

LinkedIn:
https://www.linkedin.com/in/rithinshibujohn/