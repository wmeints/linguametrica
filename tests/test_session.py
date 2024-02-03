import shutil
from pathlib import Path

import pytest
from pydantic_yaml import to_yaml_file
from pytest_mock import MockFixture

from linguametrica.config import ApplicationKind, ProjectConfig
from linguametrica.harness import TestHarness
from linguametrica.metrics import Metric
from linguametrica.session import Session
from linguametrica.testcase import TestCase


@pytest.fixture
def metric(mocker: MockFixture) -> Metric:
    metric_instance = mocker.MagicMock()
    metric_instance.collect.return_value = 0.5

    name_property = mocker.PropertyMock(return_value="test")
    type(metric_instance).name = name_property

    return metric_instance


@pytest.fixture
def test_harness(mocker: MockFixture) -> TestHarness:
    harness_instance = mocker.MagicMock()
    harness_instance.invoke.return_value = "Hello, How are you?"

    return harness_instance


@pytest.fixture
def test_case() -> TestCase:
    return TestCase(id="test-1", history=[], input="Hello, How are you?")


@pytest.fixture
def project_config(tmp_path):
    project_directory = Path(tmp_path) / "test-project"
    project_data_directory = project_directory / "data"

    project_directory.mkdir(parents=True, exist_ok=True)
    project_data_directory.mkdir(parents=True, exist_ok=True)

    config = ProjectConfig(
        kind=ApplicationKind.ChatApplication,
        module="tests.sample_pipeline:pipeline",
        metrics=["harmfulness"],
    )

    test_case = TestCase(id="test-1", history=[], input="Hello, How are you?")

    to_yaml_file(project_directory / "LinguaMetricaFile", config)
    to_yaml_file(project_data_directory / "test-1.yml", test_case)

    yield str(project_directory)

    shutil.rmtree(project_directory)


def test_load_session(project_config: str):
    session = Session.from_directory(project_config)

    assert len(session.test_cases) == 1
    assert len(session.metrics) == 1
    assert session.harness is not None


def test_run_session(test_case, metric, test_harness):
    session = Session(
        ProjectConfig(
            kind=ApplicationKind.ChatApplication,
            module="tests.sample_pipeline:pipeline",
            metrics=["test"],
        ),
        test_harness,
        [metric],
        [test_case],
    )

    results = session.run()

    assert results is not None
