VIRTUALENV_REQUIREMENTS = requirements.txt requirements-dev.txt

.PHONY: all
all: development

.PHONY: deploy
deploy: production
	gcloud app deploy --project yelp-beans --version 1

.PHONY: production
production: export VIRTUALENV_REQUIREMENTS = requirements.txt

.PHONY: development
development: venv install-hooks

.PHONY: install-hooks
install-hooks: venv
	./venv/bin/pre-commit install -f --install-hooks

.PHONY: test
test: development install-hooks
	tox

venv: $(VIRTUALENV_REQUIREMENTS) bin/venv-update
	./bin/venv-update \
	    venv= venv/ --python=python2.7 \
	    install= $(patsubst %,-r %,$(VIRTUALENV_REQUIREMENTS)) \
	    bootstrap-deps= -r requirements-bootstrap.txt \
	    pip-command= pymonkey pip-custom-platform -- pip-faster install --upgrade --prune
	rm -rf $@/local

.PHONY: serve
serve: development
	dev_appserver.py .

.PHONY: clean
clean:
	rm -rf venv/
	rm -rf node_modules/
	rm -rf dist/
