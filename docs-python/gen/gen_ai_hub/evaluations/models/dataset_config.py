from pathlib import Path
from typing import Union, Optional
from gen_ai_hub.evaluations.models.artifact_source import ArtifactSource
from gen_ai_hub.evaluations.constants import (
    SUFFIX_TO_FILE_TYPE,
)


class Dataset:
    """Dataset object for the evaluations flow.

    The Dataset class accepts various source types for evaluation datasets including
    local file paths (as strings or Path objects) or AI Core artifacts.

    :param source: Source of the dataset - can be a file path string, Path object, or ArtifactSource
    :type source: Union[str, Path, ArtifactSource]

    **Examples**:

    Using a Path object:

    >>> Dataset(Path("data/sample.json"))

    Using a string path:

    >>> Dataset("data/sample.json")

    Using an ArtifactSource with artifact dictionary:

    >>> Dataset(
    ...     ArtifactSource(
    ...         artifact={
    ...             "id": "xyfz-rtyu-2456-ojns-yu6s",
    ...             "name": "dataset-artifact",
    ...             "url": "ai://default/eval_dataset"
    ...         },
    ...         path="rootfolder/data.csv",
    ...         file_type="csv"
    ...     )
    ... )

    Using an ArtifactSource with artifact ID:

    >>> Dataset(
    ...     ArtifactSource(
    ...         artifact="xyfz-rtyu-2456-ojns-yu6s",
    ...         path="rootfolder/data.csv",
    ...         file_type="csv"
    ...     )
    ... )
    """

    def __init__(self, source: Union[str, Path, ArtifactSource]):
        """Initialize a Dataset instance.

        :param source: Source of the dataset - can be a file path string, Path object, or ArtifactSource
        :type source: Union[str, Path, ArtifactSource]
        """
        self.source = source

    @property
    def file_type(self) -> Optional[str]:
        """Infer the file type from the source.

        For ArtifactSource, returns the explicitly set file_type.
        For file paths, infers the type from the file extension.

        :return: File type (e.g., "json", "jsonl", "csv") or None if cannot be determined
        :rtype: Optional[str]
        """
        if isinstance(self.source, ArtifactSource):
            return self.source.file_type

        # If source is a path or string, try inferring from file extension
        path_str = str(self.source) if isinstance(self.source, Path) else self.source
        suffix = Path(path_str).suffix.lower()

        return SUFFIX_TO_FILE_TYPE.get(suffix, None)

__all__ = ["Dataset"]