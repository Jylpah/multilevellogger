# -----------------------------------------------------------
#  Class MultilevelFormatter(logging.Formatter)
#
#  logging.Formatter that simplifies setting different log formats
#  for different log levels.
#
# -----------------------------------------------------------

__author__ = "Jylpah"
__copyright__ = "Copyright 2024, Jylpah <Jylpah@gmail.com>"
__credits__ = ["Jylpah"]
__license__ = "MIT"
__maintainer__ = "Jylpah"
__email__ = "Jylpah@gmail.com"
__status__ = "Production"

import logging
from typing import Optional, Dict

VERBOSE: int = logging.INFO + 3
MESSAGE: int = logging.INFO + 5


def addLoggingLevel(
    levelName: str, levelNum: int, methodName: str | None = None
) -> None:
    """
    Copyright 2022 Joseph R. Fox-Rabinovitz aka Mad Physicist @StackOverflow.com
    Credits Mad Physicist

    Adapted from https://stackoverflow.com/a/35804945/12946084

    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    try:
        if methodName is None:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
            raise AttributeError(f"{levelName} level already defined in logging module")
        if hasattr(logging, methodName):
            raise AttributeError(
                f"{methodName} method already defined in logging module"
            )
        if hasattr(logging.getLoggerClass(), methodName):
            raise AttributeError(f"{methodName} method already defined in logger class")

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)
    except AttributeError:
        pass


def addLoggingLevelMessage() -> None:
    """
    Add  logging level logging.MESSAGE to the root logger with value 25
    """
    return addLoggingLevel("MESSAGE", MESSAGE)


def addLoggingLevelVerbose() -> None:
    """
    Add  logging level logging.VERBOSE to the root logger with value 15
    """
    return addLoggingLevel("VERBOSE", VERBOSE)


class MultiLevelFormatter(logging.Formatter):
    """
    logging.Formatter that simplifies setting different log formats
    for different log levels.

    Adds two new logging levels: MESSAGE (35) and VERBOSE (25)
    meant for replacing print() with verbosity level control.
    """

    VERBOSE: int = VERBOSE
    MESSAGE: int = MESSAGE

    _formats: Dict[int, str] = {
        logging.NOTSET: "%(funcName)s(): %(message)s",
        logging.DEBUG: "%(levelname)s: %(funcName)s(): %(message)s",
        logging.INFO: "%(levelname)s: %(funcName)s(): %(message)s",
        VERBOSE: "%(message)s",
        MESSAGE: "%(message)s",
        logging.WARNING: "%(levelname)s: %(message)s",
        logging.ERROR: "%(levelname)s: %(funcName)s(): %(message)s",
        logging.CRITICAL: "%(levelname)s: %(funcName)s(): %(message)s",
    }

    def __init__(
        self,
        fmts: Dict[int, str] = dict(),
        **kwargs,
    ):
        assert fmts is not None, "'fmts' cannot be None"
        self._formatters: Dict[int, logging.Formatter] = dict()
        self._formats: Dict[int, str] = self._formats | fmts
        for level, fmt in self._formats.items():
            self.setFormat(level, fmt, **kwargs)

    def setFormat(self, level: int, fmt: str | None = None, **kwargs):
        """
        Set log format for a single level
        """
        self._formatters[level] = logging.Formatter(fmt=fmt, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        try:
            return self._formatters[record.levelno].format(record)
        except IndexError as err:
            logging.error(f"{err}")
            return logging.Formatter("NOTSET: %(funcName)s(): %(message)s").format(
                record
            )
        except Exception as err:
            logging.error(f"{err}")
            return f"{err}"

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None):
        try:
            return self._formatters[record.levelno].formatTime(
                record=record, datefmt=datefmt
            )
        except IndexError as err:
            logging.error(f"{err}")
            return logging.Formatter("NOTSET: %(funcName)s(): %(message)s").formatTime(
                record, datefmt=datefmt
            )
        except Exception as err:
            logging.error(f"{err}")
            return f"{err}"
