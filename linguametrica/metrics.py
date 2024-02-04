"""The metrics used to evaluate the performance of the langchain pipeline."""

from abc import ABC, abstractmethod
from operator import itemgetter
from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from linguametrica.config import ProjectConfig
from linguametrica.llm import create_llm, read_template


class Metric(ABC):
    """
    A metric can be collected as part of a test case. It's a way to measure the
    performance of a langchain pipeline.
    """

    @abstractmethod
    def init(self, project_config: ProjectConfig):
        """
        Initializes the metric with the given project configuration

        Parameters:
        -----------
        project_config: ProjectConfig
            The configuration for the project
        """
        raise NotImplementedError()

    @abstractmethod
    def collect(
        self, prompt: str, output: str, context: Optional[str]
    ) -> Optional[float]:
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
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self) -> str:
        """Gets the descriptive name of the metric"""
        raise NotImplementedError()


class AspectCritiqueMetric(Metric, ABC):
    """
    A metric that evaluates a specific aspect of the generated response.

    Attributes:
    -----------
    aspect: str
        The aspect of the response that the metric evaluates
    """

    aspect: str
    _pipeline: Runnable

    def init(self, project_config: ProjectConfig):
        """
        Initializes the metric with the given project configuration

        Parameters:
        -----------
        project_config: ProjectConfig
            The configuration for the project
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", read_template("critique")),
            ]
        )

        context_variables = {
            "criteria": itemgetter("criteria"),
            "input": itemgetter("input"),
            "response": itemgetter("response"),
        }

        llm = create_llm(project_config)

        self._pipeline = context_variables | prompt_template | llm | StrOutputParser()

    def collect(
        self, prompt: str, output: str, context: Optional[str]
    ) -> Optional[float]:
        """
        Collects the value for the metric harmfulness by invoking the LLM.

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
        try:
            response = self._pipeline.invoke(
                {
                    "input": prompt,
                    "response": output,
                    "criteria": read_template(self.aspect),
                }
            )
        except:  # noqa
            return None

        return float(response)

    @property
    def name(self) -> str:
        return self.aspect


class HarmfulnessMetric(AspectCritiqueMetric):
    """Calculates how harmful the generated response is."""

    aspect = "harmfulness"


class MaliciousnessMetric(AspectCritiqueMetric):
    """Calculates how malicious or deceiving the generated response is."""

    aspect = "maliciousness"


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
    if name == "maliciousness":
        return MaliciousnessMetric()
    else:
        raise ValueError(f"Unknown metric: {name}")
