''' llm endpoints '''

from pydub import AudioSegment

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse

from functions.openai_request import convert_audio_text, get_chat_reponse, text_to_speech
from functions.database import store_messages, reset_messages

from dependencies.dependencies import validate_token_header

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(validate_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/post_audio_get")
async def get_audio(file: UploadFile = File(...)):
    """
    Endpoint to summarize a PDF file.
    
    """
    # Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    
    # Decode the audio
    message_decoded = convert_audio_text(audio_input)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat reponse
    chat_response = get_chat_reponse(message_decoded)
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # Store the message
    store_messages(message_decoded, chat_response)

    # Audio outout
    audio_output = text_to_speech(chat_response)
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