from fastapi import Depends

from app.utils import AppModel

from ..service import Service, get_service
from . import router

# router = APIRouter()


class ChatRequest(AppModel):
    prompt: str


class ChatResponse(AppModel):
    response: str


@router.post("/")
def post_chat(
    request: ChatRequest,
    svc: Service = Depends(get_service),
):
    prompt = request.prompt
    response = svc.arnur_service.get_response_chat(prompt)
    print(response)
    return response["content"]
