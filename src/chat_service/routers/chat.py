''' chat message endpoints '''

from fastapi import APIRouter, HTTPException, Depends

import functions.openai_request as foar

import dependencies.dependencies as dp

import database.database as dbd
import database.message as dbm

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(dp.validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/create_chat_message")
async def create_chat_message(
    thread_id: int,
    user_message: str,
    user_details: dict = Depends(dp.validate_token_header),
    cursor =  Depends(dbd.get_db_cursor)
):
    """
    Create thread message
    
    """
    # Get all the messages in the chat
    message_to_sent = dbm.get_recent_messages(
        user_details["azp"],
        thread_id,
        cursor=cursor,
    )
    
    if len(message_to_sent) > 21:
        return HTTPException(status_code=400, detail="Only 20 messages are allowed per thread")
    
    system_prompt = message_to_sent[0]
    message_to_sent = [{'role': message['role'], 'content': message['message']} for message in message_to_sent[1:]]
    message_to_sent = [system_prompt] + message_to_sent + [{"role":"user", "content":user_message}]

    # Get chat reponse
    try:
        response_message = foar.get_chat_reponse(message_to_sent)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error while getting the response") from e

    # Store the message
    dbm.store_messages(
        cursor=cursor, thread_id=thread_id,
        request_message=user_message,
        response_message=response_message
    )

    # Use StreamingResponse for streaming
    # return StreamingResponse(chat_response, media_type="plain/text")
    return response_message


@router.post("/get_chat_messages")
async def get_chat_messages(
    thread_id: int,
    user_details: dict = Depends(dp.validate_token_header),
    cursor =  Depends(dbd.get_db_cursor)
):
    """
    Get thread message
    
    """
    # Save file from frontend
    response = dbm.get_recent_messages(user_details["azp"], thread_id, cursor=cursor)
    return response[1::]