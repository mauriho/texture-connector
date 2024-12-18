"""
========================================================================================
Name: logger.py
Author: Mauricio Gonzalez Soto
Updated Date: 12-17-2024

Copyright (C) 2024 Mauricio Gonzalez Soto. All rights reserved.
========================================================================================
"""

from maya.api.OpenMaya import MGlobal

import logging
import sys


class Logger:
    LOGGER_NAME = "texture_connector"
    LOGGER_LEVEL = logging.INFO

    _logger = None

    @classmethod
    def create_logger(cls) -> logging.Logger:

        if not cls._logger:
            if cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys():
                cls._logger = logging.getLogger(cls.LOGGER_NAME)
            else:
                formatter = logging.Formatter(
                    "%(levelname)s: [Texture Connector] %(message)s"
                )

                stream_handler = logging.StreamHandler(sys.stdout)
                stream_handler.setFormatter(formatter)

                cls._logger = logging.getLogger(cls.LOGGER_NAME)
                cls._logger.addHandler(stream_handler)
                cls._logger.setLevel(cls.LOGGER_LEVEL)
                cls._logger.propagate = False

        return cls._logger

    @classmethod
    def debug(cls, msg: str) -> None:
        logger = cls.create_logger()
        logger.debug(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        MGlobal.displayInfo(f"[Texture Connector] {msg}")

    @classmethod
    def warning(cls, msg: str) -> None:
        MGlobal.displayWarning(f"[Texture Connector] {msg}")

    @classmethod
    def error(cls, msg: str) -> None:
        MGlobal.displayError(f"[Texture Connector] {msg}")
