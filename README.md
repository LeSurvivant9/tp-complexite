# TP Complexite

Projet de TPs de complexite en Python 3.14.

## Prerequis

- `uv`
- une installation LaTeX avec `latexmk`, `lualatex`, `chktex` et `latexindent`

## Installation

```bash
uv sync
```

## Execution

### TP1

```bash
uv run python -m tp1.main --exercise all
```

### TP2

Resolution d'une instance :

```bash
uv run python -m tp2.main --target 120 --numbers 2 10 100
```

Benchmark reproductible :

```bash
uv run python -m tp2.main --benchmark --games-per-size 25 --max-size 6 --seed 123
```

### TP3

Tri d'une liste :

```bash
uv run python -m tp3.main --algorithm merge --values 5 2 4 1 3
```

Benchmark reproductible :

```bash
uv run python -m tp3.main --benchmark --seed 123
```

## Verification

Tests :

```bash
uv run pytest
```

Typage statique :

```bash
uv run mypy .
```

## Documentation

Compilation du compte-rendu :

```bash
make docs
```

Verification complete de la doc :

```bash
make docs-check
```
