from functools import partial
from itertools import accumulate, repeat

from typing import Any


def py_logspace(
    start: int, stop: int, num: int = 5, basis: int = 10, dtype: Any = int
) -> list:
    if num < 3:
        raise ValueError
    offset = repeat((stop - start) / (num - 1), num - 1)
    # Would be cleaner with https://github.com/EntilZha/PyFunctional
    items = map(dtype, map(partial(pow, basis), accumulate(offset, initial=start)))
    # Would be more efficiant if they let us return an iterator instead of a list
    return list(items)


def main():
    pass


if __name__ == "__main__":
    main()
