"""The configuration models for the LainguaMetrica application."""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as


class ApplicationKind(Enum):
    """
    The kind of application to be evaluated.
    """

    ChatApplication = "ChatApplication"
    LLM = "LLM"
    KeyValue = "KeyValue"


class OutputConfig(BaseModel):
    """
    The output configuration defines where the results of the session should be
    saved. It also specifies the output format for the session results.

    Attributes:
    -----------
    output_path: str
        The path to the output directory.
    output_format: str
        The format for the output file.
    """

    output_path: str
    output_format: str


class ProjectConfig(BaseModel):
    """
    The LinguaMetricaFile is a YAML file that contains the configuration for a
    LinguaMetrica project. It is used to configure the application kind, the
    module to be evaluated and the metrics to be used.

    Attributes:
    -----------
    kind: ApplicationKind
        The kind of application to be evaluated.
    module: str
        The module to be evaluated.
    metrics: str
        The metrics to be used.
    """

    kind: ApplicationKind
    module: str
    metrics: str

    @staticmethod
    def load(path: str) -> "ProjectConfig":
        """
        Loads a LinguaMetricaFile from the given path.

        Parameters:
        -----------
        path: str
            The path to the LinguaMetricaFile.

        Returns:
        --------
        Config
            The parsed LinguaMetricaFile.

        Raises:
        -------
        FileNotFoundError
            If the LinguaMetricaFile could not be found.
        """
        project_file = Path(path) / "LinguaMetricaFile"

        if not project_file.exists():
            raise FileNotFoundError(f"Could not find LinguaMetricaFile in {path}")

        with open(project_file, "r") as f:
            return parse_yaml_raw_as(ProjectConfig, f)
