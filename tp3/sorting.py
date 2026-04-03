from collections.abc import Callable

SortFunction = Callable[[list[int]], list[int]]


def selection_sort(values: list[int]) -> list[int]:
    result = values.copy()
    size = len(result)

    for left_index in range(size):
        min_index = left_index
        for right_index in range(left_index + 1, size):
            if result[right_index] < result[min_index]:
                min_index = right_index
        result[left_index], result[min_index] = result[min_index], result[left_index]

    return result


def insertion_sort(values: list[int]) -> list[int]:
    result = values.copy()

    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current

    return result


def bubble_sort(values: list[int]) -> list[int]:
    result = values.copy()
    size = len(result)

    for upper_bound in range(size - 1, 0, -1):
        swapped = False
        for index in range(upper_bound):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break

    return result


def merge_sort(values: list[int]) -> list[int]:
    if len(values) < 2:
        return values.copy()

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    return _merge_sorted_lists(left, right)


def _merge_sorted_lists(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged
