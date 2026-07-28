"""
A base model class that extends Pydantic's BaseModel and ABC.
"""

from abc import ABC

from pydantic import BaseModel, ConfigDict


class ABCBaseModel(BaseModel, ABC):
    """
    Abstract base model that extends Pydantic's BaseModel and ABC.

    - `extra="forbid"` prevents unexpected fields from being accepted or sent,
      since the external API is strict about allowed parameters.
    - `exclude_none=True` ensures optional fields that were not provided are
      omitted from the payload instead of being serialized as None.
    - `by_alias=True` guarantees aliases are used during serialization, which is
      required because some API field names conflict with Pydantic's built-ins.

    This enforces consistent and safe serialization behavior across all
    derived models.
    """
    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
    )

    def model_dump(self, **kwargs):
        """Dumps the model to a dictionary with default settings."""
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)
