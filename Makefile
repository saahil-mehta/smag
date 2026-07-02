# Santosh Magnetic Works static site

PORT ?= 8000
MIRROR_PORT ?= 4000
MIRROR_DIR := reference-mirror/www.eclipsemagnetics.com

SITE_PORT ?= 8000

.PHONY: help web build serve-mirror serve-site

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

serve-mirror: ## Serve the pristine reference mirror (reference only, never edit/deploy)
	@test -d $(MIRROR_DIR) || { echo "Mirror not found at $(MIRROR_DIR). Run the wget mirror first."; exit 1; }
	@echo "Serving reference mirror on http://localhost:$(MIRROR_PORT)  (Ctrl-C to stop)"
	@cd $(MIRROR_DIR) && python3 -m http.server --bind 127.0.0.1 $(MIRROR_PORT)

serve-site: ## Serve the editable working copy in site/ (local-only until scrubbed)
	@test -f site/index.html || { echo "site/ working copy not found."; exit 1; }
	@echo "Serving working site on http://localhost:$(SITE_PORT)  (Ctrl-C to stop)"
	@cd site && python3 -m http.server --bind 127.0.0.1 $(SITE_PORT)

build: ## Assemble HTML pages from _partials/
	@python3 tools/build.py

web: build ## Build, then serve the site locally (override port with PORT=9000)
	@echo "Serving on http://localhost:$(PORT)  (Ctrl-C to stop)"
	@python3 -m http.server --bind 127.0.0.1 $(PORT)
