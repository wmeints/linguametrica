"""The CLI interface for the LinguaMetrica application."""

from typing import Annotated, Optional

import typer

from linguametrica.config import OutputConfig
from linguametrica.reporter import get_reporter
from linguametrica.session import Session

app = typer.Typer(help="Langchain application evaluation")


@app.command()
def analyze_performance(
    path: Annotated[str, typer.Option(help="The path to the evaluation data")],
    report_file: Annotated[
        Optional[str],
        typer.Option(
            help="The output path for the evaluation run",
        ),
    ] = None,
    report_format: Annotated[
        str,
        typer.Option(
            help="The format for the output file.",
        ),
    ] = "terminal",  # noqa
):
    """
    Analyze the performance of a langchain application.
    """
    output_config = OutputConfig(output_path=report_file, output_format=report_format)

    reporter = get_reporter(output_config)
    session = Session.from_directory(path)
    outcome = session.run()

    reporter.generate_report(outcome)


def main():
    """Runs the application"""
    app()
