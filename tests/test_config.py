import pytest
from pydantic import ValidationError

from linguametrica.config import OutputConfig


def test_invalid_json_output_directory():
    with pytest.raises(ValidationError):
        OutputConfig(
            output_format="json", output_path="/some-path/that-does-not-exist.json"
        )


def test_invalid_json_output_filename(tmp_path):
    output_path = tmp_path

    with pytest.raises(ValidationError):
        OutputConfig(output_format="json", output_path=str(output_path))
