import logging
import sys
from logging import Logger
from pathlib import Path

from loguru import logger

from app.core.config import get_settings
from app.core.logging_interceptor import InterceptHandler


def intercept_all_loggers(log_level=logging.INFO):
    intercept_handler = InterceptHandler()

    # 1. Root logger (captures all future loggers)
    logging.root.handlers = [intercept_handler]
    logging.root.setLevel(log_level)

    # 2. Existing loggers (already created)
    for name, logger_obj in logging.root.manager.loggerDict.items():
        if not isinstance(logger_obj, Logger):
            continue

        # Avoid intercepting Loguru internals
        if name.startswith("loguru"):
            continue

        logger_obj.handlers = [intercept_handler]
        logger_obj.propagate = False


def setup_logging():
    settings = get_settings()

    log_level = logging.getLevelNamesMapping().get(
        settings.log_level.upper(),
        logging.INFO,
    )
    log_dir = settings.log_dir
    environment = settings.environment
    debug = settings.debug

    try:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        # logger.error("Failed to create log directory", error=str(exc))
        logger.bind(error=str(exc)).error("Failed to create log directory")
        raise

    # Remove default Loguru handlers
    logger.remove()

    # Console sink
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=True,
        diagnose=debug,
        enqueue=True,
    )

    # Production JSON logs
    if environment == "production":
        logger.add(
            Path(log_dir) / "app.json",
            level=log_level,
            rotation="500 MB",
            retention="30 days",
            compression="gz",
            serialize=True,
            enqueue=True,
        )

    # ------------------------------------------------------------------
    # Redirect standard logging -> Loguru
    # ------------------------------------------------------------------
    intercept_all_loggers(log_level)

    logging.captureWarnings(True)

    logger.info("Logging configured", env=environment)
