Real-Time Individual Chat Application

A real-time one-to-one chat application built using Django MVT, Django Channels,
WebSockets, and Redis.


TECH STACK
----------
Python 3.13
Django 6.0
Django Channels
Redis
WebSockets
SQLite
Bootstrap 5
Daphne (ASGI Server)


FEATURES
--------
- Custom User Model (email-based login)
- User Registration, Login and Logout
- List of users (excluding self)
- Online / Offline status in real time
- One-to-one real-time chat
- Message storage in database
- Read receipts (✓ sent, ✓✓ read)
- Redis-backed WebSocket communication
- Secure WebSocket connections
- Deployed on Railway


PROJECT STRUCTURE
-----------------
django-realtime-chat/
│
├── accounts/
├── communication/
├── chat/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── Procfile
└── README.txt


SETUP STEPS (LOCAL DEVELOPMENT)
-------------------------------

1. Clone the repository

git clone https://github.com/Ashik-A-Ashok/django-realtime-chat.git
cd django-realtime-chat


2. Create and activate virtual environment

python -m venv env
env\Scripts\activate        (Windows)
source env/bin/activate     (Linux / Mac)


3. Install dependencies

pip install -r requirements.txt


4. Run Redis locally

Make sure Redis is running on localhost:6379

redis-server


5. Apply database migrations

python manage.py makemigrations
python manage.py migrate


6. Create superuser (optional)

python manage.py createsuperuser


HOW TO RUN THE PROJECT (LOCAL)
------------------------------

Run the project using Daphne (recommended for WebSockets):

daphne -b 127.0.0.1 -p 8000 chat.asgi:application

Open the browser and go to:

http://127.0.0.1:8000/


DEPLOYMENT (RAILWAY)
--------------------

1. Push the project to GitHub
2. Create a Railway project
3. Add a Django service
4. Add a Redis service
5. Connect Redis service to Django service
6. Add Procfile with the following command:

web: daphne chat.asgi:application --bind 0.0.0.0 --port $PORT

7. Deploy the project


ENVIRONMENT VARIABLES (RAILWAY)
-------------------------------

When Redis service is connected, Railway automatically injects:

REDIS_HOST
REDIS_PORT
REDIS_PASSWORD

These are used by Django Channels for real-time communication.


LIVE DEMO
---------

https://web-production-d93c.up.railway.app


NOTES
-----
- WebSockets use ws:// locally and wss:// in production
- Redis is required for real-time chat and presence
- SQLite is used for simplicity


AUTHOR
------

Ashik A Ashok
GitHub: https://github.com/Ashik-A-Ashok