.PHONY: help reset install venv up-db up-retrieval rebuild-retrieval down-retrieval logs-retrieval
.DEFAULT_GOAL := help
environment = "inlined"

help:
	@echo "Invalid command. Please use 'make reset' to reset the environment."

install:
	pip install -r requirements.txt

venv:
	python3 -m venv venv

reset:
	docker compose down --volumes && docker compose build && docker compose up

down:
	docker compose down --volumes

up-:
	docker compose up retrieval

rebuild-retrieval:
	docker compose build retrieval && docker compose up retrieval

down-retrieval:
	docker compose stop retrieval && docker compose rm -f retrieval

logs-retrieval:
	docker compose logs -f retrieval

delete-pycache:
	find ./app -type d -name "__pycache__" -exec rm -rfv {} +

build-ms:
	docker build -t retrieval-service .

run-ms:
	docker run --rm -d --name retrieval-service --network host --env-file .env retrieval-service
