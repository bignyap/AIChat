''' prompt endpoints '''

from fastapi import APIRouter, HTTPException, Depends, Form

import database.prompt as dbp

import dependencies.dependencies as dp

router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
    dependencies=[Depends(dp.get_user_info)],
    responses={404: {"description": "Not found"}},
)

@router.post("/create_user_prompt")
async def create_user_prompt(
    prompt_name: str = Form(...),
    prompt: str = Form(...),
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Create a message thread
    
    """
    user_details, cursor = user_and_cursor

    try:
        res = dbp.create_prompt(cursor, prompt_name, user_details['id'], prompt)
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while creating the prompt") from e
    

@router.get("/list_user_prompt")
async def list_user_prompt(
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    List prompt
    
    """
    user_details, cursor = user_and_cursor
    
    try:
        res = dbp.list_prompt(cursor, user_details['id'])
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while fetching the prompts") from e
    

@router.delete("/delete_user_prompt/{prompt_id}")
async def delete_user_prompt(
    prompt_id: int,
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Delete Prompt
    
    """
    user_details, cursor = user_and_cursor
    try:
        res = dbp.delete_prompt(cursor, prompt_id, user_details['id'])
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while deleting the prompt") from e
    

@router.put("/update_user_prompt/{thread_id}")
async def update_user_prompt(
    prompt_id: int,
    prompt: str = Form(...),
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Update Prompt
    
    """
    user_details, cursor = user_and_cursor
    
    try:
        res = dbp.update_prompt(cursor, prompt_id, user_details['id'], prompt)
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while updating the prompt") from e