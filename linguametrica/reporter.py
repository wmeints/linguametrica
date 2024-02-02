from abc import ABC, abstractmethod

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


def get_reporter(output_config: OutputConfig) -> Reporter:
    """
    Creates a reporter based on the provided output_format.

    Parameters:
    -----------
    output_format: str
        The output format to use.
    """
    return ConsoleReporter(output_config)
