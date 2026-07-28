# =============================================================================
# MAKEFILE — Developer-Friendly Commands
# =============================================================================
#
# WHY A MAKEFILE:
#   Provides a consistent interface for common tasks. New developers don't need
#   to remember complex commands — just run `make help` to see all available
#   commands. Also ensures everyone runs the same commands (no "works on my machine").
#
# USAGE:
#   make help          — Show all available commands
#   make install       — Install dependencies
#   make dev           — Start development server
#   make test          — Run all tests
#
# NOTE: Commands prefixed with @ suppress command echo (cleaner output)
# =============================================================================
.PHONY: help install dev run 

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
RESET := \033[0m

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Setup & Dependencies
# ---------------------------------------------------------------------------

install: ## Install all dependencies (production + dev + test + lint)
	uv sync --all-groups
	uv run pre-commit install

install-prod: ## Install production dependencies only
	uv sync --no-dev

# ---------------------------------------------------------------------------
# Development
# ---------------------------------------------------------------------------

dev: ## Start development server with hot-reload
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run: ## Start production server
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
