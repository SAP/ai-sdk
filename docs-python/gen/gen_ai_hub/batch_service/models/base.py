from abc import ABC

from pydantic import BaseModel, ConfigDict


class ABCBaseModel(BaseModel, ABC):
    """
    Abstract base model for batch service request models.

    - `extra="forbid"` rejects unexpected fields.
    - `by_alias=True` / `exclude_none=True` ensure clean API payloads.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=False,
    )

    def model_dump(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)


class ResponseBaseModel(BaseModel):
    """Base model for API response models — allows extra fields for forward compatibility."""

    model_config = ConfigDict(
        extra="allow",
        frozen=False,
    )
