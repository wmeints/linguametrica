import os
from pathlib import Path

import pytest

from linguametrica.config import OutputConfig
from linguametrica.reporter import JsonReporter
from linguametrica.session import SessionSummary, MetricSummary
from datetime import timedelta


@pytest.fixture
def output_path(tmp_path):
    value = tmp_path / "report.json"
    yield value
    os.unlink(value)


def test_json_reporter(output_path):
    reporter = JsonReporter(
        OutputConfig(output_path=str(output_path), output_format="json")
    )

    reporter.generate_report(
        SessionSummary(
            metrics=[MetricSummary(name="test", min=0, max=1, mean=0.5)],
            test_cases=1,
            failed_cases=0,
            duration=timedelta(seconds=15),
        )
    )

    assert Path(output_path).exists()
