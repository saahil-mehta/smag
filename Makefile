# Santosh Magnetic Works static site

PORT ?= 8000

.PHONY: help web

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-8s %s\n", $$1, $$2}'

web: ## Serve the site locally (override port with PORT=9000)
	@echo "Serving on http://localhost:$(PORT)  (Ctrl-C to stop)"
	@python3 -m http.server $(PORT)
