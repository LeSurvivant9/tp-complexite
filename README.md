# TP Complexite

Projet de TPs de complexité en Python 3.14.

Depot GitHub : `https://github.com/LeSurvivant9/tp-complexite`

## Prérequis

- `uv`

La documentation LaTeX est optionnelle pour le développement.

Prérequis supplémentaires pour la documentation :

- `latexmk`
- `lualatex`
- `chktex`
- `latexindent`

## Clonage

```bash
git clone git@github.com:LeSurvivant9/tp-complexite.git
cd tp-complexite
```

## Installation

Installation minimale pour développer et exécuter le projet :

```bash
uv sync
```

## Lancement rapide

Exécuter tous les tests :

```bash
uv run pytest
```

Vérifier le typage :

```bash
uv run mypy .
```

## Exécution

### TP1

```bash
uv run python -m tp1.main --exercise all
```

### TP2

Résolution d'une instance :

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

## Documentation LaTeX

Cette partie est optionnelle pour le développement.
Elle est utile uniquement si l'on souhaite générer ou vérifier le compte-rendu PDF.

Compilation du compte-rendu :

```bash
make docs
```

Vérification complète de la doc :

```bash
make docs-check
```

## Vérification

Tests :

```bash
uv run pytest
```

Typage statique :

```bash
uv run mypy .
```
