from dataclasses import dataclass
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.constants import (
    DEFAULT_KEY,
    AWS_S3_OSS_TYPE_KEY,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from ai_api_client_sdk.exception import AIAPINotFoundException

@dataclass
class ObjectStoreData:
    provider_name: str
    aws_access_key_id: str
    aws_secret_access_key: str


def create_aws_object_store_secret(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    secret_body: dict,
    is_default_secret: bool,
):
    """creates the s3 based object store secrets in aicore environment"""
    try:
        secret_data = secret_body.get("data", {}) or {}

        aws_access_key_id = secret_data.get(AWS_ACCESS_KEY_ID, aws_access_key_id)
        aws_secret_access_key = secret_data.get(
            AWS_SECRET_ACCESS_KEY, aws_secret_access_key
        )
        secret_name = DEFAULT_KEY if is_default_secret else secret_body.get("name")
        if not secret_name:
            raise KeyError(
                "Error while creating the object store secret. Name is mandatory to create the secret"
            )
        response = ai_core_client.object_store_secrets.create(
            name=secret_name,
            type=AWS_S3_OSS_TYPE_KEY,
            data={
                # use if overridden from user
                AWS_ACCESS_KEY_ID: aws_access_key_id,
                AWS_SECRET_ACCESS_KEY: aws_secret_access_key,
            },
            bucket=secret_body.get("bucket"),
            endpoint=secret_body.get("endpoint"),
            region=secret_body.get("region"),
            path_prefix=secret_body.get("pathPrefix", ""),
            verifyssl=secret_body.get("verifyssl", ""),
            usehttps=secret_body.get("usehttps", ""),
            resource_group=resource_group,
        )
        return response

    except Exception as e:
        raise ValueError(
            f"Error while creating the Object Store secret. Request failed with error of {e}"
        ) from e


def fetch_object_store_secret_by_name(
    ai_core_client: AICoreV2Client,
    name: str,
    resource_group: str,
    collector: ValidationCollector,
):
    try:
        response = ai_core_client.object_store_secrets.get(name, resource_group)
        return response
    except Exception as e:
        collector.add_error(
            ErrorCode.GET_OBJECT_STORE_SECRET_ERROR.value,
            f"Fetching Object Store secret failed with error of {e}",
        )
        return None


def delete_object_store_secret(
    ai_core_client: AICoreV2Client, name: str, resource_group: str
):
    """Delete an object store secret. Returns None if secret doesn't exist (404 error)."""

    try:
        response = ai_core_client.object_store_secrets.delete(name, resource_group)
        return response
    except AIAPINotFoundException:
        # Secret doesn't exist, which is fine when trying to delete
        return None
    except Exception as e:
        raise KeyError(
            f"Error while deleting the Object Store secret. Request failed with error of {e}"
        ) from e
