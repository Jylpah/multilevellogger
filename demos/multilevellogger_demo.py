import logging
from typer import Typer, Option  # type: ignore
from typing import Annotated, Optional
from pathlib import Path
from multilevellogger import getMultiLevelLogger, MultiLevelLogger, VERBOSE, MESSAGE


logger: MultiLevelLogger = getMultiLevelLogger(__name__)
error = logger.error
warning = logger.warning
message = logger.message
verbose = logger.verbose
info = logger.info
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
            logger.addLogFile(log_file=log)

        logger.setLevel(LOG_LEVEL)
    except Exception as err:
        error(f"{err}")
    debug("debug")
    info("info")
    message("message")
    verbose("verbose")
    warning("warning")
    error("error")


if __name__ == "__main__":
    app()
