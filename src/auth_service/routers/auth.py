''' authentication endpoints '''

from fastapi import Depends, APIRouter

from auth.auth import get_user_info
from auth.models import User

router = APIRouter(
    prefix="/auth",
)

@router.post("/get_user_info")
async def root(user: User = Depends(get_user_info)):
    return user