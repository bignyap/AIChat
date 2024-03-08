# User Info Endpoint

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_user_and_update_info

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_user_info")
async def get_user(
    user_and_cursor: dict = Depends(get_user_and_update_info)
):
    """
    Get the current user details
    
    """
    return user_and_cursor[0]