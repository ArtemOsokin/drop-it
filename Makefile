CODE = app/api app/core app/db migrations/env.py app/services app/schemas tests
TEST = pytest --verbosity=2 --strict-markers ${arg} -k "${k}" --cov-report term-missing --cov-fail-under=85
BLACK = black --line-length 100 --target-version py313 --skip-string-normalization

.PHONY: lint
lint:
	flake8 --jobs 4 --statistics --show-source --max-line-length=100 $(CODE)
	pylint --jobs 4 --disable=line-too-long $(CODE)
	${BLACK} --check $(CODE)

.PHONY: format
format:
	autoflake --in-place --recursive $(CODE)
	isort $(CODE) --line-length 100
	${BLACK} $(CODE)

.PHONY: check
check: format lint test

.PHONY: check_ci_job
check_ci_job: lint test

.PHONY: test
test:
	${TEST} --cov=.

.PHONY: test-fast
test-fast:
	${TEST} --exitfirst --cov=.

.PHONY: test-failed
test-failed:
	${TEST} --last-failed
