setup: 
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py seed_db

run:
	python manage.py runserver

test:
	pytest

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete