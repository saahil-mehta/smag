# Santosh Magnetic Works static site

PORT ?= 8000

.PHONY: help web build

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-8s %s\n", $$1, $$2}'

build: ## Assemble HTML pages from _partials/
	@python3 tools/build.py

web: build ## Build, then serve the site locally (override port with PORT=9000)
	@echo "Serving on http://localhost:$(PORT)  (Ctrl-C to stop)"
	@python3 -m http.server $(PORT)
