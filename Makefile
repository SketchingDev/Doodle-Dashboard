
help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies"
	@echo "  test        run tests"

env:
	pip install -r requirements.txt

dev: env
	pip install -r requirements.testing.txt

tests:
	py.test
