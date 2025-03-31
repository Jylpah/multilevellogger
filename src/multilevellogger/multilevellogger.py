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
from typing import Optional, cast
from pathlib import Path

from .multilevelformatter import MultiLevelFormatter, VERBOSE, MESSAGE


class MultiLevelLogger(logging.Logger):
    """
    logging.Logger that simplifies setting different log formats
    for different log levels.

    """

    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name, level)
        # self._logger: logging.Logger = logging.getLogger(name)
        # self._mformatter: logging.Formatter = MultiLevelFormatter(fmts=self._formats)
        # for handler in self._logger.handlers:
        #     handler.setFormatter(self._mformatter)
        # self._logger.setLevel(level)

    def verbose(self, msg: str, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)

    def message(self, msg: str, *args, **kwargs):
        if self.isEnabledFor(MESSAGE):
            self._log(MESSAGE, msg, args, **kwargs)


def getMultiLevelLogger(
    name: str,
    level: int = logging.NOTSET,
    log_file: Optional[str | Path] = None,
    handler: logging.Handler = logging.StreamHandler(sys.stdout),
    error_handler: Optional[logging.Handler] = None,
) -> MultiLevelLogger:
    """
    Get a MultilevelLogger with the specified name and level
    """
    logging.setLoggerClass(MultiLevelLogger)
    logger = cast(MultiLevelLogger, logging.getLogger(name))
    logger.setLevel(level)
    formatter: logging.Formatter = MultiLevelFormatter()

    # remove all handlers
    for h in logger.handlers:
        h.setFormatter(formatter)
        h.setLevel(level)
        # logger.removeHandler(h)

    handler.setFormatter(formatter)
    handler.setLevel(level)

    if error_handler is not None:
        handler.addFilter(lambda record: record.levelno < logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)

    logger.addHandler(handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

    # # def addHandler(
    # #     self,
    # #     handler: logging.Handler,
    # # ):
    # #     """
    # #     Add handler with the MultilevelFormatter to the logger
    # #     """
    # #     handler.setFormatter(self._mformatter)
    # #     self._logger.addHandler(handler)

    # def setDefaults(
    #     self,
    #     log_file: Optional[str | Path] = None,
    #     level: int = MESSAGE,
    # ):
    #     """
    #     Set defaults for MultilevelLogger
    #     """
    #     # log all but errors to STDIN
    #     handler = logging.StreamHandler(sys.stdout)
    #     handler.addFilter(lambda record: record.levelno < logging.ERROR)
    #     handler.setLevel(level)
    #     self.addHandler(handler)

    #     # log errors and above to STDERR
    #     error_handler = logging.StreamHandler(sys.stderr)
    #     error_handler.setLevel(logging.ERROR)
    #     self.addHandler(error_handler)

    #     if log_file is not None:
    #         file_handler = logging.FileHandler(log_file)
    #         file_handler.setLevel(logging.INFO)
    #         self.addHandler(file_handler)

    # # use parent class methods
    # def __getattr__(self, item):
    #     return getattr(self._logger, item)
