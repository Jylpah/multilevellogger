import pytest  # type: ignore
from pathlib import Path
import logging
from typer import Typer, Option
from click.testing import Result
from typer.testing import CliRunner
from typing import Annotated, Optional

from multilevelformatter import MultilevelFormatter


logger = logging.getLogger(__name__)
error = logger.error
warning = logger.warning
message = logger.message  # type: ignore
verbose = logger.info
debug = logger.debug

app = Typer()


@app.callback(invoke_without_command=True)
def cli(
    print_verbose: Annotated[
        bool,
        Option(
            "--verbose",
            "-v",
            show_default=False,
            help="verbose logging",
        ),
    ] = False,
    print_warning: Annotated[
        bool,
        Option(
            "--warning",
            show_default=False,
            help="warnings only",
        ),
    ] = False,
    print_debug: Annotated[
        bool,
        Option(
            "--debug",
            show_default=False,
            help="debug logging",
        ),
    ] = False,
    print_silent: Annotated[
        bool,
        Option(
            "--silent",
            show_default=False,
            help="silent logging",
        ),
    ] = False,
    log: Annotated[Optional[Path], Option(help="log to FILE", metavar="FILE")] = None,
) -> None:
    """MultilevelFormatter demo"""
    global logger

    try:
        LOG_LEVEL: int = logging.MESSAGE  # type: ignore
        if print_verbose:
            LOG_LEVEL = logging.INFO
        elif print_warning:
            LOG_LEVEL = logging.WARNING
        elif print_debug:
            LOG_LEVEL = logging.DEBUG
        elif print_silent:
            LOG_LEVEL = logging.ERROR
        MultilevelFormatter.setDefaults(logger, log_file=log)
        logger.setLevel(LOG_LEVEL)
    except Exception as err:
        error(f"{err}")
    verbose("verbose")
    message("standard")
    warning("warning")
    error("error")
    debug("debug")


@pytest.mark.parametrize(
    "args,lines",
    [
        ([], 3),
        (["--verbose"], 4),
        (["--debug"], 5),
        (["--warning"], 2),
        (["--silent"], 1),
    ],
)
def test_1_multilevelformatter(args: list[str], lines: int) -> None:
    result: Result = CliRunner().invoke(app, [*args])

    assert result.exit_code == 0, f"test failed {' '.join(args)}"

    lines_output: int = len(result.output.splitlines())
    assert (
        lines_output == lines
    ) is not None, f"incorrect output {lines_output} != {lines}"

    if len(args) > 0:
        param: str = args[0][2:]
        if param != "silent":
            assert (
                result.output.find(param) >= 0
            ), f"no expected output found: '{param}'"
    else:
        assert (
            result.output.find("standard") >= 0
        ), "no expected output found: 'standard'"
    assert result.output.find("error") >= 0, "no expected output found: 'error'"


if __name__ == "__main__":
    app()
