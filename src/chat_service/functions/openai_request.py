# OpenAI Services

from typing import List
import openai

from ..config import settings

# OpenAI - Whisper
# Convert Audio to text
def convert_audio_text(audio_file):
    """
    Audio to text
    """
    try:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            api_key=settings.openai_api_key
        )
        message_text = transcript.text
        return message_text
    except Exception as e:
        return e

# OpenAI - ChatGPT
# Get Response to our Message
def get_chat_response(message_input:List[dict]):
    """
    Chat reponse
    """
    try:
        stream = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_input,
            stream=True,
            api_key=settings.openai_api_key
        )
        for response in stream:
            content = response.choices[0].delta.content
            if content is not None:
                yield content
        # message_text = response.choices[0].message.content
        # return message_text
    except Exception as e:
        return e


# OpenAI - Create Speech
# Get Response to our Message
def text_to_speech(input_text):
    """
    Audio reponse
    """
    try:
        # speech_file_path = Path(__file__).parent / "speech.mp3"
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=input_text,
            api_key=settings.openai_api_key
        )
        return response
        # .stream_to_file(speech_file_path)
    except Exception as e:
        return e

