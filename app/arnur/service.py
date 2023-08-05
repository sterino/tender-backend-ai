import os

from dotenv import load_dotenv

from .adapters.requests_chain import ArnurService

load_dotenv()


class Service:
    def __init__(self, open_ai_api: str, pinecone_api_key: str, pinecone_api_env: str):
        self.arnur_service = ArnurService(
            open_ai_api, pinecone_api_key, pinecone_api_env
        )


def get_service():
    open_ai_key = os.getenv("OPENAI_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_api_env = os.getenv("PINECONE_API_ENV")
    svc = Service(open_ai_key, pinecone_api_key, pinecone_api_env)
    return svc
