from tp1.benchmark import (
    parse_args,
    run_eratosthene_benchmark,
    run_fibonacci_benchmarks,
    run_hanoi_benchmark,
)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    parallel = not args.sequential

    print("=" * 72)
    print("TP1 - Benchmarks")
    print(f"exercice    : {args.exercise}")
    print(f"répétitions : {args.repeats}")
    print(f"parallèle   : {'oui' if parallel else 'non'}")
    print("=" * 72)
    print()

    if args.exercise in {"all", "hanoi"}:
        run_hanoi_benchmark(repeats=args.repeats, parallel=parallel)

    if args.exercise in {"all", "fibonacci"}:
        run_fibonacci_benchmarks(repeats=args.repeats, parallel=parallel)

    if args.exercise in {"all", "eratosthene"}:
        run_eratosthene_benchmark(repeats=args.repeats, parallel=parallel)


if __name__ == "__main__":
    main()
