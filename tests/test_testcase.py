import os
from pathlib import Path

import pytest
from pydantic_yaml import to_yaml_file
from pytest_mock import MockFixture

from linguametrica.harness import TestHarness
from linguametrica.metrics import Metric
from linguametrica.testcase import TestCase, MessageData, MessageRole


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
def config_file(tmp_path):
    test_case_file = Path(tmp_path) / "test-case-1.yaml"

    test_case = TestCase(id="test-1", history=[], input="Hello, How are you?")
    to_yaml_file(test_case_file, test_case)

    yield test_case_file

    os.unlink(test_case_file)


def test_run_testcase(metric: Metric, test_harness: TestHarness):
    test_case = TestCase(id="test-1", history=[], input="Hello, How are you?")
    test_result = test_case.run([metric], test_harness)

    assert test_result is not None
    assert test_result.error is None
    assert test_result.scores["test"] == 0.5


def test_run_test_case_with_history(metric: Metric, test_harness: TestHarness):
    history = [
        MessageData(role=MessageRole.user, content="Hello"),
        MessageData(
            role=MessageRole.assistant, content="Hello, how can I help you today?"
        ),
    ]

    test_case = TestCase(id="test-1", history=history, input="Hello, How are you?")
    test_result = test_case.run([metric], test_harness)

    assert test_result is not None
    assert test_result.error is None
    assert test_result.scores["test"] == 0.5


def test_load_testcase(config_file: Path):
    test_case = TestCase.load(config_file)

    assert test_case.id == "test-1"
    assert test_case.input == "Hello, How are you?"
    assert len(test_case.history) == 0
