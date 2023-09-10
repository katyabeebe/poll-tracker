.PHONY: dev
dev:
	pip install -qU pip
	poetry config virtualenvs.in-project true
	poetry install

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name __pycache__ -delete
	rm -rf .venv

.PHONY: test
test:
	poetry run pytest 