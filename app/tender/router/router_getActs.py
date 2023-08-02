from fastapi import Depends

from app.utils import AppModel

from ..service import Service, get_service
from . import router

# router = APIRouter()


class ActsResponse(AppModel):
    response: str


@router.get("/acts")
def get_acts(
    id: str,
    svc: Service = Depends(get_service),
):
    response = svc.repository.getActs(id)
    print(response)
    return response
