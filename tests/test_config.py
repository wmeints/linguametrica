import pytest
from pydantic import ValidationError

from linguametrica.config import OutputConfig, ProjectConfig, ApplicationKind


def test_invalid_json_output_directory():
    with pytest.raises(ValidationError):
        OutputConfig(
            output_format="json", output_path="/some-path/that-does-not-exist.json"
        )


def test_invalid_json_output_filename(tmp_path):
    output_path = tmp_path

    with pytest.raises(ValidationError):
        OutputConfig(output_format="json", output_path=str(output_path))


def test_valid_project_config():
    config = ProjectConfig(
        kind=ApplicationKind.ChatApplication,
        metrics=["harmfulness"],
        module="test.module:test.pipeline",
        provider="Azure",
    )


def test_project_config_invalid_metric():
    with pytest.raises(ValidationError):
        ProjectConfig(
            kind=ApplicationKind.ChatApplication,
            metrics=["test-invalid"],
        )


def test_project_config_no_metrics():
    with pytest.raises(ValidationError):
        ProjectConfig(
            kind=ApplicationKind.ChatApplication,
            metrics=[],
        )
