# LinguaMetrica

![LinguaMetrica Logo](./images/linguametrica-logo.png)

A command-line tool to quickly evaluate your langchain application.
This tool allows you to load a dataset containing input samples and expected outputs, push the samples through the
language model and then measure various metrics.

---

**IMPORTANT** This is a work in progress. Very few metrics work, and I haven't tested all edge cases yet.

---

## Supported test cases

We support the following dataset types:

- Single input with a single output, suitable for testing LLM interactions
- Conversations with a single output, suitable for testing chat interactions
- Key/value pairs with a single output, suitable for testing custom workflows

## Installation

Currently, the project is not published to pypi. You can install the project by cloning the repository and then running
the following command:

```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

**Note:** On Windows Powershell you'll need to use `. .venv/Scripts/Activate.ps1` to activate the virtual environment.

## Usage

First, create a new dataset directory with a single file in the root of the directory
called `.linguametrica.yml`. This file should look like this:

```yaml
kind: ChatApplication
provider: Azure
metrics:
  - faithfulness
  - maliciousness
  - harmfulness
module: my_package.module:var
```

In the configuration file we've specified the following settings:

| Setting  | Description                                                            |
| -------- | ---------------------------------------------------------------------- |
| kind     | The kind of application we're testing (ChatApplication, KeyValue, LLM) |
| metrics  | The collection of metrics to evaluate                                  |
| module   | The path to the llm pipeline to evaluate                               |
| provider | The provider for the LLM used to collect metrics (Azure, OpenAI)       |

The path in the module setting has the format `<path-to-package>:<variable>`.
The module must exist in the python path for the tool to be able to load it.

After setting up the configuration file, you can create samples in the `data` directory
under the root directory of your project. This directory should contain yaml files
that specify the inputs and expected outputs.

Assuming that you have a langchain pipeline that looks like this:

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "<your-system-prompt>"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
chain = prompt_template | llm
```

You can create a yaml file in the `data` folder of your project that looks like this:

```yaml
id: <identifier>
history:
  - role: user|assistant
    content: <input|response>
context: <context>
input: <user-prompt>
output: the expected response
```

The test case defines the following properties:

| Property | Description                                                                       | Optional |
| -------- | --------------------------------------------------------------------------------- | -------- |
| id       | The identifier of the test case, this is used to identify the test case           | No       |
| history  | The history of the conversation, this is a list of messages                       | Yes      |
| context  | The context of the conversation, this is the retrieved content for a RAG pipeline | Yes      |
| input    | The input prompt to send to the model                                             | No       |
| output   | The expected output of the model                                                  | Yes      |

Most of the properties are optional, but make sure to check out the documentation of the individual metrics to
see which properties are required to collect the metric. If a metric can't be collected, it's left empty in the
report.

Once you have a set of test cases, you can start the tool like this:

```bash
linguametrica --project <directory> --report-file <output-file> --report-format json
```

The output file will contain a report with the measured metrics.

## Supported reporters

The following reporters are supported:

| Reporter name | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| json          | Requires `--report-file` to be set. Writes the report to a json file. |
| terminal      | Writes the report to the terminal.                                    |

## Supported metrics

We currently support the following metrics:

- Faithfulness
- Maliciousness
- Harmfulness

## Supported test providers

We use an LLM to collect the metrics for your langchain pipeline. Currently we support the following providers:

- Azure
- OpenAI

Please check the documentation for each of the providers to learn how to configure them.

## Developer documentation

This section covers various aspects around developing the application. You only need this information if you're planning
to contribute to the project.

### Running tests

Some test cases in this project are marked with `@pytest.mark.integration`. These tests require an internet connection
and a valid API key for the OpenAI API. You can run these tests by setting the `OPENAI_API_KEY` environment variable to
a valid API key and then running the tests with the following command:

```bash
poetry run pytest -k "integration"
```

You can run the unit-tests with the following command:

```bash
poetry run pytest -k "not integration"
```

## Special thanks

This project wouldn't be possible without the inspiration from the following projects and papers:

1. [Ragas](https://docs.ragas.io/en/latest/index.html)
2. [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/abs/2303.16634)
