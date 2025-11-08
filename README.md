### INF601 - Advanced Programming in Python
### Alexander Escobedo 
### Mini Project 4
 
 
# Project Title
 
**Miniproject 4 Event RSVP**
 
## Description

Event RSVP is a Django web application that allows users to create, manage, and RSVP to community events. It has secure user registration and login, event creation with details like date and location, an RSVP system with status options, and an organizer dashboard to track attendees. This app uses Bootstrap for design and includes admin customization for easy event management.




## Getting Started
 
### Dependencies
Prerequisites
Before running the project, ensure you have:

* Python 3.10+ installed
* pip package manager
* SQLite (bundled with Python)
* Required Python packages (install via requirements.txt)

* (tzdata package may also be added if using Windows)
### Installing
Clone the repository:

```
https://github.com/fhsuae/miniproject4AlexanderEscobedo.git
```
Create and activate a virtual environment:
Windows:

```
python -m venv venv
venv\Scripts\activate
```
macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
 Install dependencies:

```
pip install -r requirements.txt
```
### Executing program
#### Initialize the database:

Ensure your current working directory is the Event_RSVP_App directory before running these commands

generates SQL commands to enter into the database
```
python manage.py makemigrations
```

generates SQL commands to apply changes to database
```
python manage.py migrate
```

Creating admin user  
```
python manage.py createsuperuser
```

Run the django development server
```
python manage.py runserver
```
Open your web browser and go to:
```
http://127.0.0.1:8000/
```

### Using an IDE (Optional)
If you are using an IDE like PyCharm or VS Code:
* Open the project folder
* Go to Edit Configurations → Add New Configuration → Django Server.
* Set working directory to the project folder
* Enable Django Support (if using Pycharm) and set root point to app directory 
* Point to Setting.py file in app/mysite/setting.py
* Set Manage script to manage.py file in app/manage.py 
* Click the Run ▶️ button to start the development server.

This lets you run and debug the Django app with one click.

* If you are using another program that utilizes prot 8000, you may change the port number by editing configurations and entering a port number that is not in use (8001 for example)

### Project Pages



## Authors
 
Alexander Escobedo 

 
## Version History

* 0.1
    * Initial Release
 
## Acknowledgments

* [Django Documentation](https://docs.djangoproject.com/en/5.2/)
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/download/)
* [The Official Django Tutorial ](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)- Project structure adapted from this tutorial (django version 5.2)
* [SQLite Documentation](https://sqlite.org/docs.html)