import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAI
load_dotenv()


client = AzureChatOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    # model = os.getenv("AZURE_OPENAI_MODEL_NAME"),
    # temperature = 0.7,
    # top_p = 0.95,
    # max_tokens = 800,
    timeout = None
)

