### initalize project
cd project

uv init

uv add django

### creating djnago project
.venv\Scripts\activate  

mkdir project 1

uv run django-admin startproject core project1

    project1 -- ia a main project name

    core -- project main setting 
### important files
url.py - for url mapping

settings.py - for 

### new app for specific usecase
cd projet1

django-admin startapp todos  

models.py -- define database models

test.py -- writing test

view.py -- return stuff definding endpoints and redering 

19.18


migration command
 uv run manage.py makemigrations <app_name>
 uv run manage.py migrate <app_name> <migration_name>

superuser command
    uv run manage.py createsuperuser
superuser pass
admin
admin@123

user
pratham
pratham@xyz.com
Hello@123
