Framework: Django

Setup Instructions
--------------------------------
- Create a local Postgres DB and put the credentials in line 79 of /twinePerm/settings.py
- Migrate database using "python manage.py migrate"
- Run local server "python manage.py runserver"
- Navigate to homepage at "localhost:8000/permission/index"
- To create SystemUsers and Jobs, first create an admin account using "python manage.py createsuperuser", then login at "localhost:8000/admin" and use UI
- NOTE: Passwords must be set in Python shell ("python manage.py shell") with set_password() method called on SystemUser object

Time Breakdown
-------------------------------
- Planning - 30 minutes
- Backend: Setup - 10 minutes
- Backend: Models - 20 minutes
- Backend: Controller - 25 minutes
- Frontend: Views - 15 minutes
- Review/Comments/Readme - 30 minutes

Total = 2 hours 10 minutes
