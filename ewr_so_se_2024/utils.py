"""
This module contains utility functions and classes for command-line interface (CLI) options 
and Matplotlib compatibility adjustments.
"""

import click


class NotRequiredIf(click.Option):
    """
    A custom Click option class that makes an option mutually exclusive with another option.

    This class extends Click's Option to add the functionality where an option becomes
    not required if another specified option is present.

    Attributes:
        not_required_if (str): The name of the option that, if present,
                               makes this option not required.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the NotRequiredIf option.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Must include 'not_required_if'.
        """
        self.not_required_if = kwargs.pop("not_required_if")
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "\b\n"
            + f"NOTE: This argument is mutually exclusive with {self.not_required_if}"
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        """
        Handles the parse result for the option.

        This method checks if both the mutually exclusive options are present and raises a
        UsageError if so.

        Args:
            ctx (click.Context): The Click context.
            opts (dict): The parsed options.
            args (list): The remaining arguments.

        Returns:
            The result of the superclass's handle_parse_result method.

        Raises:
            click.UsageError: If both mutually exclusive options are present.
        """
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    f"Illegal usage: `{self.name}` is mutually exclusive with \
                    `{self.not_required_if}`"
                )
            self.prompt = None

        return super().handle_parse_result(ctx, opts, args)


def tikzplotlib_fix_ncols(obj):
    """
    Recursively fixes the '_ncols' attribute in Matplotlib objects for compatibility with
    tikzplotlib.

    Matplotlib 3.6 renamed the legend's '_ncol' attribute to '_ncols', which breaks tikzplotlib.
    This function renames '_ncols' back to '_ncol' in the given object and all its children.

    Args:
        obj: A Matplotlib object, typically a figure or axis, to be fixed.
    """
    if hasattr(obj, "_ncols"):
        # pylint: disable=protected-access
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)
