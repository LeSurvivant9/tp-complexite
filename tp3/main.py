import argparse

from tp3.benchmark import DEFAULT_REPEATS, DEFAULT_SEED
from tp3.benchmark import main as benchmark_main
from tp3.sorting import bubble_sort, insertion_sort, merge_sort, selection_sort

SORTING_ALGORITHMS = {
    "selection": selection_sort,
    "insertion": insertion_sort,
    "bubble": bubble_sort,
    "merge": merge_sort,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lancer les algorithmes de tri du TP3")
    parser.add_argument(
        "--algorithm",
        choices=sorted(SORTING_ALGORITHMS),
        default="merge",
        help="Algorithme de tri utilisé quand --values est fourni",
    )
    parser.add_argument(
        "--values",
        type=int,
        nargs="+",
        help="Valeurs à trier",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Lancer le mode benchmark au lieu de trier une seule liste",
    )
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        help="Tailles explicites passées au benchmark du TP3",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=DEFAULT_REPEATS,
        help="Nombre de répétitions par taille en mode benchmark",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Graine utilisée par le mode benchmark",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if args.benchmark:
        benchmark_args: list[str] = [
            "--repeats",
            str(args.repeats),
            "--seed",
            str(args.seed),
        ]
        if args.sizes is not None:
            benchmark_args.extend(["--sizes", *[str(size) for size in args.sizes]])
        benchmark_main(benchmark_args)
        return

    if args.values is None:
        raise SystemExit(
            "Use --values to sort a list or --benchmark to run the TP3 benchmarks"
        )

    sorter = SORTING_ALGORITHMS[args.algorithm]
    print(f"Algorithme : {args.algorithm}")
    print(f"Entrée     : {args.values}")
    print(f"Triée      : {sorter(args.values)}")


if __name__ == "__main__":
    main()
