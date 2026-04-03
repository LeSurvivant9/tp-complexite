from collections.abc import Callable

import pytest

from tp3.benchmark import benchmark_sorting_algorithms, generate_random_values
from tp3.sorting import bubble_sort, insertion_sort, merge_sort, selection_sort

Sorter = Callable[[list[int]], list[int]]


@pytest.mark.parametrize(
    ("sorter", "values", "expected"),
    [
        (selection_sort, [5, 2, 4, 1, 3], [1, 2, 3, 4, 5]),
        (insertion_sort, [5, 2, 4, 1, 3], [1, 2, 3, 4, 5]),
        (bubble_sort, [5, 2, 4, 1, 3], [1, 2, 3, 4, 5]),
        (merge_sort, [5, 2, 4, 1, 3], [1, 2, 3, 4, 5]),
    ],
)
def test_sorting_algorithms_return_sorted_copy(
    sorter: Sorter,
    values: list[int],
    expected: list[int],
) -> None:
    original = values.copy()

    result = sorter(values)

    assert result == expected
    assert values == original


@pytest.mark.parametrize(
    "sorter",
    [selection_sort, insertion_sort, bubble_sort, merge_sort],
)
def test_sorting_algorithms_handle_duplicates(sorter: Sorter) -> None:
    assert sorter([4, 1, 4, 2, 2, 3]) == [1, 2, 2, 3, 4, 4]


@pytest.mark.parametrize(
    "sorter",
    [selection_sort, insertion_sort, bubble_sort, merge_sort],
)
def test_sorting_algorithms_handle_empty_and_singleton(sorter: Sorter) -> None:
    assert sorter([]) == []
    assert sorter([7]) == [7]


def test_generate_random_values_is_reproducible() -> None:
    assert generate_random_values(6, seed=123) == generate_random_values(6, seed=123)


def test_benchmark_sorting_algorithms_returns_sorted_series() -> None:
    series = benchmark_sorting_algorithms(sizes=[8, 4], repeats=1, seed=123)

    assert set(series) == {"selection", "insertion", "bubble", "merge"}
    for points in series.values():
        assert [point.size for point in points] == [4, 8]
        assert all(point.elapsed_ns > 0 for point in points)
