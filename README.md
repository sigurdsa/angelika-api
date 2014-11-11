angelika-api
============

Backend (API) for project Angelika - health tracking  
The frontend is in a [separate repository](https://github.com/iver56/angelika-web)

## Setup
* Have virtualenv, pip, python, make
* Create your virtualenv folder with the name "venv": `virtualenv venv`
* `cp api/settings/local.py.example api/settings/local.py`
* `make install`
* `make migrate`
* You can now run `make run` and visit localhost:8000 in your favorite browser

### User groups
On /admin/auth/group/ you create groups with the following names:
* admins
* health-professionals
* hubs
* patients

## Commands

`make install`
Install dependencies that are specified in requirements.txt

`make run`
Fire up a dev server at localhost:8000

`make migrate`
Apply migrations, i.e. migrate your database to the newest structure. Creates a database if you don't have one.

`make migrations`
Create migrations. Do this after you have changed one or more models. Commit the migration files along with the changes in the model(s).

`make shell`
Start the interactive Python shell in your terminal. Here, you can play around with the API Django gives you.

`make test`
Run all the tests

## Contribution guidelines
* Commit your changes to a seperate branch
* "One" feature or bug fix per branch (easier to review)
* `make migrations` should be the last thing you do before commiting changes done in models
* Write tests for your code
* Code style: PEP 8
* Max line length: 100 characters

