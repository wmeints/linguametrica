from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from pydantic import BaseModel

from linguametrica.config import ProjectConfig
from linguametrica.harness import TestHarness
from linguametrica.metrics import Metric, get_metric
from linguametrica.testcase import TestCase, TestResult


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
        The duration of the session from the time the test cases were collected to the
        time the test cases were completed.
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
    test_results: List[TestResult]
    test_cases: List[TestCase]
    metrics: List[Metric]

    def __init__(
        self,
        project_config: ProjectConfig,
        harness: TestHarness,
        metrics: List[Metric],
        test_cases: List[TestCase],
    ):
        self.project_config = project_config
        self.harness = harness
        self.test_cases = test_cases
        self.metrics = metrics

    def run(self) -> SessionSummary:
        """
        Run the session. This will perform all the steps necessary to analyze the
        performance of the langchain pipeline.

        Returns:
        --------
        SessionSummary
            The summary of the session
        """

        for metric in self.metrics:
            metric.init(self.project_config)

        self.start_time = datetime.utcnow()
        self._run_test_cases()
        self.end_time = datetime.utcnow()

        return self._build_summary()

    @staticmethod
    def from_directory(project_directory: str) -> "Session":
        """
        Creates a new session based on a directory containing a project

        Parameters:
        -----------
        project_directory: str
            The directory containing the project

        Returns:
        --------
        Session
            The session
        """
        project_config = ProjectConfig.load(project_directory)
        test_cases = Session._load_project_data(Path(project_directory))
        test_harness = TestHarness.create_from_path(project_config.module)
        metrics = Session._load_metrics(project_config)

        return Session(project_config, test_harness, metrics, test_cases)

    @staticmethod
    def _load_project_data(root_directory: Path) -> List[TestCase]:
        data_directory = root_directory / "data"

        test_cases = [
            TestCase.load(test_case_file) for test_case_file in data_directory.iterdir()
        ]

        return test_cases

    @staticmethod
    def _load_metrics(project_config: ProjectConfig):
        metrics = [get_metric(metric_name) for metric_name in project_config.metrics]

        return metrics

    def _run_test_cases(self):
        test_results = []

        # Collect test results into a list
        for test_case in self.test_cases:
            test_results.append(test_case.run(self.metrics, self.harness))

        self.test_results = test_results

    def _build_summary(self):
        def calculate_metric_summaries():
            for metric_name in self.project_config.metrics:
                metric_results = [
                    result.scores[metric_name] for result in self.test_results
                ]

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
