.PHONY: run
run:
	python manage.py runserver 0.0.0.0:8000

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: shell
shell:
	python manage.py shell
	
.PHONY: test
test:
	python manage.py test
