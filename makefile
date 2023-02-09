install:
	poetry install

start:
	poetry run python manage.py runserver

ready:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run gunicorn --bind 127.0.0.1:80 task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

lint:
	poetry run flake8

test:
	poetry run python manage.py test .

req:
	poetry export -f requirements.txt --output requirements.txt

test-cov:
	poetry run coverage run manage.py test .
	poetry run coverage xml