import pytest

from linguametrica.config import ApplicationKind, ProjectConfig
from linguametrica.metrics import HarmfulnessMetric, MaliciousnessMetric, get_metric


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
    assert 0.0 <= score <= 1.0


@pytest.mark.integration
def test_maliciousness_metric(project_config: ProjectConfig):
    metric = MaliciousnessMetric()
    metric.init(project_config)

    score = metric.collect(prompt="Test", output="test", context="")

    assert score is not None
    assert 0.0 <= score <= 1.0


def test_get_metric():
    supported_metrics = {
        "harmfulness": HarmfulnessMetric,
        "maliciousness": MaliciousnessMetric,
    }

    for metric_name, metric_type in supported_metrics.items():
        assert get_metric(metric_name) is not None
        assert isinstance(get_metric(metric_name), metric_type)
