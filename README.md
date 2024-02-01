# LinguaMetrica

A command-line tool to quickly evaluate your langchain application.
This tool allows you to load a dataset containing input samples and expected outputs, push the samples through the
language model and then measure various metrics.

## Supported test cases

We support the following dataset types:

- Single input with a single output, suitable for testing LLM interactions
- Conversations with a single output, suitable for testing chat interactions
- Key/value pairs with a single output, suitable for testing custom workflows

## Usage

First, create a new dataset directory with a single file in the root of the directory
called `LinguaMetricaFile`. This file should look like this:

```yaml
kind: ChatApplication
metrics:
  - faithfulness
  - maliciousness
  - harmfulness
module: my_package.module:var
```

In the configuration file we've specified the following settings:

| Setting | Description                                                            |
|---------|------------------------------------------------------------------------|
| kind    | The kind of application we're testing (ChatApplication, KeyValue, LLM) |
| metrics | The collection of metrics to evaluate                                  |
| module  | The path to the llm pipeline to evaluate                               |

The path in the module setting has the format `<path-to-package>:<variable>`.
The module must exist in the python path for the tool to be able to load it.

After setting up the configuration file, you can create samples in the `data` directory
under the root directory of your project. This directory should contain yaml files
that specify the inputs and expected outputs.

Assuming that you have a model pipeline that looks like this:

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

You can create a yaml test case that looks like this:

```yaml
id: <identifier>
history:
  - role: user|assistant
    content: <input|response>
input: <user-prompt>
output: the expected response
```

You can have multiple messages that each specify a role and the content of the message.
The output is a single string containing the expected response from the model.

Make sure you give each sample an identifier, this can be a GUID or a descriptive name.
It helps when you need to debug the application at a later point.

Once you have a set of test cases, you can start the tool like this:

```bash
linguametrica --project <directory> --output <output-file> --format json
```

The output file will contain a report with the measured metrics.

## Supported metrics

We currently support the following metrics:

- Faithfulness
- Maliciousness
- Harmfulness
