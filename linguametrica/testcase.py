"""A test case is a single test that can be run against a langchain pipeline."""

from enum import Enum
from os import PathLike
from typing import Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as

from linguametrica.harness import TestHarness
from linguametrica.metrics import Metric


class MessageRole(Enum):
    """Defines the role of a message in a conversation."""

    assistant = "assistant"
    user = "user"


class MessageData(BaseModel):
    """
    Defines a message in a conversation.

    Attributes:
    -----------
    content: str
        The content of the message
    role: MessageRole
        The role of the message
    """

    content: str
    role: MessageRole


class TestResult(BaseModel):
    """
    The test result of a test case is defined by a set of scores. One score per metric
    that was tested. If a test case fails, an error message is recorded. Otherwise, the
    error message is None.

    Note that some metrics may not be collected when an error occurs.

    Attributes:
    -----------
    scores: Dict[str, float]
        The scores of the metrics
    error: Optional[str]
        The error message, if any
    """

    scores: Dict[str, float]
    error: Optional[str]


class TestCase(BaseModel):
    """
    Defines a test case to run against a langchain pipeline.

    Attributes:
    -----------
    id: str
        The ID of the test case
    history: Optional[List[MessageData]]
        The history of the conversation
    input: Optional[str]
        The input to the pipeline
    output: str
        The expected output of the pipeline
    """

    id: str
    history: Optional[List[MessageData]] = None
    context: Optional[str] = None
    input: str
    output: Optional[str] = None

    @staticmethod
    def load(path: PathLike) -> "TestCase":
        """
        Load a test case from a file.

        Parameters:
        -----------
        path: str
            The path to the file to load the test case from

        Returns:
        --------
        TestCase
            The test case
        """

        with open(path, "r") as f:
            return parse_yaml_raw_as(TestCase, f.read())

    def run(self, metrics: List[Metric], harness: TestHarness) -> TestResult:
        """
        Runs the test case by generating a response using the input data for the test
        case and then measuring collecting the metrics.

        Parameters:
        -----------
        metrics: List[Metric]
            The metrics to collect
        harness: TestHarness
            The test harness to use to generate the response

        Returns:
        --------
        TestResult
            The result of the test case
        """
        try:
            history_messages = self._map_history() if self._has_history() else []
            response = harness.invoke(self.input, history_messages)

            scores = {}

            for metric in metrics:
                score = metric.collect(self.input, response, self.context)
                scores[metric.name] = score

            return TestResult(scores=scores, error=None)
        except Exception as e:  # noqa
            return TestResult(
                scores={}, error=f"Error while running the test case: {e}"
            )

    def _map_history(self) -> List[BaseMessage]:
        def map_message_data(message_data: MessageData) -> BaseMessage:
            if message_data.role == MessageRole.assistant:
                return AIMessage(content=message_data.content)
            elif message_data.role == MessageRole.user:
                return HumanMessage(content=message_data.content)
            else:
                raise ValueError(f"Unknown message role: {message_data.role}")

        if self.history is None or len(self.history) == 0:
            return []

        return [map_message_data(message_data) for message_data in self.history]

    def _has_history(self):
        return self.history is not None and len(self.history) > 0
