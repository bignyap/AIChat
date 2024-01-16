"""
OpenAI Services

"""

import openai

from .database import get_recent_messages

# OpenAI - Whisper
# Convert Audio to text
def convert_audio_text(audio_file):
    """
    Audio to text
    """
    try:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        message_text = transcript.text
        return message_text
    except Exception as e:
        print(e)
        return e

# OpenAI - ChatGPT
# Get Response to our Message
def get_chat_reponse(message_input):
    """
    Chat reponse
    """

    messages = get_recent_messages()
    user_message = {"role":"user", "content":message_input}
    messages.append(user_message)

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message_text = response.choices[0].message.content
        return message_text
    except Exception as e:
        print(e)
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
            input=input_text
        )
        return response
        # .stream_to_file(speech_file_path)
    except Exception as e:
        print(e)
        return e

