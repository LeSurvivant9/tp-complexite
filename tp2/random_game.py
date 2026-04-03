from random import Random

COUNTDOWN_POOL = [
    1,
    1,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    8,
    8,
    9,
    9,
    10,
    10,
    25,
    25,
    50,
    50,
    75,
    75,
    100,
    100,
]


def draw_numbers(*, seed: int | None = None) -> tuple[int, ...]:
    rng = Random(seed)
    return tuple(rng.sample(COUNTDOWN_POOL, 6))


def draw_target(*, seed: int | None = None) -> int:
    rng = Random(seed)
    return rng.randint(100, 999)
