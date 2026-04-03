from collections.abc import Callable

MoveCallback = Callable[[str, str], None]


def _validate_disk_count(n: int) -> None:
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")


def hanoi(
    n: int,
    source: str = "A",
    auxiliary: str = "B",
    target: str = "C",
    emit_move: MoveCallback | None = None,
) -> None:
    """Solve the Towers of Hanoi problem for ``n`` disks."""
    _validate_disk_count(n)
    _hanoi_recursive(n, source, auxiliary, target, emit_move)


def _hanoi_recursive(
    n: int,
    source: str,
    auxiliary: str,
    target: str,
    emit_move: MoveCallback | None,
) -> None:
    if n == 1:
        if emit_move is not None:
            emit_move(source, target)
        return

    _hanoi_recursive(n - 1, source, target, auxiliary, emit_move)
    if emit_move is not None:
        emit_move(source, target)
    _hanoi_recursive(n - 1, auxiliary, source, target, emit_move)


def hanoi_call_count(n: int) -> int:
    """Return the number of recursive calls performed by ``hanoi(n)``."""
    _validate_disk_count(n)
    return _hanoi_call_count_recursive(n)


def _hanoi_call_count_recursive(n: int) -> int:
    if n == 1:
        return 1
    return 1 + _hanoi_call_count_recursive(n - 1) + _hanoi_call_count_recursive(n - 1)


def hanoi_theoretical_calls(n: int) -> int:
    """Return the exact closed-form number of recursive calls."""
    _validate_disk_count(n)
    return (1 << n) - 1
