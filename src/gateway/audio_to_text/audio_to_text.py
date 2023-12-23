# os library
import os

# Whisper to detect the language
import whisper


def audio_to_text(file: str) -> str:
    """
    This is a docstring for audio_to_transcript.

    Args:
        file (str): Audio file

    Returns:
        str: Path to the transcript filr
    """

    # filename = os.path.basename(file)
    filename = os.path.splitext(file)[0]
    filename = ".".join([filename, "txt"])

    # Load the base model and transcribe the audio
    model = whisper.load_model("base")
    result = model.transcribe(file)
    transcribed_text = result["text"]

    with open(filename, "w", encoding='utf-8') as file1:
        file1.write(transcribed_text)

    return transcribed_text


if __name__ == "__main__":
    AUDIO_FILEPATH = str(input("Audio filepath: "))
    print(audio_to_text(AUDIO_FILEPATH))
