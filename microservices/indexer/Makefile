.PHONY: help reset install venv up-db up-indexer rebuild-indexer down-indexer logs-indexer connect-db
.DEFAULT_GOAL := help
environment = "inlined"

help:
	@echo "Invalid command. Please use 'make reset' to reset the environment."

install:
	pip install -r requirements.txt

venv:
	python3 -m venv venv

build-indexer:
	docker compose build && docker compose up

down:
	docker compose down --volumes

up-db:
	docker compose up -d db

up-indexer:
	docker compose up indexer

rebuild-indexer:
	docker compose build indexer && docker compose up indexer

down-indexer:
	docker compose stop indexer && docker compose rm -f indexer

logs-indexer:
	docker compose logs -f indexer

connect-db:
	docker exec -it postgres_local psql -U ragadmin -d rag_db

py-dev-env:
	sudo apt-get update && sudo apt install -y libpq-dev python3-dev build-essential

delete-pycache:
	find ./app -type d -name "__pycache__" -exec rm -rfv {} +

up-ms:
	python -m uvicorn app.main:app --reload

build-ms:
	docker build -t indexer-service .

run-ms:
	docker run --rm -d --name indexer-service --network host --env-file .env indexer-service

stop-ms:
	docker stop indexer-service
