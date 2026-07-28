class MetricRef:
    """
    Represents a reference to a specific metric definition.

    A metric can be identified in multiple ways:
    - By its UUID from metric management service (`id`)
    - By name (`name`)
    - By a combination of scenario, name, and version (`scenario`, `name`, `version`)
    """

    def __init__(
        self,
        scenario: str = None,
        name: str = None,
        version: str = None,
        id: str = None,
    ):
        self.name = name
        self.scenario = scenario
        self.version = version
        self.id = id

class MetricConfig:
    """
    Defines the metric config of the evaluation flow

    Parameters:
        reference(MetricRef): Provide the reference of metric to be evaluated, can be one of name,uuid(id), scenario/name/version
        variable_mapping(Optional[dict]): Any variable maping associated with the metric
    """

    def __init__(
        self,
        reference: MetricRef,
        variable_mapping: dict = None,
    ):
        self.reference = reference
        self.variable_mapping = variable_mapping

__all__ = ["MetricRef", "MetricConfig"]