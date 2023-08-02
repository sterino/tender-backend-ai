from fastapi import Depends

from app.utils import AppModel

from ..service import Service, get_service
from . import router

# router = APIRouter()


class TrdAppsResponse(AppModel):
    response: str


@router.get("/trd_apps")
def get_trade_app(
    bin: str,
    svc: Service = Depends(get_service),
):
    response = svc.repository.getTradesApp(bin)
    
    print(response)
    return response
