.PHONY: diff diff-dir all clean test \
	docker-build-clean docker-build docker-up \
	docker-logs docker-ps \
	docker-down docker-restart \
	docker-rebuild  \
	diff branch-from \
	set-upstream-feature-branches

ifneq ( ,$ (wildcard ./.env))
include .env
export
endif

# Docker Compose Makefile commands
COMPOSE_FILE = docker-compose.yml
# Build containers without using cache
docker-build-clean:
	docker compose -f $(COMPOSE_FILE) build --no-cache --progress=plain
# Build containers
docker-build:
	docker compose -f $(COMPOSE_FILE) build --progress=plain
# Start containers in detached mode
docker-up:
	docker compose -f $(COMPOSE_FILE) up -d
# View logs in follow mode
docker-logs:
	docker compose -f $(COMPOSE_FILE) logs -f
# List all containers
docker-ps:
	docker compose -f $(COMPOSE_FILE) ps -a
# Stop and remove containers and volumes
docker-down:
	docker compose -f $(COMPOSE_FILE) down -v
# Restart containers (down then up)
docker-restart: docker-down docker-up
# Rebuild and restart containers
docker-rebuild: docker-build docker-restart
# Placeholder targets to satisfy checkmake
all:
	@echo "No build steps defined"
clean:
	@echo "🧹 Cleaning cache directories and virtual environment..."
	@rm -rf .uv_cache .idea .pytest_cache .venv uv.lock
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type d -name "smart_invoice_escalation.egg-info" -exec rm -r {} +
	@echo "✅ Clean completed!"
test:
	@echo "No tests defined"
uv_init_env:
	uv venv --python=3.11.11 .venv
	uv pip install --upgrade pip

uv_sync:
	uv pip install -r requirements.txt
# UV dependency management commands
uv_sync_dev:
	uv sync --extra dev
uv_sync_docs:
	uv sync --extra docs
uv_sync_test:
	uv sync --extra test
uv_sync_lint:
	uv sync --extra lint
uv_sync_all:
	uv sync --python 3.12.10 --upgrade --all-groups --all-extras --reinstall --no-cache --resolution=highest
uv_mkdocs_build:
	uv run mkdocs build -v
# Combined environment setup commands
setup_dev: uv_sync_dev
	@echo "Development environment ready!"
setup_docs: uv_sync_docs
	@echo "Documentation tools installed!"
setup_ci: uv_sync_test uv_sync_lint
	@echo "CI environment ready!"

uv_pre_commit:
	uv run pre-commit run --all-files -v --color always
uv_run_tests:
	uv run pytest -n 2 -q tests/**/test_*.py
uv_run_server:
	uv run uvicorn src.main:app --reload --port 8080
uv_mkdoc_serve:
	uv run mkdocs  serve --dirtyreload
uv_mkdoc_build:
	uv run mkdocs -v  build --strict

diff:
	@if [ -z "$(file)" ]; then \
		echo "Usage: make diff file=<path/to/file>"; \
		exit 1; \
	fi; \
	git diff main --unified=0 $(file)

diff-dir:
	@if [ -z "$(dir)" ]; then \
		echo "Usage: make diff-dir dir=<path/to/directory>"; \
		exit 1; \
	fi; \
	git diff main --unified=0 -- "$(dir)"

branch-from:
	@if [ -z "$(SOURCE)" ] || [ -z "$(DEST)" ]; then \
		echo "Error: Missing required parameters"; \
		echo "Usage: make branch-from DEST=<new-branch-name> SOURCE=<source-branch>"; \
		echo "Example: make branch-from DEST=feature/new-feature SOURCE=develop"; \
		exit 1; \
	fi
	@echo "Creating new branch '$(DEST)' from '$(SOURCE)'..."
	@git checkout -b $(DEST) $(SOURCE)
	@echo "Local branch '$(DEST)' created successfully from '$(SOURCE)'."

# Set upstream of all feature/* branches to origin/develop
set-upstream-feature-branches:
	@git for-each-ref --format='%(refname:short)' refs/heads/feature/ | while read branch; do \
			echo "Setting upstream for $$branch to origin/develop..."; \
			git branch --set-upstream-to=origin/develop "$$branch" || echo "Failed to set upstream for $$branch"; \
	done
	@echo "Done setting upstreams for feature branches."

# setting up executable permissions for shell scripts
set-script-permissions:
	@echo "Setting up executable permissions for shell scripts..."
	@find scripts base_vm/scripts -name "*.sh" -type f -exec git update-index --chmod=+x {} \;
	@echo "Adding executable files to git..."
	@git add --chmod=+x scripts/*.sh base_vm/scripts/*.sh 2>/dev/null || true
	@echo "Shell script permissions fixed. Run 'git status' to see changes."
	@echo "Note: If any script is missing a shebang, add '#!/bin/bash' as the first line."
