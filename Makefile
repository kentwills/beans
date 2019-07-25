.PHONY: deploy
deploy: build deploy_dispatch
	gcloud app deploy frontend/app.yaml api/app.yaml --project yelp-beans --version 1

.PHONY: development
development:
	make -C frontend/ development
	make -C api/ development

.PHONY: build
build:
	make -C frontend/
	make -C api/

.PHONY: test
test:
	make -C frontend/ test
	make -C api/ test

.PHONY: deploy_dispatch
deploy_dispatch:
	gcloud app deploy dispatch.yaml --project yelp-beans

.PHONY: deploy_cron
deploy_cron:
	gcloud app deploy cron.yaml --project yelp-beans

.PHONY: clean
clean:
	make -C frontend/ clean
	make -C api/ clean
