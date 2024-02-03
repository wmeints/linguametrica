from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a digital assistant, you're here to help me write stuff.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo")
pipeline = prompt_template | llm
