import multiprocessing
import statistics
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

BenchmarkFunction = Callable[[int], object]


@dataclass(frozen=True, slots=True)
class BenchmarkPoint:
    size: int
    elapsed_ns: int

    @property
    def elapsed_s(self) -> float:
        return self.elapsed_ns / 1_000_000_000


def benchmark_input(
    func: BenchmarkFunction,
    size: int,
    repeats: int = 3,
) -> BenchmarkPoint:
    if repeats < 1:
        raise ValueError("repeats must be greater than or equal to 1")

    timings = [_measure_once_ns(func, size) for _ in range(repeats)]
    median_ns = int(statistics.median(timings))
    return BenchmarkPoint(size=size, elapsed_ns=median_ns)


def benchmark_series(
    func: BenchmarkFunction,
    sizes: Iterable[int],
    repeats: int = 3,
    *,
    parallel: bool = False,
    processes: int | None = None,
) -> list[BenchmarkPoint]:
    sizes_list = list(sizes)
    if parallel and len(sizes_list) > 1:
        with multiprocessing.Pool(processes=processes) as pool:
            points = pool.map(
                _benchmark_worker,
                [(func, size, repeats) for size in sizes_list],
            )
    else:
        points = [benchmark_input(func, size, repeats) for size in sizes_list]

    return sorted(points, key=lambda point: point.size)


def _measure_once_ns(func: BenchmarkFunction, size: int) -> int:
    start = time.perf_counter_ns()
    func(size)
    return time.perf_counter_ns() - start


def _benchmark_worker(args: tuple[BenchmarkFunction, int, int]) -> BenchmarkPoint:
    func, size, repeats = args
    return benchmark_input(func, size, repeats)
