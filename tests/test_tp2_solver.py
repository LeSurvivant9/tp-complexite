from tp2.benchmark import benchmark_random_games
from tp2.random_game import COUNTDOWN_POOL, draw_numbers, draw_target
from tp2.solver import OperationResult, build_pairs, combine_pair, solve_countdown


def test_build_pairs_returns_all_unique_pairs() -> None:
    assert build_pairs((2, 10, 100)) == [(2, 10), (2, 100), (10, 100)]


def test_combine_pair_filters_invalid_operations() -> None:
    results = combine_pair(3, 10)

    assert OperationResult(13, "(3 + 10)") in results
    assert OperationResult(30, "(3 * 10)") in results
    assert OperationResult(7, "(10 - 3)") in results
    assert all(result.value >= 0 for result in results)
    assert all(result.value != 3 for result in results)


def test_solve_countdown_returns_example_solution() -> None:
    solution = solve_countdown(120, (2, 10, 100))

    assert solution.found is True
    assert solution.value == 120
    assert solution.expression in {"((2 * 10) + 100)", "(100 + (2 * 10))"}
    assert solution.states_visited > 0


def test_solve_countdown_reports_unsolved_cases() -> None:
    solution = solve_countdown(999, (1, 1, 1))

    assert solution.found is False
    assert solution.expression is None
    assert solution.value is None
    assert solution.states_visited > 0


def test_random_draw_uses_authorized_pool() -> None:
    numbers = draw_numbers(seed=123)

    assert len(numbers) == 6
    assert all(number in COUNTDOWN_POOL for number in numbers)
    assert all(
        numbers.count(number) <= COUNTDOWN_POOL.count(number) for number in numbers
    )


def test_target_draw_stays_in_expected_range() -> None:
    assert 100 <= draw_target(seed=123) <= 999


def test_benchmark_random_games_returns_sorted_rows() -> None:
    rows = benchmark_random_games(sizes=[3, 2], games_per_size=2, seed=123)

    assert [row.size for row in rows] == [2, 3]
    assert all(row.mean_elapsed_ns >= 0 for row in rows)
    assert all(row.median_elapsed_ns >= 0 for row in rows)
    assert all(row.mean_states_visited > 0 for row in rows)
    assert all(0.0 <= row.success_rate <= 1.0 for row in rows)
