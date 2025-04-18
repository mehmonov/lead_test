CELERY_PROJECT_NAME = config
PYTHON = python
PIP = pip
MANAGE = $(PYTHON) manage.py
CELERY = celery

.PHONY: install migrate run test celery-worker celery-beat celery-flower clean format createsuperuser docker-run

install:
	$(PIP) install -r requirements.txt

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

run:
	$(MANAGE) migrate

	$(MANAGE) runserver 0.0.0.0:8000

test:
	$(MANAGE) test

celery-worker:
	$(CELERY) -A $(CELERY_PROJECT_NAME) worker --loglevel=info

celery-beat:
	$(CELERY) -A $(CELERY_PROJECT_NAME) beat --loglevel=info

celery-flower:
	$(CELERY) -A $(CELERY_PROJECT_NAME) flower --port=5555

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name ".coverage" -delete
	rm -rf htmlcov/

docker-up:
	docker compose  up -d --build

docker-down:
	docker compose down --volumes
docker-run:
	docker compose up --build
docker-logs:
	docker compose logs -f --tail=50
docker-shell:
	docker compose exec web sh
docker-superuser:
	docker compose exec web python manage.py createsuperuser
docker-rebuild:
	make docker-down
	make docker-up
