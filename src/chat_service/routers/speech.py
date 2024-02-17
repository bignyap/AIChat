''' speech-to-text and text-to-speech endpoints '''

from pydub import AudioSegment

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse

import functions.openai_request as foar

import database.message as dbm

import dependencies.dependencies as dp

router = APIRouter(
    prefix="/speech",
    tags=["speech"],
    dependencies=[Depends(dp.validate_token_header)],
    responses={404: {"description": "Not found"}},
)

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
    dbm.store_messages(message_decoded, chat_response)

    # Audio outout
    audio_output = foar.text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get audio response")
    
    def generate_audio_chunks(audio_output: AudioSegment):
        yield audio_output.content

    # Use StreamingResponse for streaming
    return StreamingResponse(generate_audio_chunks(audio_output), media_type="application/octet-stream")