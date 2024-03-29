# MultiLevelFormatter

`MultiLevelFormatter` is a Python `logging.Formatter` that simplifies setting log formats for different log levels. Log records with level `logging.ERROR` or higher are printed to STDERR if using defaults with `MultilevelFormatter.setDefaults()`.

Importing `MultiLevelFormatter` adds MESSAGE level (`25`) to logging and an `logging.message()` method. The idea is that you can use `logging.message()` instead of `print()` and use logging levels to control verbosity. See the full example below.  


## Install

*Python 3.11 or later is required.*

```sh
pip install multilevelformatter
```

## Usage

*Please note.* If you use `mypy`, you need to add `# type: ignore` to the lines assigning `logging.message` to `message` (function) and whenever using `logging.MESSAGE` log level name. `mypy` does not recognize the modifications to the `logging` class that is done when importing `multilevelformatter`. See [mypy#5363](https://github.com/python/mypy/issues/5363) for details.

```python

logger = logging.getLogger(__name__)
error = logger.error
warning = logger.warning
# added when importing multilevelformatter
message = logging.message  # type: ignore 
verbose = logger.info
debug = logger.debug

# Not complete, does not run
def main() -> None:
    
    ...

    # assumes command line arguments have been parsed into 
    # boolean flags: arg_verbose, arg_debug, arg_silent
    
    # MultiLevelFormatter adds MESSAGE level (25) to logging
    LOG_LEVEL: int = logging.MESSAGE # type: ignore 
    if arg_verbose: 
        LOG_LEVEL = logging.INFO
    elif arg_warning:
        LOG_LEVEL = logging.WARNING
    elif arg_debug:
        LOG_LEVEL = logging.DEBUG
    elif arg_silent:
        LOG_LEVEL = logging.ERROR
    MultilevelFormatter.setDefaults(logger, log_file=log)
    logger.setLevel(LOG_LEVEL)

    ...

```

# Example

Full runnable example below. It can be found in [demos/](demos/) folder. 

```python
import logging
from typer import Typer, Option
from typing import Annotated, Optional
from pathlib import Path
from multilevelformatter import MultilevelFormatter

logger = logging.getLogger(__name__)
error = logger.error
# MultiLevelFormatter adds MESSAGE level and message() to logging
message =  logger.message # type: ignore 
verbose = logger.info
debug = logger.debug

# the demo uses typer for CLI parsing. 
# Typer has nothing to do with MultiLevelFormatter
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
        LOG_LEVEL: int = logging.MESSAGE # type: ignore 
        if print_verbose:
            LOG_LEVEL = logging.INFO
        elif print_debug:
            LOG_LEVEL = logging.DEBUG
        elif print_silent:
            LOG_LEVEL = logging.ERROR
        MultilevelFormatter.setDefaults(logger, log_file=log)
        logger.setLevel(LOG_LEVEL)
    except Exception as err:
        error(f"{err}")
    message("standard")
    verbose("verbose")
    error("error")
    debug("debug")


if __name__ == "__main__":
    app()

```
