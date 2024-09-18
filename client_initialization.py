import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
load_dotenv()


client = AzureChatOpenAI(
    # azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
    api_key = os.environ['AZURE_OPENAI_API_KEY'],
    openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"],
    # azure_deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    temperature = 0.7,
    top_p = 0.95,
    max_tokens = 800,
    timeout = None
)

