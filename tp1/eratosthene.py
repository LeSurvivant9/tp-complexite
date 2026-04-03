import math


def sieve_eratosthenes(limit: int) -> list[int]:
    """Return all prime numbers less than or equal to ``limit``."""
    if limit < 0:
        raise ValueError("limit must be greater than or equal to 0")
    if limit < 2:
        return []

    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"

    for candidate in range(2, math.isqrt(limit) + 1):
        if not is_prime[candidate]:
            continue

        start = candidate * candidate
        count = ((limit - start) // candidate) + 1
        is_prime[start : limit + 1 : candidate] = b"\x00" * count

    return [number for number in range(2, limit + 1) if is_prime[number]]


def prime_count_up_to(limit: int) -> int:
    """Return the number of prime numbers less than or equal to ``limit``."""
    return len(sieve_eratosthenes(limit))
