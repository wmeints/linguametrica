from datetime import timedelta, datetime
from os import PathLike
from pathlib import Path
from typing import List

from pydantic import BaseModel

from linguametrica.config import ProjectConfig
from linguametrica.harness import TestHarness
from linguametrica.metrics import get_metric
from linguametrica.testcase import TestCase


class MetricSummary(BaseModel):
    """
    Contains summary information about a metric after it's been collected.

    Attributes:
    -----------
    name: str
        The name of the metric
    mean: float
        The mean value of the metric
    max: float
        The maximum value of the metric
    min: float
        The minimum value of the metric
    """
    name: str
    mean: float
    max: float
    min: float


class SessionSummary(BaseModel):
    """
    Contains information about the session after it's completed.

    Attributes:
    -----------
    metrics: List[MetricSummary]
        The summarized metrics of the session.
    duration: timedelta
        The duration of the session from the time the test cases were collected to the time the test cases
        were completed.
    """
    metrics: List[MetricSummary]
    duration: timedelta


class Session:
    """
    A session is a single run of the linguametrica program. It is the top-level
    object that orchestrates the entire process.

    A session is created with a project configuration and an output configuration.
    The project configuration contains the information about the project to be
    analyzed, and the output configuration contains the information about where
    the output should be written to.

    Attributes:
    -----------
    project_config: ProjectConfig
        The project configuration
    """

    project_config: ProjectConfig
    start_time: datetime
    end_time: datetime

    def __init__(self, root_directory: Path, project_config: ProjectConfig):
        self.project_config = project_config
        self.root_directory = root_directory

    def run(self) -> SessionSummary:
        """
        Run the session. This will perform all the steps necessary to analyze the performance of the langchain pipeline.

        Returns:
        --------
        SessionSummary
            The summary of the session
        """

        self.start_time = datetime.utcnow()

        self._load_project_data()
        self._load_test_harness()
        self._load_metrics()

        self._run_test_cases()

        self.end_time = datetime.utcnow()

        return self._build_summary()

    def _load_project_data(self):
        data_directory = self.root_directory / "data"

        test_cases = []

        for _, _, files in data_directory.iterdir():
            test_cases = test_cases + [TestCase.load(file) for file in files]

        self.test_cases = test_cases

    def _load_test_harness(self):
        self._harness = TestHarness.create_from_path(self.project_config.module)

    def _load_metrics(self):
        self.metrics = [get_metric(metric_name) for metric_name in self.project_config.metrics]

    def _run_test_cases(self):
        test_results = []

        # Collect test results into a list
        for test_case in self.test_cases:
            test_results.append(test_case.run(self.metrics, self._harness))

        self.test_results = test_results

    def _build_summary(self):
        def calculate_metric_summaries():
            for metric_name in self.project_config.metrics:
                metric_results = [result.metrics[metric_name] for result in self.test_results]

                yield MetricSummary(
                    name=metric_name,
                    mean=sum(metric_results) / len(metric_results),
                    max=max(metric_results),
                    min=min(metric_results),
                )

        return SessionSummary(
            metrics=list(calculate_metric_summaries()),
            duration=self.end_time - self.start_time,
        )
