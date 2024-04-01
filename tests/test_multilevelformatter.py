import pytest  # type: ignore
from pathlib import Path
import logging
from typer import Typer, Option  # type: ignore
from click.testing import Result
from typer.testing import CliRunner  # type: ignore
from typing import Annotated, Optional

from multilevelformatter import MultilevelFormatter, addLoggingLevelMessage, MESSAGE

# from icecream import ic  # type: ignore

logger = logging.getLogger(__name__)
error = logger.error
message = logger.warning
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
    # try:
    #     addLoggingLevelMessage()

    # except AttributeError:
    #     pass
    try:
        LOG_LEVEL: int = logging.WARNING
        if print_verbose:
            LOG_LEVEL = logging.INFO
        elif print_debug:
            LOG_LEVEL = logging.DEBUG
        elif print_silent:
            LOG_LEVEL = logging.ERROR
        MultilevelFormatter.setDefaults(logger, log_file=log, level=LOG_LEVEL)
    except Exception as err:
        error(f"{err}")

    verbose("verbose")
    message("standard")
    error("error")
    debug("debug")


@pytest.mark.parametrize(
    "args,lines",
    [
        ([], 2),
        (["--verbose"], 3),
        (["--debug"], 4),
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
        ), f"no expected output found: 'standard': {result.output}"
    assert result.output.find("error") >= 0, "no expected output found: 'error'"


def test_2_addLoggingLevelMessage() -> None:
    addLoggingLevelMessage()
    try:
        logging.message("test message()")  # type: ignore
        assert True, "logging.message() worked as it should"
    except Exception as err:
        assert False, f"could not add logging.message(): {err}"

    assert logging.MESSAGE == MESSAGE, "Added logging.MESSAGE level == 25"  # type: ignore


if __name__ == "__main__":
    app()
