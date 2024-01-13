# os library
import os
import uuid
# Audio file manipulations
import librosa
import soundfile as sf

# from pydub import AudioSegment
from tkinter.filedialog import askopenfilename

from openai import OpenAI

from dotenv import load_dotenv

DOTEBV_PATH = "../.env"  # Path to the .env file in the parent directory
load_dotenv(DOTEBV_PATH)


def _segment_audio(file: str, target_dir: str) -> None:
    """
    Segment an audio file into 10-second segments.

    Args:
        file (str): Path to the audio file.

    Returns:
        None
    """
    audio, sr = librosa.load(file, sr=None)
    duration = len(audio)
    ten_seconds = 10 * sr

    for i in range(0, duration, ten_seconds):
        segment = audio[i:i+ten_seconds]
        segment_path = f"segment_{i // ten_seconds}.wav"
        sf.write(os.path.join(target_dir, segment_path), segment, sr, 'PCM_24')


def _audio_to_text(file: str) -> str:
    """
    Convert segmented audio files to text using OpenAI's Whisper API.

    Args:
        file (str): Path to the directory containing segmented audio files.

    Returns:
        str: Full transcript of the audio.
    """
    client = OpenAI()

    transcripts = []
    for segment_file in sorted(os.listdir(file)):
        with open(os.path.join(file, segment_file), "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            transcripts.append(transcript.text)

    return " ".join(transcripts)


def audio_to_text(file: str) -> str:
    """
    Convert an audio file to text.

    Args:
        file (str): Path to the audio file.

    Returns:
        str: Full transcript of the audio.
    """
    # Create the target directory
    target_dir = os.path.join(os.path.dirname(file), str(uuid.uuid4()))
    os.makedirs(target_dir, exist_ok=True)

    try:
        # Segment the audio file
        _segment_audio(file, target_dir)

        # Convert segmented audio to text and get the full transcript
        full_transcript = _audio_to_text(target_dir)

        # Delete the segmented audio files
        for segment_file in os.listdir(target_dir):
            if segment_file.startswith("segment_"):
                os.remove(os.path.join(target_dir, segment_file))

        return full_transcript
    finally:
        # Remove the target directory after completion
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            os.remove(file_path)
        os.rmdir(target_dir)

if __name__ == "__main__":
    AUDIO_FILEPATH = askopenfilename()
    print(audio_to_text(AUDIO_FILEPATH))