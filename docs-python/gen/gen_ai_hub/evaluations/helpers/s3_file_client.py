import boto3
import os
from typing import Dict, List, Any
import json
import csv
import pandas as pd
import sqlite3
from io import StringIO
import tempfile
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.logging import get_logger
from gen_ai_hub.evaluations.constants import CONTENT_TYPE

logger = get_logger()


class S3FileClient:
    """S3 client for read/write file operations with format-specific parsing."""

    def __init__(
        self,
        bucket_name: str,
        region: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        error_collector: ValidationCollector = None,
    ):
        """Initialize S3 client with flexible authentication options.

        :param bucket_name: S3 bucket name
        :type bucket_name: str
        :param region: AWS region (defaults to boto3 default), defaults to None
        :type region: str, optional
        :param aws_access_key_id: AWS access key (optional if using IAM/profile), defaults to None
        :type aws_access_key_id: str, optional
        :param aws_secret_access_key: AWS secret key (optional if using IAM/profile), defaults to None
        :type aws_secret_access_key: str, optional
        :param error_collector: Validation error collector, defaults to None
        :type error_collector: ValidationCollector, optional
        """
        self.bucket_name = bucket_name
        self.error_collector = error_collector

        try:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region,
            )

            self.s3_client = session.client("s3")
            self.region = region or session.region_name

            # Validate bucket access
            self._validate_bucket_access()

        except NoCredentialsError:
            self.error_collector.add_error(
                ErrorCode.INVALID_S3_CLIENT_ERROR,
                "AWS credentials not found. Please provide credentials via "
                "environment variables",
            )
        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.INVALID_S3_CLIENT_ERROR,
                f"Failed to initialize S3 client: {e}",
            )

    def _validate_bucket_access(self):
        """Validate that we can access the specified bucket.

        :raises ClientError: If bucket access fails
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Successfully connected to bucket: {self.bucket_name}")
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                self.error_collector.add_error(
                    ErrorCode.INVALID_S3_CLIENT_ERROR,
                    f"Bucket '{self.bucket_name}' not found",
                )
            elif error_code == "403":
                self.error_collector.add_error(
                    ErrorCode.INVALID_S3_CLIENT_ERROR,
                    f"Access denied to bucket '{self.bucket_name}'",
                )
            else:
                self.error_collector.add_error(
                    ErrorCode.INVALID_S3_CLIENT_ERROR,
                    f"Error accessing bucket '{self.bucket_name}': {e}",
                )

    def read_json(self, s3_key: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Read JSON file from S3.

        :param s3_key: S3 object key
        :type s3_key: str
        :param encoding: File encoding, defaults to "utf-8"
        :type encoding: str, optional
        :return: Dictionary containing JSON data, or empty list if file is empty or error occurs
        :rtype: Dict[str, Any]
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            content = response["Body"].read().decode(encoding)

            # Handle empty files
            if not content.strip():
                logger.warning(f"Empty JSON file: s3://{self.bucket_name}/{s3_key}")
                return []

            data = json.loads(content)
            logger.info(f"Successfully read JSON file from s3://{self.bucket_name}/{s3_key}")
            return data

        except json.JSONDecodeError as e:
            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR,
                f"Invalid JSON in s3://{self.bucket_name}/{s3_key}: {e}",
            )
            return []
        except (BotoCoreError, ClientError) as e:
            error_message = (
                f"Failed to read JSON from S3: s3://{self.bucket_name}/{s3_key} - {e}"
            )

            if getattr(e, "response", {}).get("Error", {}).get("Code") == "NoSuchKey":
                error_message = f"File not found: s3://{self.bucket_name}/{s3_key}"

            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR, error_message
            )
            return []
        except Exception as e:  # any other generic excedptions
            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR,
                f"Unexpected error reading JSON from S3: {e}",
            )
            return []

    def read_jsonl(self, s3_key: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
        """Read JSONL (JSON Lines) file from S3.

        :param s3_key: S3 object key
        :type s3_key: str
        :param encoding: File encoding, defaults to "utf-8"
        :type encoding: str, optional
        :return: List of dictionaries, one per line
        :rtype: List[Dict[str, Any]]
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            content = response["Body"].read().decode(encoding)

            if not content.strip():
                logger.warning(f"Empty JSONL file: s3://{self.bucket_name}/{s3_key}")
                return []

            data = []
            valid_lines = 0
            invalid_lines = 0

            for line_num, line in enumerate(content.strip().split("\n"), 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    data.append(json.loads(line))
                    valid_lines += 1
                except json.JSONDecodeError as e:
                    invalid_lines += 1
                    logger.warning(f"Skipping invalid JSON on line {line_num}: {e}")
                    continue

            logger.info(
                f"Successfully read JSONL file from s3://{self.bucket_name}/{s3_key} "
                f"({valid_lines} valid records, {invalid_lines} skipped)"
            )
            return data

        except (BotoCoreError, ClientError) as e:
            error_message = (
                f"Failed to read JSONL from S3: s3://{self.bucket_name}/{s3_key} - {e}"
            )

            if getattr(e, "response", {}).get("Error", {}).get("Code") == "NoSuchKey":
                error_message = f"File not found: s3://{self.bucket_name}/{s3_key}"

            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR, error_message
            )
            return []

        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR,
                f"Unexpected error reading JSONL from S3: {e}",
            )
            return []

    def read_csv(self, s3_key: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
        """Read CSV file from S3.

        :param s3_key: S3 object key
        :type s3_key: str
        :param encoding: File encoding, defaults to "utf-8"
        :type encoding: str, optional
        :return: List of dictionaries, one per row
        :rtype: List[Dict[str, Any]]
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            content = response["Body"].read().decode(encoding)

            df = pd.read_csv(
                StringIO(content),
                quoting=1,
                escapechar="\\",
                encoding="utf-8",
                keep_default_na=False,
                dtype=str,
            )

            logger.info(f"Successfully read CSV file from s3://{self.bucket_name}/{s3_key}")
            return df.to_dict("records")

        except csv.Error as e:
            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR,
                f"CSV parsing error in s3://{self.bucket_name}/{s3_key}: {e}",
            )
            return []
        except (BotoCoreError, ClientError) as e:
            error_message = (
                f"Failed to read CSV from S3: s3://{self.bucket_name}/{s3_key} - {e}"
            )

            if getattr(e, "response", {}).get("Error", {}).get("Code") == "NoSuchKey":
                error_message = f"File not found: s3://{self.bucket_name}/{s3_key}"

            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR, error_message
            )
            return []

        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.READ_FILE_DATA_FROM_ARTIFACT_ERROR,
                f"Unexpected error reading CSV from S3: {e}",
            )
            return []

    # UPLOAD METHODS
    def upload_json(self, data: Any, s3_key: str, **kwargs) -> bool:
        """Upload JSON data to S3.

        :param data: Data to upload (will be JSON-serialized)
        :type data: Any
        :param s3_key: S3 key path
        :type s3_key: str
        :param kwargs: Additional S3 put_object parameters
        :type kwargs: dict
        :return: True if upload succeeded, False otherwise
        :rtype: bool
        """
        try:
            json_string = json.dumps(
                data,
                ensure_ascii=False,
                separators=(",", ":"),
                default=str,
            )

            default_params = {
                "Bucket": self.bucket_name,
                "Key": s3_key,
                "Body": json_string.encode("utf-8"),
                "ContentType": CONTENT_TYPE,
            }
            default_params.update(kwargs)

            self.s3_client.put_object(**default_params)
            logger.info(
                "Uploaded JSON file to path s3://%s/%s", self.bucket_name, s3_key
            )
            return True

        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.FILE_UPLOAD_ERROR, f"Failed to upload JSON: {e}"
            )
            return False

    def upload_jsonl(self, data: List[Dict], s3_key: str, **kwargs) -> bool:
        """Upload JSONL data to S3.

        :param data: List of dictionaries to upload as JSONL
        :type data: List[Dict]
        :param s3_key: S3 key path
        :type s3_key: str
        :param kwargs: Additional S3 put_object parameters
        :type kwargs: dict
        :return: True if upload succeeded, False otherwise
        :rtype: bool
        """
        try:
            jsonl_lines = []
            for item in data:
                jsonl_lines.append(
                    json.dumps(
                        item, ensure_ascii=False, separators=(",", ":"), default=str
                    )
                )

            jsonl_string = "\n".join(jsonl_lines)

            default_params = {
                "Bucket": self.bucket_name,
                "Key": s3_key,
                "Body": jsonl_string.encode("utf-8"),
                "ContentType": "application/x-ndjson",  # Standard MIME type for JSONL
            }
            default_params.update(kwargs)

            self.s3_client.put_object(**default_params)
            logger.info(
                "Uploaded JSONL file to s3://%s/%s  with the length of %s records ",
                self.bucket_name,
                s3_key,
                len(data),
            )
            return True

        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.FILE_UPLOAD_ERROR, f"Failed to upload JSONL: {e}"
            )
            return False

    def upload_csv(self, data: List[Dict], s3_key: str, **kwargs) -> bool:
        """Upload CSV data to S3.

        :param data: List of dictionaries to upload as CSV
        :type data: List[Dict]
        :param s3_key: S3 key path
        :type s3_key: str
        :param kwargs: Additional S3 put_object parameters
        :type kwargs: dict
        :return: True if upload succeeded, False otherwise
        :rtype: bool
        """
        try:
            if not data:
                self.error_collector.add_error(
                    ErrorCode.FILE_UPLOAD_ERROR, "No data provided to upload"
                )
                return False

            df = pd.DataFrame(data)
            csv_string = df.to_csv(
                index=False, quoting=1, escapechar="\\", encoding="utf-8"
            )
            default_params = {
                "Bucket": self.bucket_name,
                "Key": s3_key,
                "Body": csv_string.encode("utf-8"),
                "ContentType": "text/csv",  # Standard type for CSV
            }
            default_params.update(kwargs)

            self.s3_client.put_object(**default_params)
            logger.info("Uploaded CSV file to s3://%s/%s", self.bucket_name, s3_key)
            return True

        except Exception as e:
            self.error_collector.add_error(
                ErrorCode.FILE_UPLOAD_ERROR, f" Failed to upload CSV: {e}"
            )
            return False

    def get_sqlitedb_tables_data_from_s3(self, s3_key: str, tables_list: List[str]) -> Dict[str, List[Dict]]:
        """Download SQLite DB from S3, load given tables into memory, return dict of lists.

        :param s3_key: S3 object key for the SQLite database file
        :type s3_key: str
        :param tables_list: List of table names to extract from the database
        :type tables_list: List[str]
        :return: Dictionary mapping table names to lists of row dictionaries
        :rtype: Dict[str, List[Dict]]
        :raises RuntimeError: If database operations fail
        """
        data_store = {}

        s3_key = s3_key.lstrip("/")
        logger.debug(f"Fetching SQLite tables {tables_list} from s3://{self.bucket_name}/{s3_key}")

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            self.s3_client.download_fileobj(self.bucket_name, s3_key, tmp)
            tmp_path = tmp.name

        try:
            conn = sqlite3.connect(tmp_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            for table in tables_list:
                cursor.execute(f"SELECT * FROM {table}")
                data_store[table] = [dict(row) for row in cursor.fetchall()]

            conn.close()
        except Exception as e:
            raise RuntimeError(
                f"Failed to get data from sqlite in the path of {s3_key} with error of {e}"
            ) from e
        finally:
            os.remove(tmp_path)

        return data_store
