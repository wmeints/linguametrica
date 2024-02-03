"""The configuration models for the LainguaMetrica application."""

from enum import Enum
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as


class TestProviderKind(Enum):
    """Specifies the provider of the LLM used to collect metrics"""

    Azure = "Azure"
    OpenAI = "OpenAI"


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
    The .linguametrica.yml is a YAML file that contains the configuration for a
    LinguaMetrica project. It is used to configure the application kind, the
    module to be evaluated and the metrics to be used.

    You can specify a specific LLM provider to run the tests with. Please note that
    this is the provider used to collect the metrics. You configure your own
    LLM in the langchain application you're testing.

    Attributes:
    -----------
    kind: ApplicationKind
        The kind of application to be evaluated.
    module: str
        The module to be evaluated.
    metrics: str
        The metrics to be used.
    provider: TestProviderKind
        The provider for the LLM used to test the langchain application
    """

    kind: ApplicationKind
    module: str
    metrics: List[str]
    provider: Optional[TestProviderKind] = TestProviderKind.OpenAI

    @staticmethod
    def load(path: str) -> "ProjectConfig":
        """
        Loads a .linguametrica.yml from the given path.

        Parameters:
        -----------
        path: str
            The path to the .linguametrica.yml.

        Returns:
        --------
        Config
            The parsed .linguametrica.yml.

        Raises:
        -------
        FileNotFoundError
            If the .linguametrica.yml could not be found.
        """
        project_file = Path(path) / ".linguametrica.yml"

        if not project_file.exists():
            raise FileNotFoundError(f"Could not find .linguametrica.yml in {path}")

        with open(project_file, "r") as f:
            return parse_yaml_raw_as(ProjectConfig, f)
