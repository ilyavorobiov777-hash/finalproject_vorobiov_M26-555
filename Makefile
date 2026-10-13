install:
	uv sync

project:
	uv run project

build:
	uv build

publish:
	uv publish --dry-run  --token test

package-install:
	uv tool install --force $(wildcard dist/*.whl)

lint:
	uv run ruff check .
