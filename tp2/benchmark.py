"""Benchmarks for TP2 countdown solver.

Usage:
    uv run python -m tp2.benchmark
    uv run python tp2/benchmark.py
"""

import argparse
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from tp2.random_game import COUNTDOWN_POOL, draw_target  # noqa: E402
from tp2.solver import solve_countdown  # noqa: E402
from utils.plotting import save_figure, style_axes  # noqa: E402

DEFAULT_SIZES: Final[list[int]] = [2, 3, 4, 5, 6]
DEFAULT_GAMES_PER_SIZE: Final[int] = 25


@dataclass(frozen=True, slots=True)
class CountdownBenchmarkRow:
    size: int
    mean_elapsed_ns: int
    median_elapsed_ns: int
    mean_states_visited: float
    success_rate: float

    @property
    def mean_elapsed_s(self) -> float:
        return self.mean_elapsed_ns / 1_000_000_000

    @property
    def median_elapsed_s(self) -> float:
        return self.median_elapsed_ns / 1_000_000_000


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lancer les benchmarks du TP2")
    parser.add_argument(
        "--games-per-size",
        type=int,
        default=DEFAULT_GAMES_PER_SIZE,
        help="Nombre de parties aléatoires générées pour chaque taille d'entrée",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=6,
        help="Nombre maximal de plaques utilisées pendant le benchmark",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=123,
        help="Graine utilisée pour rendre les benchmarks reproductibles",
    )
    return parser.parse_args(argv)


def benchmark_random_games(
    *,
    sizes: list[int],
    games_per_size: int,
    seed: int,
) -> list[CountdownBenchmarkRow]:
    rows: list[CountdownBenchmarkRow] = []
    for size in sorted(sizes):
        elapsed_values: list[int] = []
        states_visited_values: list[int] = []
        solved_count = 0

        for game_index in range(games_per_size):
            numbers = _draw_numbers_for_size(
                size=size, seed=seed + (size * 1_000) + game_index
            )
            target = draw_target(seed=seed + (size * 10_000) + game_index)

            start = time.perf_counter_ns()
            solution = solve_countdown(target, numbers)
            elapsed_ns = time.perf_counter_ns() - start

            elapsed_values.append(elapsed_ns)
            states_visited_values.append(solution.states_visited)
            solved_count += int(solution.found)

        rows.append(
            CountdownBenchmarkRow(
                size=size,
                mean_elapsed_ns=int(statistics.fmean(elapsed_values)),
                median_elapsed_ns=int(statistics.median(elapsed_values)),
                mean_states_visited=statistics.fmean(states_visited_values),
                success_rate=solved_count / games_per_size,
            )
        )

    return rows


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sizes = [size for size in DEFAULT_SIZES if size <= args.max_size]
    rows = benchmark_random_games(
        sizes=sizes,
        games_per_size=args.games_per_size,
        seed=args.seed,
    )
    _print_rows(rows)
    plot_benchmark_time(rows)
    plot_benchmark_states(rows)


def _draw_numbers_for_size(*, size: int, seed: int) -> tuple[int, ...]:
    from random import Random

    if size < 2 or size > 6:
        raise ValueError("size must be between 2 and 6")

    rng = Random(seed)
    return tuple(rng.sample(COUNTDOWN_POOL, size))


def _print_rows(rows: list[CountdownBenchmarkRow]) -> None:
    header = (
        f"{'n':>5} | {'Temps moyen (s)':>16} | {'Temps médian (s)':>17} | "
        f"{'États moyens':>13} | {'Taux succès':>11}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row.size:>5} | {row.mean_elapsed_s:>16.8f} | "
            f"{row.median_elapsed_s:>17.8f} | {row.mean_states_visited:>13.2f} | "
            f"{row.success_rate:>11.2%}"
        )


def plot_benchmark_time(rows: list[CountdownBenchmarkRow]) -> None:
    sizes = [row.size for row in rows]
    mean_times = [row.mean_elapsed_s for row in rows]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(
        sizes, mean_times, "o-", linewidth=2, color="tab:blue", label="Temps moyen"
    )
    style_axes(
        ax,
        title="TP2 - Temps moyen de résolution",
        xlabel="n",
        ylabel="Temps (s) - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "tp2_time")
    print(f"  -> {output}")
    plt.close(fig)


def plot_benchmark_states(rows: list[CountdownBenchmarkRow]) -> None:
    sizes = np.array([row.size for row in rows], dtype=float)
    states = [row.mean_states_visited for row in rows]
    trend = [worst_case_state_count(int(size)) for size in sizes]
    scale = states[0] / trend[0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.semilogy(
        sizes, states, "o-", linewidth=2, color="tab:orange", label="États moyens"
    )
    ax.semilogy(
        sizes,
        [scale * value for value in trend],
        "--",
        color="gray",
        alpha=0.7,
        label="Tendance pire cas",
    )
    style_axes(
        ax,
        title="TP2 - États explorés",
        xlabel="n",
        ylabel="Nombre d'états - échelle logarithmique",
    )
    fig.tight_layout()
    output = save_figure(fig, "tp2_states")
    print(f"  -> {output}")
    plt.close(fig)


def worst_case_state_count(size: int) -> int:
    if size < 1:
        raise ValueError("size must be greater than or equal to 1")
    if size == 1:
        return 1
    return 1 + (2 * size * (size - 1) * worst_case_state_count(size - 1))


if __name__ == "__main__":
    main()
