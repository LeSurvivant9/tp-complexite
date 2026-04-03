"""Benchmarks for TP3 sorting algorithms.

Usage:
    uv run python -m tp3.benchmark
    uv run python tp3/benchmark.py
"""

import argparse
import sys
from collections.abc import Callable
from pathlib import Path
from random import Random
from typing import Final

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.axes  # noqa: E402
import matplotlib.figure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from tp3.sorting import (  # noqa: E402
    SortFunction,
    bubble_sort,
    insertion_sort,
    merge_sort,
    selection_sort,
)
from utils.benchmarking import (  # noqa: E402
    BenchmarkPoint,
    benchmark_input,
    benchmark_series,
)
from utils.plotting import save_figure, style_axes  # noqa: E402

DEFAULT_SMALL_SIZE: Final[int] = 1_000
DEFAULT_REPEATS: Final[int] = 1
DEFAULT_SEED: Final[int] = 123
SIZE_GROWTH_FACTOR: Final[int] = 2
TARGET_MEDIUM_RATIO: Final[float] = 10.0
TARGET_LARGE_RATIO: Final[float] = 100.0
MAX_REFERENCE_SIZE: Final[int] = 128_000

SORTING_ALGORITHMS: Final[dict[str, SortFunction]] = {
    "selection": selection_sort,
    "insertion": insertion_sort,
    "bubble": bubble_sort,
    "merge": merge_sort,
}

SortRunner = Callable[[int], list[int]]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lancer les benchmarks du TP3")
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        help=(
            "Tailles d'entrée explicites à mesurer au lieu des tailles de "
            "référence calculées"
        ),
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=DEFAULT_REPEATS,
        help="Nombre de répétitions par algorithme et par taille",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Graine utilisée pour générer des tableaux aléatoires reproductibles",
    )
    return parser.parse_args(argv)


def generate_random_values(size: int, *, seed: int) -> list[int]:
    rng = Random(seed)
    upper_bound = max(10, size * 10)
    return [rng.randint(0, upper_bound) for _ in range(size)]


def benchmark_sorting_algorithms(
    *,
    sizes: list[int],
    repeats: int,
    seed: int,
) -> dict[str, list[BenchmarkPoint]]:
    return {
        name: benchmark_series(
            _build_sort_runner(sorter=sorter, seed=seed),
            sizes,
            repeats=repeats,
        )
        for name, sorter in SORTING_ALGORITHMS.items()
    }


def estimate_reference_sizes(*, repeats: int, seed: int) -> tuple[int, int, int]:
    small_size = DEFAULT_SMALL_SIZE
    baseline = benchmark_input(
        _build_sort_runner(sorter=insertion_sort, seed=seed),
        small_size,
        repeats,
    ).elapsed_ns
    medium_size = _find_size_for_target_ratio(
        baseline_ns=baseline,
        start_size=small_size * SIZE_GROWTH_FACTOR,
        target_ratio=TARGET_MEDIUM_RATIO,
        repeats=repeats,
        seed=seed,
    )
    medium_elapsed = benchmark_input(
        _build_sort_runner(sorter=insertion_sort, seed=seed),
        medium_size,
        repeats,
    ).elapsed_ns
    large_size = _find_size_for_target_ratio(
        baseline_ns=medium_elapsed,
        start_size=medium_size * SIZE_GROWTH_FACTOR,
        target_ratio=TARGET_LARGE_RATIO,
        repeats=repeats,
        seed=seed,
    )
    return small_size, medium_size, large_size


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sizes = (
        sorted(args.sizes)
        if args.sizes is not None
        else list(estimate_reference_sizes(repeats=args.repeats, seed=args.seed))
    )
    series = benchmark_sorting_algorithms(
        sizes=sizes, repeats=args.repeats, seed=args.seed
    )
    _print_summary(series, sizes=sizes)
    plot_time_comparison(series)
    plot_insertion_reference_sizes(series["insertion"])


def _build_sort_runner(*, sorter: SortFunction, seed: int) -> SortRunner:
    def run(size: int) -> list[int]:
        values = generate_random_values(size, seed=seed + size)
        return sorter(values)

    return run


def _find_size_for_target_ratio(
    *,
    baseline_ns: int,
    start_size: int,
    target_ratio: float,
    repeats: int,
    seed: int,
) -> int:
    target_ns = baseline_ns * target_ratio
    size = start_size
    runner = _build_sort_runner(sorter=insertion_sort, seed=seed)

    while size <= MAX_REFERENCE_SIZE:
        elapsed = benchmark_input(runner, size, repeats).elapsed_ns
        if elapsed >= target_ns:
            return size
        size *= SIZE_GROWTH_FACTOR

    return MAX_REFERENCE_SIZE


def _print_summary(
    series: dict[str, list[BenchmarkPoint]], *, sizes: list[int]
) -> None:
    print("[TP3 - Benchmarks]")
    print(f"Tailles retenues : {sizes}")
    header = (
        f"{'n':>8} | {'Sélection (s)':>14} | {'Insertion (s)':>14} | "
        f"{'Bulles (s)':>12} | {'Fusion (s)':>12}"
    )
    print(header)
    print("-" * len(header))

    for index, size in enumerate(sizes):
        selection_point = series["selection"][index]
        insertion_point = series["insertion"][index]
        bubble_point = series["bubble"][index]
        merge_point = series["merge"][index]
        print(
            f"{size:>8} | {selection_point.elapsed_s:>14.8f} | "
            f"{insertion_point.elapsed_s:>14.8f} | {bubble_point.elapsed_s:>12.8f} | "
            f"{merge_point.elapsed_s:>12.8f}"
        )


def plot_time_comparison(series: dict[str, list[BenchmarkPoint]]) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {
        "selection": "tab:blue",
        "insertion": "tab:orange",
        "bubble": "tab:red",
        "merge": "tab:green",
    }
    labels = {
        "selection": "Sélection",
        "insertion": "Insertion",
        "bubble": "Bulles",
        "merge": "Fusion",
    }

    for name, points in series.items():
        ax.loglog(
            [point.size for point in points],
            [point.elapsed_s for point in points],
            "o-",
            linewidth=2,
            color=colors[name],
            label=labels[name],
        )

    style_axes(
        ax,
        title="TP3 - comparaison des temps de tri",
        xlabel="Taille du tableau - échelle logarithmique",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "tp3_time_compare")
    print(f"  -> {output}")
    plt.close(fig)


def plot_insertion_reference_sizes(points: list[BenchmarkPoint]) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(
        [point.size for point in points],
        [point.elapsed_s for point in points],
        "o-",
        linewidth=2,
        color="tab:orange",
        label="Insertion",
    )
    style_axes(
        ax,
        title="TP3 - tailles de référence pour le tri par insertion",
        xlabel="Taille du tableau - échelle logarithmique",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "tp3_insertion_reference")
    print(f"  -> {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
