"""The CLI interface for the LinguaMetrica application."""

from pathlib import Path
from typing import Annotated

import typer

from linguametrica.config import OutputConfig, ProjectConfig
from linguametrica.reporter import get_reporter
from linguametrica.session import Session

app = typer.Typer(help="Langchain application evaluation")


@app.command()
def analyze_performance(
    path: Annotated[str, typer.Option(help="The path to the evaluation data")],
    output: Annotated[str, typer.Option(help="The output path for the evaluation run")],
    format: Annotated[
        str, typer.Option(help="The format for the output file.")
    ],  # noqa
):
    """
    Analyzes the performance of a given application.

    Parameters:
    -----------
    path: str
        The path to the evaluation data.
    output: str
        The output path for the evaluation run.
    format: str
        The format for the output file.
    """
    project_config = ProjectConfig.load(path)
    output_config = OutputConfig(output_path=output, output_format=format)

    reporter = get_reporter(output_config)
    session = Session(Path(path).absolute(), project_config)
    outcome = session.run()

    reporter.generate_report(outcome)


def main():
    """Runs the application"""
    app()
