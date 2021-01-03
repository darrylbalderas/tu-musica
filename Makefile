dev:
	@python3 -m venv venv
	. ./venv/bin/activate
	pip3 install -r requirements-dev.txt
tooling:
	@rm -rf src/__pycache__
	@black -t py38 src/
	@eradicate src/*
	# vulture src/
	@coverage erase
	@coverage run --branch src/*
	@coverage report -m src/*
	@pycodestyle --show-source --statistics   --max-line-length=88 src/
	@pylint src/
	@mypy --python-version 3.8 --strict src/*
	@python -m flake8 --max-line-length=88 src/*
	@python -m pyflakes src/*
	@bandit -s B101 -ll -f screen src/*
	@radon cc mi raw src/* -na