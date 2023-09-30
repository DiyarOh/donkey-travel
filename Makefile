PROJECT_NAME=donkeytravel

.PHONY:	start
start:
	docker compose up 

.PHONY:	down
down:
	docker compose	down

.PHONY: migrate
migrate:
	docker compose run web python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker compose run web python manage.py makemigrations

.PHONY: collectstatic
collectstatic:
	docker compose run web python manage.py collectstatic --noinput

