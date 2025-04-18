CELERY_PROJECT_NAME = config
PYTHON = python
PIP = pip
MANAGE = $(PYTHON) manage.py
CELERY = celery

.PHONY: install migrate run test celery-worker celery-beat celery-flower \
        clean format docker-build docker-up docker-down

install:
	$(PIP) install -r requirements.txt

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

run:
	$(MANAGE) runserver 0.0.0.0:8000
test:
	$(MANAGE) test

celery-worker:
	$(CELERY) -A $(CELERY_PROJECT_NAME) worker --loglevel=info
celery-beat:
	$(CELERY) -A $(CELERY_PROJECT_NAME) beat --loglevel=info

celery-flower:
	$(CELERY) -A $(CELERY_PROJECT_NAME) flower --port=5555
celery-all:
	$(CELERY) -A $(CELERY_PROJECT_NAME) worker --beat --loglevel=info

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name ".coverage" -delete
	find . -name "htmlcov" -type d -exec rm -rf {} +


shell:
	$(MANAGE) shell_plus --ipython || $(MANAGE) shell


collectstatic:
	$(MANAGE) collectstatic --noinput
