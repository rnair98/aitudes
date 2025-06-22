.PHONY: clean clean-bazel add setup

SHELL := /bin/bash

DO_NOT_TRACK=1

UV_COMPILE_BYTECODE=1
UV_CONCURRENT_DOWNLOADS=4
UV_CONCURRENT_INSTALLS=4
UV_NO_CACHE=1
UV_NO_INSTALLER_METADATA=1
UV_PYTHON="$(which python)"
UV_HTTP_TIMEOUT=60

clean:
	@echo "Cleaning up..."
	@echo "🧹 Cleaning Bazel artifacts..."
	@if command -v bazel >/dev/null 2>&1; then \
		bazel clean --expunge 2>/dev/null || true; \
	fi
	@rm -rf bazel-* 2>/dev/null || true
	@echo "🧹 Cleaning Docker artifacts..."
	@docker container prune -f
	@docker image prune -f
	@docker volume prune -f
	@docker network prune -f
	@echo "🧹 Cleaning Python cache directories..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name ".DS_Store" -exec rm -f {} +
	@echo "✅ Cleanup complete!"

clean-bazel:
	@echo "🧹 Cleaning Bazel artifacts only..."
	@if command -v bazel >/dev/null 2>&1; then \
		bazel clean --expunge; \
	else \
		echo "⚠️  Bazel not found, removing bazel-* directories manually"; \
	fi
	@rm -rf bazel-* 2>/dev/null || true
	@echo "✅ Bazel cleanup complete!"

add:
ifdef PACKAGES
	@if [ -n "$(GROUP)" ]; then \
		uv add --group $(GROUP) $(PACKAGES); \
	else \
		uv add $(PACKAGES); \
	fi
else
	@read -p "Enter dependency group: " group && \
	read -p "Enter package name(s): " packages && \
	if [ -n "$$group" ]; then \
		uv add --group $$group $$packages; \
	else \
		uv add $$packages; \
	fi
endif

setup:
	@uv sync
