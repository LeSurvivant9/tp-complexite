import argparse

from tp2.benchmark import main as benchmark_main
from tp2.random_game import draw_numbers, draw_target
from tp2.solver import solve_countdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Résoudre Le compte est bon")
    parser.add_argument("--target", type=int, help="Valeur cible à atteindre")
    parser.add_argument(
        "--numbers",
        type=int,
        nargs="+",
        help="Nombres disponibles pour atteindre la cible",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Tirer une cible aléatoire et six plaques aléatoires",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Lancer les benchmarks du TP2 au lieu de résoudre une seule partie",
    )
    parser.add_argument(
        "--seed", type=int, help="Graine pour le mode aléatoire et les benchmarks"
    )
    parser.add_argument(
        "--games-per-size",
        type=int,
        default=25,
        help="Nombre de parties aléatoires par taille quand --benchmark est utilisé",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=6,
        help="Nombre maximal de plaques utilisées quand --benchmark est utilisé",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if args.benchmark:
        benchmark_args = [
            "--games-per-size",
            str(args.games_per_size),
            "--max-size",
            str(args.max_size),
        ]
        if args.seed is not None:
            benchmark_args.extend(["--seed", str(args.seed)])
        benchmark_main(benchmark_args)
        return

    if args.random:
        numbers = draw_numbers(seed=args.seed)
        target = draw_target(seed=None if args.seed is None else args.seed + 1)
    else:
        if args.target is None or args.numbers is None:
            raise SystemExit(
                "Utilisez --random ou fournissez à la fois --target et --numbers"
            )
        numbers = tuple(args.numbers)
        target = args.target

    solution = solve_countdown(target, numbers)

    print(f"Cible   : {target}")
    print(f"Plaques : {list(numbers)}")
    print(f"États   : {solution.states_visited}")
    if solution.found:
        print(f"Solution: {solution.expression} = {solution.value}")
        return
    print("Solution: aucune solution exacte trouvée")


if __name__ == "__main__":
    main()
