# Santosh Magnetic Works static site

PORT ?= 8000
MIRROR_PORT ?= 4000
MIRROR_DIR := reference-mirror/www.eclipsemagnetics.com

SITE_PORT ?= 8000
LANGS ?= hi mr gu kn te ml ta

.PHONY: help web build serve-mirror serve-site i18n-extract i18n-check i18n

help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

serve-mirror: ## Serve the pristine reference mirror (reference only, never edit/deploy)
	@test -d $(MIRROR_DIR) || { echo "Mirror not found at $(MIRROR_DIR). Run the wget mirror first."; exit 1; }
	@python3 tools/serve.py $(MIRROR_DIR) $(MIRROR_PORT)

serve-site: ## Serve the editable working copy in site/ (local-only until scrubbed)
	@test -f site/index.html || { echo "site/ working copy not found."; exit 1; }
	@python3 tools/serve.py site $(SITE_PORT)

build: ## Assemble HTML pages from _partials/
	@python3 tools/build.py

web: build ## Build, then serve the site locally (override port with PORT=9000)
	@python3 tools/serve.py . $(PORT)

i18n-extract: ## Collect translatable text from the English site into the catalogue and work files
	@python3 tools/i18n/extract.py && python3 tools/i18n/split_work.py

i18n-check: ## Check the translations (LANGS="hi" for one language)
	@for l in $(LANGS); do python3 tools/i18n/check.py $$l; done

i18n: ## Build the language copies of the site from the English pages and translations
	@python3 tools/i18n/build.py
