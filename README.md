# Daily Habit Tracker 🧠✨

A Django-based daily wellness tracker to log mood, sleep, yoga, and reflections.

## Features
- User authentication (signup / login)
- Daily mood tracking with emoji scale
- Sleep duration and yoga tracking
- Weekly summary chart
- CSV export of personal data

## Tech Stack
- Python
- Django
- HTML / CSS
- Chart.js

## Setup (local)
```bash
git clone https://github.com/YOUR_USERNAME/daily-habit-tracker.git
cd daily-habit-tracker
python -m venv venv
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
