import logging
from typer import Typer, Option  # type: ignore
from typing import Annotated, Optional
from pathlib import Path
from multilevellogger import getMultiLevelLogger, VERBOSE, MESSAGE


logger = getMultiLevelLogger(__name__)
error = logger.error
message = logger.message
verbose = logger.verbose
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

    try:
        LOG_LEVEL: int = MESSAGE  # type: ignore
        if print_verbose:
            LOG_LEVEL = VERBOSE
        elif print_debug:
            LOG_LEVEL = logging.DEBUG
        elif print_silent:
            LOG_LEVEL = logging.ERROR
        logger.setLevel(LOG_LEVEL)
        if log is not None:
            logger.addFileHandler(log_file=log)

        logger.setLevel(LOG_LEVEL)
    except Exception as err:
        error(f"{err}")
    message("standard")
    verbose("verbose")
    error("error")
    debug("debug")


if __name__ == "__main__":
    app()
