start:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

lint:
	poetry run flake8