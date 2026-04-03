import pytest

from tp1.eratosthene import prime_count_up_to, sieve_eratosthenes
from tp1.fibonacci import fib_fast_doubling, fib_iterative, fib_recursive
from tp1.hanoi import hanoi_call_count, hanoi_theoretical_calls
from utils.benchmarking import BenchmarkPoint, benchmark_series


def test_hanoi_call_count_matches_theory() -> None:
    assert hanoi_call_count(1) == 1
    assert hanoi_call_count(4) == 15
    assert hanoi_call_count(4) == hanoi_theoretical_calls(4)


def test_fibonacci_variants_return_same_value() -> None:
    expected = 55
    assert fib_iterative(10) == expected
    assert fib_recursive(10) == expected
    assert fib_fast_doubling(10) == expected


def test_fibonacci_rejects_negative_inputs() -> None:
    with pytest.raises(ValueError):
        fib_iterative(-1)

    with pytest.raises(ValueError):
        fib_recursive(-1)

    with pytest.raises(ValueError):
        fib_fast_doubling(-1)


def test_sieve_returns_primes_up_to_limit() -> None:
    assert sieve_eratosthenes(1) == []
    assert sieve_eratosthenes(10) == [2, 3, 5, 7]
    assert prime_count_up_to(30) == 10


def test_benchmark_series_returns_sorted_points() -> None:
    points = benchmark_series(fib_iterative, [5, 1, 3], repeats=2)

    assert [point.size for point in points] == [1, 3, 5]
    assert all(point.elapsed_ns > 0 for point in points)
    assert all(isinstance(point, BenchmarkPoint) for point in points)
    assert points[0].elapsed_s > 0.0
