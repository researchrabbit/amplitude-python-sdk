.PHONY: fmt lint test

fmt:
	poetry run black .

lint:
	poetry run pylint amplitude_python_sdk

test:
	poetry run pytest amplitude_python_sdk --cov=amplitude_python_sdk
