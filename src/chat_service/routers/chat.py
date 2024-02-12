''' llm endpoints '''

import uuid

from pydub import AudioSegment

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse

import functions.openai_request as foar
import database.database as db
import database.crud as dc
import dependencies.dependencies as dp

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(dp.validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/create_chat_thread")
async def create_chat_thread(
    name: str = uuid.uuid4(),
    user_details: dict = Depends(dp.validate_token_header),
    cursor =  Depends(db.get_db_cursor)
):
    """
    Create a message thread
    
    """
    try:
        res = dc.create_thread(cursor, name, user_details['azp'])
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error while creating the thread") from e
    

@router.post("/list_chat_thread")
async def list_chat_thread(
    user_details: dict = Depends(dp.validate_token_header),
    cursor =  Depends(db.get_db_cursor)
):
    """
    Create a message thread
    
    """
    try:
        res = dc.list_thread(cursor, user_details['azp'])
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error while fetching the threads") from e
    

@router.post("/delete_chat_thread")
async def delete_chat_thread(
    thread_id: int,
    user_details: dict = Depends(dp.validate_token_header),
    cursor =  Depends(db.get_db_cursor)
):
    """
    Create a message thread
    
    """
    try:
        res = dc.delete_thread(cursor, thread_id, user_details['azp'])
        return res
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token") from e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error while deleting the threads") from e
    


@router.post("/post_audio_get")
async def get_audio(file: UploadFile = File(...)):
    """
    Audio response generator
    
    """
    # Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    
    # Decode the audio
    message_decoded = foar.convert_audio_text(audio_input)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat reponse
    chat_response = foar.get_chat_reponse(message_decoded)
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Store the message
    dc.store_messages(message_decoded, chat_response)

    # Audio outout
    audio_output = foar.text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get audio response")
    
    def generate_audio_chunks(audio_output: AudioSegment):
        yield audio_output.content

    # Use StreamingResponse for streaming
    return StreamingResponse(generate_audio_chunks(audio_output), media_type="application/octet-stream")


@router.post("/reset_messages")
async def reset_conversation():
    """
    Delete chat history
    """
    reset_messages()
    return {"message":"conversation reset"}