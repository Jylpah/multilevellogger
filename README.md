![CI](https://github.com/Jylpah/multilevellogger/actions/workflows/python-package.yml/badge.svg) [![codecov](https://codecov.io/gh/Jylpah/multilevellogger/graph/badge.svg?token=IDH9SJB44Q)](https://codecov.io/gh/Jylpah/multilevellogger)  [![CodeQL](https://github.com/Jylpah/multilevellogger/actions/workflows/codeql.yml/badge.svg)](https://github.com/Jylpah/multilevellogger/actions/workflows/workflows/codeql.yml)

# MultiLevelLogger

`MultiLevelLogger` is a Python `logging.Logger` that simplifies setting log formats for different log levels. Log records with level `logging.ERROR` or higher are printed to STDERR by default. Motivation for the class has been the use of `logging` package for CLI verbosity control (`--verbose`, `--debug`):

1. Define shortcuts for printing different level information instead of using `print() `:

```python
import multilevellogger

logger = multilevellogger.getMultiLevelLogger(__name__)
error = logger.error
message = logger.message
verbose = logger.verbose
debug = logger.debug
```

2. Set logging level based on CLI option given. Mapping of logging levels:

| CLI option  | logging level     |
| ----------- | ----------------- |
| `--debug`   | `logging.DEBUG`   |
| `--verbose` | `multilevellogger.VERBOSE`    |
| default     | `multilevellogger.MESSAGE` |
| `--silent`  | `logging.ERROR`   |


```python
# Not complete, does not run
def main() -> None:
    
    ...

    # assumes command line arguments have been parsed into 
    # boolean flags: arg_verbose, arg_debug, arg_silent
    
    LOG_LEVEL: int = multilevellogger.MESSAGE
    if arg_verbose: 
        LOG_LEVEL = multilevellogger.VERBOSE
    elif arg_debug:
        LOG_LEVEL = logging.DEBUG
    elif arg_silent:
        LOG_LEVEL = logging.ERROR
    logger : MultiLevelLogger = getMultiLevelLogger(__name_)
    logger.setLevel(LOG_LEVEL)
    logger.addLogFile(log_file=file_to_log, level=logging.INFO)
```

See the example below for more details.

## Install

*Python 3.11 or later is required.*

```sh
pip install git+https://github.com/Jylpah/multilevellogger.git
```

# Example

Full runnable example below. It can be found in [demos/](demos/) folder. 

```python
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
```
