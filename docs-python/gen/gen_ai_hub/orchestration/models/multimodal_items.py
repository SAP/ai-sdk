import base64
import mimetypes
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, Union

from gen_ai_hub.orchestration.models.base import JSONSerializable

class ImageDetailLevel(Enum):
    """
    Controls the resolution and detail level for image analysis.

    Attributes:
    
    - AUTO: The model determines the detail level automatically.

    - LOW: The model uses a low-fidelity, faster version of the image.

    - HIGH: The model uses a high-fidelity version of the image.
    """
    AUTO = "auto"
    LOW = "low"
    HIGH = "high"

@dataclass
class TextPart(JSONSerializable):
    """
    Represents a text segment within a multimodal content block.

    Args:
    
    - text: The string content of the text part.
    
    - type: The type identifier, defaulting to "text".
    """
    text: str
    type: str = field(default="text")

    def to_dict(self):
        """Converts the TextPart instance to a dictionary.

        :return: A dictionary representation of the TextPart.
        :rtype: dict
        """
        return {
            "type": self.type,
            "text": self.text,
        }


@dataclass
class ImageUrl:
    """
    A data structure holding the URL and detail level for an image.

    Args:
    
    - url: The location of the image, as a standard or data URL.
    
    - detail: The processing detail level for the image.
    """
    url: str
    detail: Optional[ImageDetailLevel] = None


@dataclass
class ImagePart(JSONSerializable):
    """
    Represents an image segment within a multimodal content block.

    Args:
    
    - image_url: An `ImageUrl` object containing the image's location and detail level.
    - type: The type identifier, defaulting to "image_url".
    """
    image_url: ImageUrl
    type: str = field(default="image_url")

    def to_dict(self):
        """Converts the ImagePart instance to a dictionary.

        :return: A dictionary representation of the ImagePart.
        :rtype: dict
        """
        base = {
            "type": self.type,
            "image_url": {
                "url": self.image_url.url,
            },
        }

        if self.image_url.detail:
            base["image_url"]["detail"] = self.image_url.detail

        return base


ContentPart = Union[TextPart, ImagePart]


class ImageItem(JSONSerializable):
    """
    Represents an image for use in multimodal messages.

    Examples:

    Using a standard URL
    img1 = ImageItem(url="https://example.com/image.png", detail=ImageDetailLevel.HIGH)

    Using a data URL
    img2 = ImageItem(url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...")
    """

    def __init__(
        self,
        url: Optional[str] = None,
        detail: Optional[ImageDetailLevel] = None,
    ):
        """Initializes an ImageItem instance.

        :param url: The image location as a standard or data URL, defaults to None
            
                    Standard URL example: 'https://example.com/image.png'

                    Data URL example: 'data:image/png;base64,...'
        :type url: Optional[str], optional
        :param detail: The image detail level for model processing, defaults to None
        :type detail: Optional[ImageDetailLevel], optional
        """
        self.url = url
        self.detail = detail

    @staticmethod
    def from_file(
        file_path: str,
        mime_type: Optional[str] = None,
        detail: Optional[ImageDetailLevel] = None,
    ) -> "ImageItem":
        """Creates an ImageItem from a local image file.

        :param file_path: Path to the image file.
        :type file_path: str
        :param mime_type: Explicit MIME type (e.g., 'image/png').
                          If not provided, the MIME type will be guessed from the file extension.
        :type mime_type: Optional[str], optional
        :param detail: The image detail level for model processing.
        :type detail: Optional[ImageDetailLevel], optional
        :raises ValueError: If the MIME type cannot be determined and is not provided.
        :raises FileNotFoundError: If the file does not exist.
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

    def to_dict(self) -> Dict[str, Any]:
        """Converts the ImageItem instance to a dictionary representation.

        :return: A dictionary representation of the ImageItem.
        :rtype: Dict[str, Any]
        """
        return ImagePart(image_url=ImageUrl(url=self.url, detail=self.detail)).to_dict()
