"""
This module provides functions for reading, saving, and loading data.

Usage Examples:
---------------

Example usage of `read_number`:

    prompt = "Please enter an integer x with 3 <= x <= 7: "
    input_number = read_number(prompt, int, 3.0, 7.0)
    print(f"Entered number: {input_number}")

Example usage of `save_data`:

    output_path = "save.json"
    save_data(output_path, [1, 2, 3], 4, 3, 4)

Example usage of `load_data`:

    sequence_elements, (param_a, param_b, param_c) = load_data("save.json")
    print(f"Sequence elements: {sequence_elements}")
    print(f"Parameters: {param_a}, {param_b}, {param_c}")
"""

# Enable postponed evaluation of type annotations
from __future__ import annotations

import json

from typing import TYPE_CHECKING, Any, Callable, List, Tuple, TypeVar

# Type hints for type checking (only used for static type checkers)
if TYPE_CHECKING:
    from _typeshed import FileDescriptorOrPath

T = TypeVar("T", bound=Callable)

# Exposing symbols to be imported from this module
__all__ = ["read_number", "save_data", "load_data"]

VERSION = 1.1


def read_number(
    question: str,
    data_type: T,
    lower_limit: float = float("-inf"),
    upper_limit: float = float("inf"),
) -> T:
    """
    Repeatedly prompts the user to enter a number that matches the specified data
    type and is within the given limits.

    The following flowchart explains the rough function flow:

    ![Function Flowchart](./read_number.png)

    Args:
        question: The question to ask the user.
        data_type: The desired data type (e.g., `int`, `float`).
        lower_limit: The lower limit.
        upper_limit: The upper limit.

    Returns:
        The user's input in the desired data type.

    Raises:
        ValueError: If the user decides not to retry after an invalid input.
    """
    while True:
        answer = input(question)
        try:
            input_value = data_type(answer)
            if lower_limit <= input_value <= upper_limit:
                return input_value
            print(
                f"Your input is not within the limits {lower_limit} and {upper_limit}."
            )
        except ValueError:
            print(f"Your input does not match the data type {data_type}.")
        retry = input("Do you want to try again (Y/n): ")
        if retry.lower() == "n":
            raise ValueError("Invalid input and the user aborted the retry attempt.")


def save_data(output_path: FileDescriptorOrPath, sequence: List[Any], *parameters: Any):
    """
    Saves the sequence elements and input parameters to a file.

    Args:
        output_path: The path where the data should be saved.
        sequence: A list of sequence elements.
        *parameters: Any number of additional parameters.
    """
    data = {"sequence": sequence, "parameters": parameters, "version": VERSION}
    with open(output_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data(path: FileDescriptorOrPath) -> Tuple[List[Any], Tuple[Any, ...]]:
    """
    Loads data from a file.

    Args:
        path: The file path of the file to be loaded.

    Returns:
        A tuple consisting of the list of sequence elements and a tuple of parameters.
    """
    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    if data.get("version") != VERSION:
        raise ValueError(
            f"Invalid version: expected {VERSION}, but got {data.get('version')}"
        )

    if "sequence" not in data:
        raise KeyError("Missing 'sequence' key in the data")
    if "parameters" not in data:
        raise KeyError("Missing 'parameters' key in the data")

    return data["sequence"], tuple(data["parameters"])


def main():
    """
    Main function to demonstrate the usage of `read_number`, `save_data`, and `load_data`.
    """
    # This is imported here outside of the top level imports because it is only used by the
    # example and thus not required by the code above.
    # pylint: disable=import-outside-toplevel
    import numpy
    import sys

    # Example usage of read_number
    prompt = "Please enter an integer x with 3 <= x <= 7: "
    try:
        input_number = read_number(prompt, int, 3.0, 7.0)
        print(f"Entered number: {input_number}")
    except ValueError:
        print("User did not provide a valid number (exiting).")
        sys.exit(1)

    # Example usage of save_data
    example_save_file = "save.json"
    print(f"Saving entered number and random sequence into `{example_save_file}`")
    save_data(example_save_file, list(numpy.random.rand(10)), input_number)

    # Example usage of load_data
    print(f"Loading data from `{example_save_file}`")
    random_sequence, (input_number, *_) = load_data(example_save_file)
    print(f"Loaded random sequence: {random_sequence}")
    print(f"Loaded Input number: {input_number}")


if __name__ == "__main__":
    main()
