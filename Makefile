.PHONY: fmt lint test integration-test

fmt:
	poetry run ruff format .

lint:
	poetry run ruff check .

test:
	poetry run pytest amplitude_python_sdk/tests --cov=amplitude_python_sdk

integration-test:
	poetry run pytest amplitude_python_sdk/integration_tests
