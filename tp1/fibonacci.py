def _validate_index(n: int) -> None:
    if n < 0:
        raise ValueError("n must be greater than or equal to 0")


def fib_iterative(n: int) -> int:
    """Return the n-th Fibonacci number using an iterative algorithm."""
    _validate_index(n)
    if n < 2:
        return n

    previous = 0
    current = 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


def fib_recursive(n: int) -> int:
    """Return the n-th Fibonacci number using naive recursion."""
    _validate_index(n)
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_fast_doubling(n: int) -> int:
    """Return the n-th Fibonacci number using fast doubling."""
    _validate_index(n)
    return _fib_fast_doubling_pair(n)[0]


def _fib_fast_doubling_pair(n: int) -> tuple[int, int]:
    if n == 0:
        return 0, 1

    a, b = _fib_fast_doubling_pair(n // 2)
    c = a * ((2 * b) - a)
    d = (a * a) + (b * b)

    if n % 2 == 0:
        return c, d
    return d, c + d
