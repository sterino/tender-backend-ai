import os

from dotenv import load_dotenv

from .adapters.openai import ChatService
from .repository.repository import tenderRepository

load_dotenv()


class Service:
    def __init__(self, chat_service: str):
        self.chat_service = ChatService(chat_service)
        self.repository = tenderRepository()


def get_service():
    chat_service = os.getenv("OPENAI_API_KEY")
    svc = Service(chat_service)
    return svc
