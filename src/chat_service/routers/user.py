# User Info Endpoint

from fastapi import APIRouter, Depends

from dependencies.dependencies import get_user_and_update_info_wrapper, get_user_info

router = APIRouter(
    prefix="/thread",
    tags=["thread"],
    dependencies=[Depends(get_user_info)],
    responses={404: {"description": "Not found"}},
)

@router.post("/get_user_info")
async def get_user(
    user_and_cursor: dict = Depends(get_user_and_update_info_wrapper)
):
    """
    Get the current user details
    
    """
    return user_and_cursor[0]