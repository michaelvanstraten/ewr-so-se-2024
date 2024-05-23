# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import click


# https://stackoverflow.com/a/44349292
class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop("not_required_if")
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "\b\n"
            + f"NOTE: This argument is mutually exclusive with {self.not_required_if}"
        ).strip()
        # print(kwargs["help"])
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    # pylint: disable=line-too-long
                    f"Illegal usage: `{self.name}` is mutually exclusive with `{self.not_required_if}`"
                )
            self.prompt = None

        return super().handle_parse_result(ctx, opts, args)


# https://stackoverflow.com/a/75903189
def tikzplotlib_fix_ncols(obj):
    """
    workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, which breaks tikzplotlib
    """
    if hasattr(obj, "_ncols"):
        # pylint: disable=protected-access)
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)
