
help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies"
	@echo "  docs        build documentation"
	@echo "  test        run tests"

env:
	pip install -r requirements.txt

dev: env
	pip install -r requirements.testing.txt

docs:
	$(MAKE) -C docs html

test:
	py.test
