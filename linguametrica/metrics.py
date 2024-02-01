from abc import ABC, abstractmethod
from typing import Optional


class Metric(ABC):
    """
    A metric can be collected as part of a test case. It's a way to measure the performance of a langchain pipeline.
    """

    @abstractmethod
    def collect(self, prompt: str, output: str, context: Optional[str]) -> Optional[float]:
        """
        Collects the value for the metric

        Parameters:
        -----------
        prompt: str
            The prompt that was used to generate the response
        output: str
            The response that was generated
        context: Optional[str]
            The context that was used to generate the output

        Returns:
        --------
        Optional[float]
            The value of the metric, or None if the metric could not be collected
        """
        raise NotImplemented

    @property
    @abstractmethod
    def name(self) -> str:
        """Gets the descriptive name of the metric"""
        raise NotImplemented


class HarmfulnessMetric(Metric):
    """Calculates how harmful the generated response is."""
    @property
    def name(self) -> str:
        return "harmfulness"

    def collect(self, prompt: str, output: str, context: Optional[str]) -> Optional[float]:
        return 0.0


def get_metric(name: str) -> Metric:
    """
    Gets the metric with the given name.

    Parameters:
    -----------
    name: str
        The name of the metric

    Returns:
    --------
    Metric
        The metric
    """

    if name == "harmfulness":
        return HarmfulnessMetric()
    else:
        raise ValueError(f"Unknown metric: {name}")