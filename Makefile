.PHONY: fmt lint test integration-test

fmt:
	poetry run black .

lint:
	poetry run pylint amplitude_python_sdk

test:
	poetry run pytest amplitude_python_sdk/tests --cov=amplitude_python_sdk

integration-test:
	poetry run pytest amplitude_python_sdk/integration_tests
