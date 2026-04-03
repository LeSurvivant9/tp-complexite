all:
	$(MAKE) -C docs all

docs:
	$(MAKE) -C docs all

docs-check:
	$(MAKE) -C docs check

test:
	uv run pytest

typecheck:
	uv run mypy .

bench-tp1:
	uv run python -m tp1.main --exercise all

bench-tp2:
	uv run python -m tp2.main --benchmark --games-per-size 25 --max-size 6 --seed 123

bench-tp3:
	uv run python -m tp3.main --benchmark --seed 123

clean:
	$(MAKE) -C docs clean

.PHONY: all docs docs-check test typecheck bench-tp1 bench-tp2 bench-tp3 clean
