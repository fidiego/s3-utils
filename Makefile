.DEFAULT_GOAL := help
OPEN=$(word 1, $(wildcard /usr/bin/xdg-open /usr/bin/open))
GIT_HEAD=$(shell git rev-parse --short HEAD)
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

.PHONY: help
help: ## Print the help message
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%s\033[0m : %s\n", $$1, $$2}' $(MAKEFILE_LIST) | \
		sort | \
		column -s ':' -t

.PHONY: install
install: ## install dependeices
	@pipenv install

.PHONY: bucket
bucket: ## create a bucket
	@pipenv run python make-bucket.py

.PHONY: name
name: ## generate a random name
	@pipenv run python gen-name.py

.PHONY: delete
delete: ## delete a bucket
	@pipenv run python delete-bucket.py
