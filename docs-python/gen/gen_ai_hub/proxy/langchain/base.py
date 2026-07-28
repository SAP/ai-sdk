from typing import Any, Optional

from pydantic import BaseModel

from gen_ai_hub.proxy.core import get_proxy_client

_VALUES = [('proxy_model_name', 'model_name'), ('deployment_id', 'deployment_id'), ('config_id', 'config_id'),
           ('config_name', 'config_name')]


class BaseAuth(BaseModel):
    """Base class for authentication models.

    :param BaseModel: The base model class to inherit from.
    :type BaseModel: pydantic.BaseModel
    :return: An instance of the BaseAuth class.
    :rtype: BaseAuth
    """
    proxy_client: Optional[Any] = None  #: :meta private:
    deployment_id: Optional[str] = None
    config_name: Optional[str] = None
    config_id: Optional[str] = None
    proxy_model_name: Optional[str] = None

    @classmethod
    def _get_proxy_client(cls, values):
        return values.get('proxy_client', None) or get_proxy_client()

    @staticmethod
    def _set_deployment_parameters(values, deployment):
        for key_values, key_deployment in _VALUES:
            if hasattr(deployment, key_deployment):
                values[key_values] = getattr(deployment, key_deployment)
