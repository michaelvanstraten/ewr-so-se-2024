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

from __future__ import annotations

import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import FileDescriptorOrPath
    from typing import Any, Callable, List, Tuple, TypeVar

    T = TypeVar("T", bound=Callable)

__all__ = ["read_number", "save_data", "load_data"]

VERSION = 1.0


def read_number(
    question: str,
    data_type: T,
    lower_limit: float = float("-inf"),
    upper_limit: float = float("inf"),
) -> T:
    """
    Prompts the user to enter a number that matches the specified data type
    and is within the given limits.

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
    # Example usage of read_number
    prompt = "Please enter an integer x with 3 <= x <= 7: "
    input_number = read_number(prompt, int, 3.0, 7.0)
    print(f"Entered number: {input_number}")

    # Example usage of save_data
    output_path = "save.json"
    save_data(output_path, [1, 2, 3], 4, 3, 4)

    # Example usage of load_data
    sequence_elements, (param_a, param_b, param_c) = load_data(output_path)
    print(f"Sequence elements: {sequence_elements}")
    print(f"Parameters: {param_a}, {param_b}, {param_c}")


if __name__ == "__main__":
    main()
