import pytest

from utils.benchmarking import BenchmarkPoint, benchmark_series


def test_benchmark_series_returns_sorted_points() -> None:
    points = benchmark_series(lambda n: n * 2, [5, 1, 3], repeats=2)

    assert [point.size for point in points] == [1, 3, 5]
    assert all(point.elapsed_ns > 0 for point in points)
    assert all(isinstance(point, BenchmarkPoint) for point in points)
    assert points[0].elapsed_s > 0.0


def test_benchmark_series_rejects_invalid_repeat_count() -> None:
    with pytest.raises(ValueError):
        benchmark_series(lambda n: n, [1, 2, 3], repeats=0)
