from typing import List, Optional, Union
from gen_ai_hub.evaluations.models.dataset_config import Dataset
from gen_ai_hub.evaluations.models.metric_config import MetricConfig

from gen_ai_hub.orchestration_v2.models.llm_model_details import LLMModelDetails as LLM
from gen_ai_hub.orchestration_v2.models.template_ref import (
    TemplateRef,
)
from gen_ai_hub.prompt_registry.models.prompt_template import PromptTemplateSpec


class EvaluationConfig:
    """Defines the evaluation configuration object for the Evaluations flow.

    This class encapsulates all configuration parameters needed to run an evaluation job,
    including the model/template configuration, dataset, metrics, and execution settings.

    At least one of the following must be provided:

    - ``llm`` and ``template`` combination (using orchestration_v2 models)
    - ``orchestration_registry_reference`` (UUID of a registered orchestration configuration)

    :param dataset_config: Dataset configuration object specifying the evaluation dataset
    :type dataset_config: Dataset
    :param metrics: List of metric configurations for evaluation
    :type metrics: List[MetricConfig]
    :param llm: LLM configuration from orchestration_v2 (LLMModelDetails)
    :type llm: Optional[LLM]
    :param template: Prompt template as string, PromptTemplateSpec, or TemplateRef
    :type template: Optional[Union[str, PromptTemplateSpec, TemplateRef]]
    :param orchestration_registry_reference: UUID of registered orchestration configuration
    :type orchestration_registry_reference: Optional[str]
    :param template_variable_mapping: Variable mapping for the prompt template
    :type template_variable_mapping: Optional[dict]
    :param test_row_count: Number of rows to sample from dataset (-1 for all rows), defaults to -1
    :type test_row_count: Optional[int]
    :param repetitions: Number of times to repeat evaluation over the dataset, defaults to 1
    :type repetitions: Optional[int]
    :param tags: User-defined metadata as key-value pairs, defaults to "{}"
    :type tags: Optional[dict]
    :param debug_mode: Enable debug logs in hyperscaler output path, defaults to False
    :type debug_mode: Optional[bool]

    .. note::
       This module uses orchestration_v2 models directly.

    **Example using TemplateRef with ID**:

    >>> from gen_ai_hub.evaluations.models import EvaluationConfig, Dataset, MetricConfig
    >>> from gen_ai_hub.orchestration_v2.models.llm_model_details import LLMModelDetails as LLM
    >>> from gen_ai_hub.orchestration_v2.models.template_ref import TemplateRef, TemplateRefByID
    >>> config = EvaluationConfig(
    ...     dataset_config=Dataset("data/test.jsonl"),
    ...     metrics=[MetricConfig(name="accuracy")],
    ...     llm=LLM(name="gpt-4", version="latest"),
    ...     template=TemplateRef(template_ref=TemplateRefByID(id="template-id-here")),
    ...     test_row_count=100
    ... )

    **Example using TemplateRef with scenario/name/version**:

    >>> from gen_ai_hub.orchestration_v2.models.template_ref import TemplateRefByScenarioNameVersion
    >>> config = EvaluationConfig(
    ...     dataset_config=Dataset("data/test.jsonl"),
    ...     metrics=[MetricConfig(name="accuracy")],
    ...     llm=LLM(name="gpt-4", version="latest", params={"temperature": 0.7}),
    ...     template=TemplateRef(template_ref=TemplateRefByScenarioNameVersion(
    ...         scenario="foundation-models", name="prompt1", version="1.0"
    ...     )),
    ...     test_row_count=100
    ... )
    """

    def __init__(
        self,
        dataset_config: Dataset,
        metrics: List[MetricConfig],
        llm: Optional[LLM] = None,
        template: Optional[Union[str, PromptTemplateSpec, TemplateRef]] = None,
        orchestration_registry_reference: Optional[
            str
        ] = None,  # currently only supports uuid, in future when dataclasses comes up in sdk, then support scenario/name/version
        template_variable_mapping: Optional[dict] = None,
        test_row_count: Optional[int] = -1,
        repetitions: Optional[int] = 1,
        tags: Optional[dict] = "{}",
        debug_mode: Optional[bool] = False,
    ):
        """Initialize an EvaluationConfig instance.

        :param dataset_config: Dataset configuration object
        :type dataset_config: Dataset
        :param metrics: List of metric configurations
        :type metrics: List[MetricConfig]
        :param llm: LLM object from orchestration_v2 (LLMModelDetails), defaults to None
        :type llm: Optional[LLM]
        :param template: Prompt template (string, PromptTemplateSpec, or TemplateRef), defaults to None
        :type template: Optional[Union[str, PromptTemplateSpec, TemplateRef]]
        :param orchestration_registry_reference: UUID of orchestration config, defaults to None
        :type orchestration_registry_reference: Optional[str]
        :param template_variable_mapping: Variable mapping for prompt template, defaults to None
        :type template_variable_mapping: Optional[dict]
        :param test_row_count: Number of dataset rows to sample (-1 for all), defaults to -1
        :type test_row_count: Optional[int]
        :param repetitions: Number of evaluation repetitions (minimum: 1), defaults to 1
        :type repetitions: Optional[int]
        :param tags: Key-value metadata pairs applied to all runs, defaults to "{}"
        :type tags: Optional[dict]
        :param debug_mode: Enable debug logging, defaults to False
        :type debug_mode: Optional[bool]
        :raises ValueError: If neither (llm, template) nor orchestration_registry_reference is provided
        """
        super().__init__()
        self.llm = llm
        self.template = template
        self.orchestration_registry_reference = orchestration_registry_reference
        self.template_variable_mapping = template_variable_mapping
        self.dataset_config = dataset_config
        self.metrics = metrics
        self.test_row_count = test_row_count
        self.tags = tags
        self.repetitions = repetitions
        self.debug_mode = debug_mode

__all__ = ["EvaluationConfig"]