# MultiLevelFormatter

`MultiLevelFormatter` is a Python `logging.Formatter` that simplifies setting log formats for different log levels. Log records with level `logging.ERROR` or higher are printed to STDERR if using defaults with `MultilevelFormatter.setDefaults()`.

Motivation for the class has been the use of `logging` package for CLI verbosity control (`--verbose`, `--debug`):

1. Define shortcuts for printing different level information instead of using `print() `:

```python
logger = logging.getLogger(__name__)
error = logger.error
message = logger.warning
verbose = logger.info
debug = logger.debug
```

2. Set logging level based on CLI option given. Mapping of logging levels:

| CLI option  | logging level     |
| ----------- | ----------------- |
| `--debug`   | `logging.DEBUG`   |
| `--verbose` | `logging.INFO`    |
| default     | `logging.WARNING` |
| `--silent`  | `logging.ERROR`   |


```python
# Not complete, does not run
def main() -> None:
    
    ...

    # assumes command line arguments have been parsed into 
    # boolean flags: arg_verbose, arg_debug, arg_silent
    
    LOG_LEVEL: int = logging.WARNING
    if arg_verbose: 
        LOG_LEVEL = logging.INFO
    elif arg_debug:
        LOG_LEVEL = logging.DEBUG
    elif arg_silent:
        LOG_LEVEL = logging.ERROR
    MultilevelFormatter.setDefaults(logger, log_file=log)
    logger.setLevel(LOG_LEVEL)
```

See the example below for more details.

## Install

*Python 3.11 or later is required.*

```sh
pip install multilevelformatter
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
message =  logger.warning 
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
    message("standard")
    verbose("verbose")
    error("error")
    debug("debug")


if __name__ == "__main__":
    app()

```
