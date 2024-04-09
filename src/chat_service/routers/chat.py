# Chat message endpoints

from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import StreamingResponse

import functions.openai_request as foar
import dependencies.dependencies as dp
import database.message as dbm

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(dp.get_user_info)],
    responses={404: {"description": "Not found"}},
)

@router.post("/create_chat_message/{thread_id}")
async def create_chat_message(
    thread_id: int,
    user_message: str = Form(...),
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    '''
    Create chat messages
    '''
    user_details, cursor = user_and_cursor
    user_id = user_details["id"]

    message_to_sent = dbm.get_recent_messages(user_id, thread_id, cursor=cursor)

    if len(message_to_sent) > 21:
        return HTTPException(status_code=400, detail="Only 20 messages are allowed per thread")

    system_prompt = message_to_sent[0]
    message_to_sent = [{'role': message['role'], 'content': message['message']} for message in message_to_sent[1:]]
    message_to_sent = [system_prompt] + message_to_sent + [{"role":"user", "content":user_message}]

    model_name = dbm.check_default_model(user_id, cursor=cursor)

    try:
        response_message = foar.get_chat_response(message_to_sent, model_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while getting the response") from e

    combined_message = ""

    async def generate():
        nonlocal combined_message
        for chunk in response_message:
            combined_message += "".join(chunk)
            yield chunk

        dbm.store_messages(
            thread_id=thread_id,
            request_message=user_message,
            response_message=combined_message
        )
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.get("/get_chat_messages/{thread_id}")
async def get_chat_messages(
    thread_id: int,
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Get thread message
    
    """
    user_details, cursor = user_and_cursor
    response = dbm.get_recent_messages(user_details["id"], thread_id, cursor=cursor)
    return response[1::]


@router.put("/update_default_chat_model")
async def update_default_chat_model(
    default_model_name: str = Form(...),
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Update the default chat model
    
    """
    user_details, cursor = user_and_cursor

    return dbm.update_default_model(user_details["id"], default_model_name, cursor=cursor)


@router.put("/get_default_chat_model")
async def get_default_chat_model(
    user_and_cursor: dict = Depends(dp.get_user_and_update_info)
):
    """
    Get the default chat model
    
    """
    user_details, cursor = user_and_cursor

    return dbm.check_default_model(user_details["id"], cursor=cursor)