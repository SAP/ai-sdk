from typing import List, Any, Optional, Union
from dataclasses import dataclass, field

@dataclass
class _EvaluationConfigData:
    """
    Defines the helper model to store the data of orch_configs, testdataset, custom_metric_config in case of user not providing the direct config.

    :param orch_config_data: Orchestration configuration data.
                             Can be a single dictionary or a list of dictionaries.
    :type orch_config_data: Union[dict, List[dict]]

    :param dataset_type: Type of dataset (e.g., ``json``, ``jsonl``, ``csv``).
    :type dataset_type: str

    :param dataset_data: Loaded dataset content. Supports multiple formats
                         depending on ``dataset_type``.
    :type dataset_data: Any

    :param metric_templates: List of custom metric template configurations.
    :type metric_templates: List[dict]

    :param metrics_list: List of metric identifiers to evaluate.
    :type metrics_list: List[str]

    :param variable_mapping: Optional mapping between prompt/metric variables
                             and dataset columns.
    :type variable_mapping: Optional[dict]

    :param test_row_count: Number of dataset rows to evaluate. Defaults to ``-1`` (all rows).
    :type test_row_count: Optional[int]

    :param repetitions: Number of times each test should be repeated. Defaults to ``1``.
    :type repetitions: Optional[int]

    :param tags: Optional metadata tags associated with the evaluation run.
    :type tags: Optional[dict]

    :param debug_mode: Enables debug mode for additional logging or diagnostics.
    :type debug_mode: Optional[bool]
    """

    orch_config_data: Union[dict | List[dict]]
    dataset_type: str
    dataset_data: Any  # to support for csv,json,jsonl data types
    metric_templates: List[dict]
    metrics_list: List[str]
    variable_mapping: Optional[dict] = (
        None  # after converting the Json dict to string to be compatible with the utils code
    )
    test_row_count: Optional[int] = -1
    repetitions: Optional[int] = 1
    tags: Optional[dict] = field(default_factory=dict)
    debug_mode: Optional[bool] = False


@dataclass
class _AWSObjectStoreData:
    """
    Stores AWS object store credentials used for accessing S3-compatible storage.

    :param aws_access_key_id: AWS access key ID.
    :type aws_access_key_id: str

    :param aws_secret_access_key: AWS secret access key.
    :type aws_secret_access_key: str
    """
    aws_access_key_id: str
    aws_secret_access_key: str
