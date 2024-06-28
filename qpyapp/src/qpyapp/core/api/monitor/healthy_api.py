from fastapi import APIRouter

from .models import HealthyStatusModel

router = APIRouter()


@router.get("/healthy", status_code=200, response_model=HealthyStatusModel)
def healthy():
    return HealthyStatusModel()
