angelika-api
============

Backend (API) for project Angelika - health tracking  
The frontend is in a [separate repository](https://github.com/iver56/angelika-web)

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

#Contribution guideline
* Commit your changes to a seperate branch
* "One" feature or bug fix per branch (easier to review)
* `make migrations` should be the last thing you do before commiting changes done in models
* Code style: PEP 8
* Max line length: 100 characters
