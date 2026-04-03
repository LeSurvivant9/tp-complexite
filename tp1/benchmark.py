"""Benchmarks for TP1 algorithms.

Usage:
    uv run python -m tp1.benchmark
    uv run python tp1/benchmark.py
"""

import argparse
import sys
from pathlib import Path
from typing import Final

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from tp1.eratosthene import prime_count_up_to, sieve_eratosthenes  # noqa: E402
from tp1.fibonacci import (  # noqa: E402
    fib_fast_doubling,
    fib_iterative,
    fib_recursive,
)
from tp1.hanoi import hanoi_call_count, hanoi_theoretical_calls  # noqa: E402
from utils.benchmarking import BenchmarkPoint, benchmark_series  # noqa: E402
from utils.plotting import save_figure, style_axes  # noqa: E402

DEFAULT_REPEATS: Final[int] = 3
HANOI_VALUES: Final[list[int]] = [1, 5, 10, 15, 20, 25, 30]
FIBONACCI_COMPARE_VALUES: Final[list[int]] = [0, 1, 2, 5, 10, 15, 20, 25, 30]
FIBONACCI_SCALING_VALUES: Final[list[int]] = [
    100,
    500,
    1_000,
    2_500,
    5_000,
    10_000,
]
ERATOSTHENE_VALUES: Final[list[int]] = [
    100,
    500,
    1_000,
    5_000,
    10_000,
    50_000,
    100_000,
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lancer les benchmarks du TP1")
    parser.add_argument(
        "--exercise",
        choices=["all", "hanoi", "fibonacci", "eratosthene"],
        default="all",
        help="Exercice à mesurer",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=DEFAULT_REPEATS,
        help="Nombre de répétitions par taille d'entrée",
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Désactiver le parallélisme entre tailles d'entrée indépendantes",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    from tp1.main import main as tp1_main

    tp1_main(argv)


def run_hanoi_benchmark(*, repeats: int, parallel: bool) -> None:
    print("[Hanoi]")
    points = benchmark_series(
        hanoi_call_count,
        HANOI_VALUES,
        repeats=repeats,
        parallel=parallel,
    )
    _print_hanoi_table(points)
    plot_hanoi_time(points)
    plot_hanoi_calls(points)
    print()


def run_fibonacci_benchmarks(*, repeats: int, parallel: bool) -> None:
    print("[Fibonacci]")
    compare_points = {
        "Itératif": benchmark_series(
            fib_iterative,
            FIBONACCI_COMPARE_VALUES,
            repeats=repeats,
            parallel=parallel,
        ),
        "Récursif": benchmark_series(
            fib_recursive,
            FIBONACCI_COMPARE_VALUES,
            repeats=repeats,
            parallel=parallel,
        ),
        "Logarithmique": benchmark_series(
            fib_fast_doubling,
            FIBONACCI_COMPARE_VALUES,
            repeats=repeats,
            parallel=parallel,
        ),
    }
    scaling_points = {
        "Itératif": benchmark_series(
            fib_iterative,
            FIBONACCI_SCALING_VALUES,
            repeats=repeats,
            parallel=parallel,
        ),
        "Logarithmique": benchmark_series(
            fib_fast_doubling,
            FIBONACCI_SCALING_VALUES,
            repeats=repeats,
            parallel=parallel,
        ),
    }
    _print_fibonacci_table(compare_points)
    plot_fibonacci_compare(compare_points)
    plot_fibonacci_scaling(scaling_points)
    print()


def run_eratosthene_benchmark(*, repeats: int, parallel: bool) -> None:
    print("[Crible d'Ératosthène]")
    points = benchmark_series(
        sieve_eratosthenes,
        ERATOSTHENE_VALUES,
        repeats=repeats,
        parallel=parallel,
    )
    _print_eratosthene_table(points)
    plot_eratosthene_time(points)
    print()


def _print_hanoi_table(points: list[BenchmarkPoint]) -> None:
    header = (
        f"{'n':>5} | {'Appels mesurés':>16} | {'Théorique':>16} | "
        f"{'Temps médian (s)':>18}"
    )
    print(header)
    print("-" * len(header))
    for point in points:
        calls = hanoi_call_count(point.size)
        theoretical = hanoi_theoretical_calls(point.size)
        print(
            f"{point.size:>5} | {calls:>16} | {theoretical:>16} | "
            f"{point.elapsed_s:>18.8f}"
        )


def _print_fibonacci_table(points_by_label: dict[str, list[BenchmarkPoint]]) -> None:
    labels = ["Itératif", "Récursif", "Logarithmique"]
    header = (
        f"{'n':>5} | {'Itératif (s)':>14} | {'Récursif (s)':>14} | "
        f"{'Logarithmique (s)':>19}"
    )
    print(header)
    print("-" * len(header))

    point_maps = {
        label: {point.size: point for point in points}
        for label, points in points_by_label.items()
    }
    for size in FIBONACCI_COMPARE_VALUES:
        row = [point_maps[label][size].elapsed_s for label in labels]
        print(f"{size:>5} | {row[0]:>14.8f} | {row[1]:>14.8f} | {row[2]:>19.8f}")


def _print_eratosthene_table(points: list[BenchmarkPoint]) -> None:
    header = (
        f"{'N':>8} | {'Nb premiers':>12} | {'Temps médian (s)':>18} | "
        f"{'N log log N':>14}"
    )
    print(header)
    print("-" * len(header))
    for point in points:
        theoretical = (
            point.size * np.log(np.log(point.size)) if point.size >= 3 else 0.0
        )
        prime_count = prime_count_up_to(point.size)
        print(
            f"{point.size:>8} | {prime_count:>12} | {point.elapsed_s:>18.8f} | "
            f"{theoretical:>14.2f}"
        )


def plot_hanoi_time(points: list[BenchmarkPoint]) -> None:
    ns = [point.size for point in points]
    times = [point.elapsed_s for point in points]
    n_curve = np.linspace(float(min(ns)), float(max(ns)), 400)
    scale = times[0] / (2.0 ** ns[0])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(ns, times, "o-", linewidth=2, color="tab:blue", label="Temps mesuré")
    ax.semilogy(
        n_curve,
        scale * (2.0**n_curve),
        "--",
        color="gray",
        alpha=0.7,
        label=r"$O(2^n)$",
    )
    style_axes(
        ax,
        title="Temps d'exécution de Hanoï(n)",
        xlabel="n",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "hanoi_time")
    print(f"  -> {output}")
    plt.close(fig)


def plot_hanoi_calls(points: list[BenchmarkPoint]) -> None:
    ns = [point.size for point in points]
    calls = [hanoi_call_count(point.size) for point in points]
    n_curve = np.linspace(float(min(ns)), float(max(ns)), 400)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(
        ns,
        calls,
        "o-",
        linewidth=2,
        color="tab:orange",
        label="Appels récursifs mesurés",
    )
    ax.semilogy(
        n_curve,
        (2.0**n_curve) - 1,
        "--",
        color="gray",
        alpha=0.7,
        label=r"$2^n - 1$",
    )
    style_axes(
        ax,
        title="Nombre d'appels récursifs de Hanoï(n)",
        xlabel="n",
        ylabel="Appels récursifs - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "hanoi_calls")
    print(f"  -> {output}")
    plt.close(fig)


def plot_fibonacci_compare(points_by_label: dict[str, list[BenchmarkPoint]]) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {
        "Itératif": "tab:blue",
        "Récursif": "tab:red",
        "Logarithmique": "tab:green",
    }

    for label, points in points_by_label.items():
        ax.semilogy(
            [point.size for point in points],
            [point.elapsed_s for point in points],
            "o-",
            linewidth=2,
            color=colors[label],
            label=label,
        )

    style_axes(
        ax,
        title="Fibonacci - comparaison des approches",
        xlabel="n",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "fibonacci_time_compare")
    print(f"  -> {output}")
    plt.close(fig)


def plot_fibonacci_scaling(points_by_label: dict[str, list[BenchmarkPoint]]) -> None:
    iterative_points = points_by_label["Itératif"]
    logarithmic_points = points_by_label["Logarithmique"]
    ns = [point.size for point in iterative_points]
    time_iterative = [point.elapsed_s for point in iterative_points]
    time_logarithmic = [point.elapsed_s for point in logarithmic_points]
    n_curve = np.array(ns, dtype=float)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(
        ns,
        time_iterative,
        "o-",
        linewidth=2,
        color="tab:blue",
        label="Itératif",
    )
    ax.loglog(
        ns,
        time_logarithmic,
        "o-",
        linewidth=2,
        color="tab:green",
        label="Logarithmique",
    )

    iterative_scale = time_iterative[0] / ns[0]
    logarithmic_scale = time_logarithmic[0] / np.log2(ns[0])
    ax.loglog(
        n_curve,
        iterative_scale * n_curve,
        "--",
        color="tab:blue",
        alpha=0.5,
        label=r"Tendance $O(n)$",
    )
    ax.loglog(
        n_curve,
        logarithmic_scale * np.log2(n_curve),
        "--",
        color="tab:green",
        alpha=0.5,
        label=r"Tendance $O(\log n)$",
    )

    style_axes(
        ax,
        title="Fibonacci - grande échelle",
        xlabel="n - échelle logarithmique",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "fibonacci_time_scaling")
    print(f"  -> {output}")
    plt.close(fig)


def plot_eratosthene_time(points: list[BenchmarkPoint]) -> None:
    ns = [point.size for point in points]
    times = [point.elapsed_s for point in points]
    n_curve = np.array(ns, dtype=float)
    trend = n_curve * np.log(np.log(n_curve))
    scale = times[0] / trend[0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(
        ns,
        times,
        "o-",
        linewidth=2,
        color="tab:purple",
        label="Temps mesuré",
    )
    ax.loglog(
        n_curve,
        scale * trend,
        "--",
        color="gray",
        alpha=0.7,
        label=r"Tendance $O(n \log \log n)$",
    )
    style_axes(
        ax,
        title="Crible d'Ératosthène - temps d'exécution",
        xlabel="N - échelle logarithmique",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "eratosthene_time")
    print(f"  -> {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
