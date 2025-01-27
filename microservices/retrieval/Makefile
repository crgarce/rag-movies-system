.PHONY: help install venv delete-pycache build-ms run-ms up-ms test
.DEFAULT_GOAL := help
environment = "inlined"

help:
	@echo "Invalid command. Please use 'make reset' to reset the environment."

install:
	pip install -r requirements.txt

venv:
	python3 -m venv venv

delete-pycache:
	find ./app -type d -name "__pycache__" -exec rm -rfv {} +

build-ms:
	docker build -t retrieval-service .

run-ms:
	docker run --rm -d --name retrieval-service --network host --env-file .env retrieval-service

up-ms:
	python -m uvicorn app.main:app --reload

test:
	pytest --cov=app 
	pytest --cov-report=html:./test_coverage