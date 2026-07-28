import logging
import os
from gen_ai_hub.evaluations.constants import DEBUG_ENV_VAR_NAME


BASE_LOGGER_NAME = "gen_ai_evaluations_sdk"
DEFAULT_LOG_LEVEL = logging.INFO


def get_logger(name: str = None):
    # Use a hierarchical logger structure to allow for more granular control
    logger_name = f"{name}" if name else BASE_LOGGER_NAME
    return logging.getLogger(logger_name)


def set_log_level(logger: logging.Logger, default_level=DEFAULT_LOG_LEVEL):
    # Check if DEBUG is set to "true" (case-insensitive)
    debug_env = os.getenv(DEBUG_ENV_VAR_NAME)
    debug = debug_env is not None and debug_env.lower() == 'true'
    logger.setLevel(logging.DEBUG if debug else default_level)


set_log_level(get_logger())
