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
import sys
from typing import Literal, Optional, Dict, ClassVar, List
from pathlib import Path

from deprecated import deprecated  # type: ignore

# from icecream import ic  # type: ignore

MESSAGE: int = logging.WARNING - 5  # 25


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
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError(f"{levelName} already defined in logging module")
    if hasattr(logging, methodName):
        raise AttributeError(f"{methodName} already defined in logging module")
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError(f"{methodName} already defined in logger class")

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


def addLoggingLevelMessage() -> None:
    """
    Add  logging level logging.MESSAGE to the root logger with value 25
    """
    addLoggingLevel("MESSAGE", logging.WARNING - 5)


class MultilevelFormatter(logging.Formatter):
    """
    logging.Formatter that simplifies setting different log formats
    for different log levels.

    Add to the module file:

    logger = logging.getLogger(__name__)
    error = logger.error
    message = logger.warning
    verbose = logger.info
    debug = logger.debug
    """

    _levels: ClassVar[List[int]] = [
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]

    def __init__(
        self,
        fmts: Dict[int, str],
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        *,
        defaults=None,
    ):
        assert fmts is not None, "'fmts' cannot be None"
        assert style in ["%", "{", "$"], "'style' must be '%', '{' or '$'"
        assert isinstance(validate, bool), "'validate' must be bool"
        self._formatters: Dict[int, logging.Formatter] = dict()
        for level in set(self._levels) | set(fmts.keys()):
            _fmt: str | None = fmt
            if level in fmts.keys():
                _fmt = fmts[level]
            self.setFormat(
                level,
                fmt=_fmt,
                datefmt=datefmt,
                style=style,
                validate=validate,
                defaults=defaults,
            )

    @classmethod
    @deprecated(version="0.5", reason="Renamed, please use setFormats() instead")
    def setLevels(
        cls,
        logger: logging.Logger,
        fmts: Dict[int, str],
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        log_file: Optional[str | Path] = None,
    ) -> None:
        """
        DEPRECIATED: Use setFormats()

        Will be removed

        Setup logging format for multiple levels
        """
        cls.setFormats(
            logger=logger,
            fmts=fmts,
            fmt=fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
            log_file=log_file,
        )

    @classmethod
    def setFormats(
        cls,
        logger: logging.Logger,
        fmts: Dict[int, str],
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        log_file: Optional[str | Path] = None,
    ) -> None:
        """
        Setup logging format for multiple levels
        """
        try:
            multi_formatter = MultilevelFormatter(
                fmts=fmts, fmt=fmt, datefmt=datefmt, style=style, validate=validate
            )
            # log all but errors to STDIN
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.addFilter(lambda record: record.levelno < logging.ERROR)
            stream_handler.setFormatter(multi_formatter)
            logger.addHandler(stream_handler)
            # log errors and above to STDERR
            error_handler = logging.StreamHandler(sys.stderr)
            error_handler.setLevel(logging.ERROR)
            error_handler.addFilter(lambda record: record.levelno >= logging.ERROR)
            error_handler.setFormatter(multi_formatter)
            logger.addHandler(error_handler)
            if log_file is not None:
                file_handler = logging.FileHandler(log_file)
                log_formatter = logging.Formatter(
                    fmt=fmt, style=style, validate=validate
                )
                file_handler.setFormatter(log_formatter)
                logger.addHandler(file_handler)
        except Exception as err:
            logging.error(f"Could not set formats: {err}")

    @classmethod
    def setDefaults(
        cls,
        logger: logging.Logger,
        log_file: Optional[str | Path] = None,
        level: int = logging.WARNING,
    ) -> None:
        """Set multi-level formatting defaults

        INFO: %(message)s
        WARNING: %(message)s                 ## Used as message() / default
        ERROR: %(levelname)s: %(funcName)s(): %(message)s
        CRITICAL: %(levelname)s: %(funcName)s(): %(message)s
        """
        logger_conf: Dict[int, str] = {
            logging.INFO: "%(message)s",
            logging.WARNING: "%(message)s",
            # logging.ERROR: '%(levelname)s: %(message)s'
        }
        if level == MESSAGE:
            logger_conf[MESSAGE] = "%(message)s"
            logger_conf[logging.WARNING] = "WARN: %(message)s"
            addLoggingLevelMessage()

        MultilevelFormatter.setFormats(
            logger,
            fmts=logger_conf,
            fmt="%(levelname)s: %(funcName)s(): %(message)s",
            log_file=log_file,
        )
        logger.setLevel(level=level)

    def setFormat(self, level: int, fmt: str | None = None, **kwargs):
        """
        Set log format for a single level
        """
        self._formatters[level] = logging.Formatter(fmt=fmt, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        try:
            return self._formatters[record.levelno].format(record)
        except Exception as err:
            logging.error(f"{err}")
            return f"{err}"

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None):
        try:
            return self._formatters[record.levelno].formatTime(
                record=record, datefmt=datefmt
            )
        except Exception as err:
            logging.error(f"{err}")
            return f"{err}"


# def warning(msg: str):
#     """
#     Helper to log a warning message.
#     """
#     return eval(f"message('WARN: {msg}')")
