PHONY: clean

SHELL := /bin/bash

DO_NOT_TRACK=1

UV_COMPILE_BYTECODE=1
UV_CONCURRENT_DOWNLOADS=4
UV_CONCURRENT_INSTALLS=4
UV_NO_CACHE=1
UV_NO_INSTALLER_METADATA=1
UV_PYTHON="$(HOME)/.pyenv/versions/3.12.3/bin/python"
UV_HTTP_TIMEOUT=60

clean:
	@echo "Cleaning up..."
	@docker container prune -f
	@docker image prune -f
	@docker volume prune -f
	@docker network prune -f
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".DS_Store" -exec rm -rf {} +

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
