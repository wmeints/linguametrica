import pytest

from linguametrica.config import ApplicationKind, ProjectConfig
from linguametrica.metrics import HarmfulnessMetric


@pytest.fixture
def project_config() -> ProjectConfig:
    return ProjectConfig(
        kind=ApplicationKind.ChatApplication,
        module="tests.test_session:pipeline",
        metrics=["harmfulness"],
    )


@pytest.mark.integration
def test_harmfulness_metric(project_config: ProjectConfig):
    metric = HarmfulnessMetric()
    metric.init(project_config)

    score = metric.collect(prompt="Test", output="test", context="")

    assert score is not None
    assert score >= 0.0 and score <= 1.0
