from pathlib import Path
from typing import Union, Dict, Any, List
import json
import uuid
import pandas as pd
from gen_ai_hub.evaluations.constants import (
    CSV_FILE_TYPE,
    JSON_FILE_TYPE,
    JSONL_FILE_TYPE,
    SUPPORTED_FILE_TYPES,
)
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def load_config_file(
    file_path: Union[str, Path], error_collector: ValidationCollector
) -> Union[Dict[str, Any], List[Dict[str, Any]], List]:
    """Load config from local file path or Path object"""
    # Convert to Path object for consistent handling
    path = Path(file_path).expanduser().resolve()
    logger.info("Loading the local file from the path: %s", path)

    # Validate file exists
    if not path.exists():
        error_collector.add_error(
            ErrorCode.INVALID_FILE_PATH_ERROR, f"Provide Config file not found: {path}"
        )
        return []

    if not path.is_file():
        error_collector.add_error(
            ErrorCode.INVALID_FILE_PATH_ERROR,
            f"Provided Path: {path} is not an actual file. Please provide a file and not a directory!",
        )
        return []

    # Determine file type by extension
    suffix = path.suffix.lower().lstrip(".")

    if suffix not in SUPPORTED_FILE_TYPES:
        error_collector.add_error(
            ErrorCode.UNSUPPORTED_FILE_TYPE_ERROR,
            f"File type provided is not supported for this file: {path}. Please provide one of {SUPPORTED_FILE_TYPES}",
        )
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            if suffix in [JSON_FILE_TYPE]:
                return json.load(f)
            if suffix in [CSV_FILE_TYPE]:
                return read_local_csv_file(path, error_collector)
            if suffix in [JSONL_FILE_TYPE]:
                return [json.loads(line) for line in f]

    except json.JSONDecodeError as e:
        error_collector.add_error(
            ErrorCode.INVALID_JSON_DECODING_ERROR,
            f"Failed to parse config file {path}: {e}",
        )
        return []
    except (OSError, UnicodeDecodeError) as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"File access error for config file {path}: {e}"
        )
        return []
    except ValueError as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"Value error reading config file {path}: {e}"
        )
        return []
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"Reading config file {path} failed with: {e}"
        )
        return []


def read_local_csv_file(file_path: Path, error_collector: ValidationCollector) -> List[Dict[str, Any]]:
    """reads csv and returns the data as df"""
    try:
        df = pd.read_csv(
            file_path,
            quoting=1,
            escapechar="\\",
            encoding="utf-8",
            keep_default_na=False,
            dtype=str,
        )
        return df.to_dict("records")
    except pd.errors.ParserError as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"CSV parsing error in file: {file_path}: {e}"
        )
        return []
    except OSError as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"File access error for csv file: {file_path}: {e}"
        )
        return []
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR, f"Reading config file {file_path} failed with: {e}"
        )
        return []