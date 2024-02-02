import pytest
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

from linguametrica.harness import TestHarness

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a digital assistant, you're here to help me write interesting content.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ]
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="sk-1234")
pipeline = prompt_template | llm


def test_create_test_harness():
    harness = TestHarness.create_from_path("tests.test_harness:pipeline")

    assert harness is not None
    assert harness._pipeline is not None


@pytest.mark.integration
def test_can_invoke_pipeline():
    harness = TestHarness.create_from_path("tests.test_harness:pipeline")
    messages = [HumanMessage(content="Is this thing on?")]

    result = harness.invoke("Test, how are you?", [])

    assert result is not None
