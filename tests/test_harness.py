import pytest
from langchain_core.messages import HumanMessage

from linguametrica.harness import TestHarness


def test_create_test_harness():
    harness = TestHarness.create_from_path("tests.sample_pipeline:pipeline")

    assert harness is not None
    assert harness._pipeline is not None


@pytest.mark.integration
def test_can_invoke_pipeline():
    harness = TestHarness.create_from_path("tests.sample_pipeline:pipeline")
    messages = [HumanMessage(content="Is this thing on?")]

    result = harness.invoke("Test, how are you?", messages)

    assert result is not None
