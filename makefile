build:
	docker-compose build

up:
	docker-compose up

setup:
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py seed_db
	
test:
	docker-compose run web pytest -v

down:
	docker-compose down
	
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
