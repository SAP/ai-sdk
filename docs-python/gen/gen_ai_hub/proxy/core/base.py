from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Type

from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass


class BaseDeployment(BaseModel, ABC):
    """Abstract base class for all deployment types.

    :param BaseModel: the base model class from Pydantic.
    :type BaseModel: pydantic.BaseModel
    :param ABC: the abstract base class module.
    :type ABC: abc.ABC
    :return: the abstract base class for deployments.
    :rtype: BaseDeployment
    """
    model_config = ConfigDict(
        protected_namespaces=()
    )

    @abstractmethod
    def additional_request_body_kwargs(self) -> Dict[str, Any]:
        ...

    @property
    @abstractmethod
    def prediction_url(self) -> Tuple[str]:
        ...

    @classmethod
    @abstractmethod
    def get_model_identification_kwargs(cls) -> Tuple[str]:
        ...

    @classmethod
    def get_main_model_identification_kwargs(cls) -> str:
        return cls.get_model_identification_kwargs()[0]


class InstanceCacheMeta(type):
    """Metaclass that caches instances based on their initialization arguments.

    :param type: the metaclass type.
    :type type: type
    :return: the metaclass that caches instances.
    :rtype: InstanceCacheMeta
    """
    _instances = {}

    def clear_cache(cls):
        """Clear the instance cache."""
        cls._instances = {}

    def __call__(cls, *args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))

        if key not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[key] = instance

        return cls._instances[key]


class CombinedMeta(InstanceCacheMeta, ModelMetaclass):
    pass


class BaseProxyClient(ABC, BaseModel, metaclass=CombinedMeta):
    """Abstract base class for all proxy clients."""
    model_config = ConfigDict(
        protected_namespaces=()
    )

    @classmethod
    def refresh_instance_cache(cls):
        """Refresh the cache of instances."""
        InstanceCacheMeta.clear_cache(cls)

    @property
    @abstractmethod
    def request_header(self) -> Dict[str, Any]:
        ...

    @property
    @abstractmethod
    def deployments(self) -> Dict[str, Any]:
        ...

    @property
    @abstractmethod
    def deployment_class(self) -> Type[BaseDeployment]:
        ...

    @abstractmethod
    def select_deployment(self, **kwargs) -> BaseDeployment:
        ...
