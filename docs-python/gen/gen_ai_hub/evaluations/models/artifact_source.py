from typing import Optional, Union
from typing_extensions import Literal
from ai_api_client_sdk.models.artifact import Artifact


class ArtifactSource:
    """
    Extends the artifact object with the relative path user can provide inside to be used for EvaluationConfig
    Example Usage:
        >>> ArtifactSource(
                artifact={
                    "id": "xyfz-rtyu-2456-ojns-yu6s",
                    "name": "dataset-artifact",
                    "url": "ai://default/eval_dataset"
                    ...
                },
                path= "rootfolder/data.csv,
                file_type="csv"
            )
        >>> ArtifactSource(
                artifact="xyfz-rtyu-2456-ojns-yu6s",
                path="rootfolder/data.json,
                file_type="json"
            )
        )
    """

    def __init__(
        self,
        file_type: Literal["csv", "json", "jsonl"],
        artifact: Union[str,Artifact], # str is id
        path: Optional[str] = None,
    ):
        """
        Parameters:
            artifact(Union[str,Artifact]): Can just provide the artifact id as a string or the Artifact object of the AI_API_Client sdk.
            path(Optional[str]): Relative path within the artifact path provided and should point to a single file.
            file_type(Literal["csv", "json", "jsonl"]): One of the supported file_types
        """
        self.artifact = artifact
        self.path = path
        self.file_type = file_type

__all__ = ["ArtifactSource"]