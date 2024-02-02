from importlib import import_module
from operator import itemgetter
from typing import List

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable


class TestHarness:
    """Hosts the pipeline in a test harness, so we can inject chat history and input."""

    def __init__(self, pipeline: Runnable):
        context_variables = {
            "input": itemgetter("input"),
            "history": itemgetter("history"),
        }

        self._pipeline = context_variables | pipeline

        # Make sure we have a string output parser at the end of the pipeline.
        # We need this for the generate_response method to work correctly.
        if not isinstance(self._pipeline, StrOutputParser):
            self._pipeline = self._pipeline | StrOutputParser()

    def invoke(self, prompt: str, history: List[BaseMessage]) -> str:
        """
        Generates a response from the pipeline, given an input.

        Parameters:
        -----------
        prompt: str
            The input to the pipeline
        history: List[BaseMessage]
            The history of the conversation

        Returns:
        --------
        str
            The response from the pipeline
        """

        return self._pipeline.invoke({"input": prompt, "history": history})

    @staticmethod
    def create_from_path(pipeline_path: str) -> "TestHarness":
        """
        Creates a new test harness based on the pipeline path.

        The pipeline path is formed as <module_name>:<variable_name>.
        We'll import the <module_name> and then try to grab the <variable_name>.

        Parameters:
        -----------
        pipeline_path: str
            The path to the pipeline


        Returns:
        --------
        TestHarness
            The test harness
        """

        [module_name, variable_name] = pipeline_path.split(":")

        module_instance = import_module(module_name)
        pipeline_instance = getattr(module_instance, variable_name)

        return TestHarness(pipeline_instance)
