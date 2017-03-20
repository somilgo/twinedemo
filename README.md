Framework: Django

Setup Instructions
--------------------------------
- Create a local Postgres DB and put the credentials in line 79 of /twinePerm/settings.py
- Migrate database using "python manage.py migrate"
- Run local server "python manage.py runserver"
- Navigate to homepage at "localhost:8000/permission/index"
- Use "Create User" button on login page to create users (right now there is no security to prevent anyone from creating an admin account but this is an easy fix given further specifications on admin verification)
- Create jobs from main page and similarly assign recruiters jobs (pretty self-explanatory)

Time Breakdown
-------------------------------
- Planning - 30 minutes
- Backend: Setup - 10 minutes
- Backend: Models - 20 minutes
- Backend: Controller - 25 minutes
- Frontend: Views - 15 minutes
- Review/Comments/Readme - 30 minutes

Total = 2 hours 10 minutes
