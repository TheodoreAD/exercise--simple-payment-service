install:
	pip install .

install-dev:
	pip install --editable .
	pip install -r requirements-test.txt

start:
	simple_payment_service

start-dev:
	simple_payment_service_dev

format:
	black --line-length=120 .

format-check:
	black --line-length=120 --check .

lint:
	flake8 --max-line-length=120

test:
	pytest -v tests
