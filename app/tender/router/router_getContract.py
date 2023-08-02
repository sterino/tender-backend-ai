from fastapi import Depends

from app.utils import AppModel

from ..service import Service, get_service
from . import router

# router = APIRouter()


class ContractsResponse(AppModel):
    response: str


@router.get("/contracts")
def get_contracts(
    bin: str,
    svc: Service = Depends(get_service),
):
    response = svc.repository.getContracts(bin)
    print(response)
    return response
