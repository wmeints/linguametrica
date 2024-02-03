import json
from abc import ABC, abstractmethod
from pathlib import Path

from linguametrica.config import OutputConfig
from linguametrica.session import SessionSummary


class Reporter(ABC):
    """
    Reports the output of a session.
    """

    def __init__(self, config: OutputConfig):
        self.config = config

    @abstractmethod
    def generate_report(self, summary: SessionSummary) -> None:
        """
        Generates a session report

        Parameters:
        -----------
        summary: SessionSummary
            The summary of the session
        """
        raise NotImplementedError()


class ConsoleReporter(Reporter):
    """
    Reports the output of a session to the console.
    """

    def __init__(self, config: OutputConfig):
        super().__init__(config)

    def generate_report(self, summary: SessionSummary) -> None:
        print(summary)


class JsonReporter(Reporter):
    """Reports session results as a JSON file"""

    def __init__(self, config: OutputConfig):
        super().__init__(config)

    def generate_report(self, summary: SessionSummary) -> None:
        """
        Generates a JSON report from the session summary.

        Parameters:
        -----------
        summary: SessionSummary
            The summary of the session

        Raises:
        -------
        NotADirectoryError
            If the output path does not exist
        ValueError
            If the output path is not provided
        """

        if self.config.output_path is None or self.config.output_path.strip() == "":
            raise ValueError("Output path is required")

        output_path = Path(self.config.output_path.strip())

        if not output_path.parent.exists():
            raise NotADirectoryError(
                f"The directory {output_path.parent} does not exist"
            )

        with open(output_path, "w") as f:
            json.dump(summary.model_dump(), f, indent=4)


def get_reporter(output_config: OutputConfig) -> Reporter:
    """
    Creates a reporter based on the provided output_format.

    Parameters:
    -----------
    output_format: str
        The output format to use.
    """

    if output_config.output_format == "terminal":
        return ConsoleReporter(output_config)
    elif output_config.output_format == "json":
        return JsonReporter(output_config)
    else:
        raise ValueError(f"Unsupported output format: {output_config.output_format}")
