.PHONY: help reset install venv up-db up-indexer rebuild-indexer down-indexer logs-indexer connect-db
.DEFAULT_GOAL := help
environment = "inlined"

help:
	@echo "Invalid command. Please use 'make reset' to reset the environment."

install:
	pip install -r requirements.txt

venv:
	python3 -m venv venv && source venv/bin/activate

reset:
	docker compose down --volumes && docker compose build && docker compose up

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