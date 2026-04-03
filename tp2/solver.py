from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OperationResult:
    value: int
    expression: str


@dataclass(frozen=True, slots=True)
class CountdownSolution:
    found: bool
    value: int | None
    expression: str | None
    states_visited: int


def build_pairs(values: tuple[int, ...]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for left_index in range(len(values) - 1):
        for right_index in range(left_index + 1, len(values)):
            pairs.append((values[left_index], values[right_index]))
    return pairs


def combine_pair(left: int, right: int) -> list[OperationResult]:
    results = {
        OperationResult(left + right, f"({left} + {right})"),
        OperationResult(left * right, f"({left} * {right})"),
    }

    high = max(left, right)
    low = min(left, right)
    if high > low:
        results.add(OperationResult(high - low, f"({high} - {low})"))

    if low != 0 and high % low == 0:
        results.add(OperationResult(high // low, f"({high} / {low})"))

    return sorted(results, key=lambda result: (result.value, result.expression))


def solve_countdown(target: int, numbers: tuple[int, ...]) -> CountdownSolution:
    expressions = tuple(str(number) for number in numbers)
    found, value, expression, states_visited = _search(target, numbers, expressions)
    return CountdownSolution(
        found=found,
        value=value,
        expression=expression,
        states_visited=states_visited,
    )


def _search(
    target: int,
    values: tuple[int, ...],
    expressions: tuple[str, ...],
) -> tuple[bool, int | None, str | None, int]:
    states_visited = 1

    for value, expression in zip(values, expressions, strict=True):
        if value == target:
            return True, value, expression, states_visited

    if len(values) < 2:
        return False, None, None, states_visited

    for left_index in range(len(values) - 1):
        for right_index in range(left_index + 1, len(values)):
            left_value = values[left_index]
            right_value = values[right_index]
            remaining_values = tuple(
                value
                for index, value in enumerate(values)
                if index not in {left_index, right_index}
            )
            remaining_expressions = tuple(
                expression
                for index, expression in enumerate(expressions)
                if index not in {left_index, right_index}
            )

            for result in _combine_entries(
                left_value,
                right_value,
                expressions[left_index],
                expressions[right_index],
            ):
                child_found, child_value, child_expression, child_states = _search(
                    target,
                    remaining_values + (result.value,),
                    remaining_expressions + (result.expression,),
                )
                states_visited += child_states
                if child_found:
                    return True, child_value, child_expression, states_visited

    return False, None, None, states_visited


def _combine_entries(
    left_value: int,
    right_value: int,
    left_expression: str,
    right_expression: str,
) -> list[OperationResult]:
    results = {
        OperationResult(
            left_value + right_value,
            f"({left_expression} + {right_expression})",
        ),
        OperationResult(
            left_value * right_value,
            f"({left_expression} * {right_expression})",
        ),
    }

    if left_value >= right_value and left_value - right_value > 0:
        results.add(
            OperationResult(
                left_value - right_value,
                f"({left_expression} - {right_expression})",
            )
        )
    elif right_value > left_value and right_value - left_value > 0:
        results.add(
            OperationResult(
                right_value - left_value,
                f"({right_expression} - {left_expression})",
            )
        )

    if right_value != 0 and left_value % right_value == 0:
        results.add(
            OperationResult(
                left_value // right_value,
                f"({left_expression} / {right_expression})",
            )
        )
    elif left_value != 0 and right_value % left_value == 0:
        results.add(
            OperationResult(
                right_value // left_value,
                f"({right_expression} / {left_expression})",
            )
        )

    return sorted(results, key=lambda result: (result.value, result.expression))
