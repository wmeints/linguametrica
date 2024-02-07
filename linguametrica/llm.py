"""The internal LLM used for testing the langchain pipeline."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.runnables import Runnable
from langchain_openai.chat_models import AzureChatOpenAI, ChatOpenAI


def read_template(name: str) -> str:
    """
    Reads a prompt template from the package.

    Parameters:
    -----------
    name: str
        The name of the template

    Returns:
    --------
    str
        The template
    """
    template_path = Path(__file__).parent / "templates" / f"{name}.txt"

    with open(template_path, "r") as f:
        return f.read()


def create_llm(provider: str) -> Runnable:
    """
    Creates the LLM model to use for testing the langchain pipeline.

    Parameters:
    -----------
    config: ProjectConfig
        The configuration for the project

    Returns:
    --------
    Runnable
        The LLM model to use for testing the langchain pipeline
    """
    load_dotenv()

    if provider == "OpenAI":
        return ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        )
    elif provider == "Azure":
        return AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_MODEL", ""),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
