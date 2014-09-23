angelika-api
============

Backend (API) for project Angelika - health tracking

# Virtualenv

Create your virtualenv folder with the name "venv"

# Commands

`make install`
Install dependencies that are specified in requirements.txt

`make run`
Fire up a dev server at localhost:8000

`make migrate`
Apply migrations, i.e. migrate your database to the newest structure. Creates a database if you don't have one.

`make migrations`
Create migrations. Do this after you have changed one or more models. Commit the migration files along with the changes in the model(s).
