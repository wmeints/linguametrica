# OpenAI

This section covers how to use the OpenAI API as a provider for collecting LLM metrics.
Please make sure you have generated an API key through the [OpenAI dashboard](https://platform.openai.com/api-keys).

## Configuration

Please configure the following environment variables to use the OpenAI Provider:

| Environment Variable | Description                                                                      |
|----------------------|----------------------------------------------------------------------------------|
| OPENAI_API_KEY       | The API key found in the Azure OpenAI resource configuration on the Azure Portal |
| OPENAI_MODEL         | The identifier of the model (gpt-3.5-turbo or gpt-4)                             |

You can use a `.env` file to store these environment variables.