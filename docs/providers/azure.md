# Azure OpenAI Service

This section covers how to use the Azure OpenAI service as a provider for collecting LLM metrics.
Please make sure you have deployed an instance of the Azure OpenAI in your subscription before proceeding.

## Configuration

Please configure the following environment variables to use the Azure Provider:

| Environment Variable  | Description                                                                           |
|-----------------------|---------------------------------------------------------------------------------------|
| AZURE_OPENAI_API_KEY  | The API key found in the Azure OpenAI resource configuration on the Azure Portal      |
| AZURE_OPENAI_ENDPOINT | The endpoint URL found in the Azure OpenAI resource configuration on the Azure Portal |
| AZURE_OPENAI_MODEL    | The name of a deployment of GPT 3.5 Turbo or GPT-4 on Azure OpenAI.                   |

You can use a `.env` file to store these environment variables.