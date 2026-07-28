# pylint: disable=duplicate-code
"""
Models for representing multimodal content parts, including text and images.
"""

import base64
import mimetypes
from enum import Enum
from typing import Any, Optional, Union, Literal, Callable

from pydantic import Field
from pydantic.main import IncEx

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class ImageDetailLevel(Enum):
    """
    Controls the resolution and detail level for image analysis.

    Attributes:
        AUTO: The model determines the detail level automatically.

        LOW: The model uses a low-fidelity, faster version of the image.

        HIGH: The model uses a high-fidelity version of the image.
    """
    AUTO = "auto"
    LOW = "low"
    HIGH = "high"


class TextPart(BaseModel):
    """
    Represents a text segment within a multimodal content block.

    Args:
        text: The string content of the text part.

        type: The type identifier, defaulting to "text".
    """
    text: str
    type_: Literal["text"] = Field(default="text", alias="type")


class ImageUrl(BaseModel):
    """
    A data structure holding the URL and detail level for an image.

    Args:
        url: The location of the image, as a standard or data URL.

        detail: The processing detail level for the image.
    """
    url: str
    detail: Optional[ImageDetailLevel] = None


# @dataclass
class ImagePart(BaseModel):
    """
    Represents an image segment within a multimodal content block.

    Args:
        image_url: An `ImageUrl` object containing the image's location and detail level.

        type: The type identifier, defaulting to "image_url".
    """
    image_url: ImageUrl
    type_: Literal["image_url"] = Field(default="image_url", alias="type")


ContentPart = Union[TextPart, ImagePart]


class ImageItem(BaseModel):
    """
    Represents an image for use in multimodal messages.

    Args:
        url: The image location, specified as either a standard URL or a data URL.
            - Standard URL example: 'https://example.com/image.png'

            - Data URL example: 'data:image/png;base64,...'

        detail: The image detail level for model processing.

    Example:
        # Using a standard URL
        img1 = ImageItem(url="https://example.com/image.png", detail=ImageDetailLevel.HIGH)

        # Using a data URL
        img2 = ImageItem(url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...")
    """

    url: Optional[str] = None
    detail: Optional[ImageDetailLevel] = None

    @staticmethod
    def from_file(
            file_path: str,
            mime_type: Optional[str] = None,
            detail: Optional[ImageDetailLevel] = None,
    ) -> "ImageItem":
        """Create an ImageItem from a local image file.

        :param file_path: Path to the image file.
        :type file_path: str
        :param mime_type: Explicit MIME type (e.g., 'image/png').
            If not provided, the MIME type will be guessed from the file extension.
        :type mime_type: Optional[str], optional
        :param detail: The image detail level for model processing.
        :type detail: Optional[ImageDetailLevel], optional
        :raises ValueError: If the MIME type cannot be determined and is not provided.
        :return: An ImageItem instance with the image data as a data URL.
        :rtype: ImageItem
        """

        mime = mime_type or mimetypes.guess_type(file_path)[0]
        if not mime:
            raise ValueError(
                f"Could not determine MIME type for file: {file_path}. "
                "Please provide mime_type explicitly."
            )
        with open(file_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("utf-8")
        data_url = f"data:{mime};base64,{encoded}"

        return ImageItem(url=data_url, detail=detail)

    def model_dump(  # pylint: disable=arguments-differ
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx | None = None,
            exclude: IncEx | None = None,
            context: Any | None = None,
            by_alias: bool = True,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool | Literal['none', 'warn', 'error'] = True,
            fallback: Callable[[Any], Any] | None = None,
            serialize_as_any: bool = False,
    ) -> dict[str, Any]:    
        return ImagePart(image_url=ImageUrl(url=self.url, detail=self.detail)).model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )

__all__ = ["ImageDetailLevel", "TextPart", "ImageUrl", "ImagePart", "ContentPart", "ImageItem"]