# Datetime library
import datetime
import os

from typing import List, Dict

# Library to Search, Download YouTube video and audio stream
from pytube import Search, YouTube, Stream

# Whisper to detect the language
import whisper

def search_video(query: str, howmany: int = 5) -> Dict[str, List[str]]:
    """
    This is a docstring for search_video.

    Args:
        query (str): Query to find the YouTube Video
        howmany (int): How many videos to search for

    Returns:
        str: List of video links
    """
    video_objects = Search(query).results
    youtube_links = [f"https://www.youtube.com/watch?v={video.video_id}" for video in video_objects]
    return youtube_links[:howmany]


def audio_to_transcript(file: str) -> str:
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


def download_audio_from_stream(stream: Stream) -> str:
    """
    This is a docstring for download_audio_from_stream.

    Args:
        stream (Stream): Audio Stream

    Returns:
        str: Path to the audio file
    """

    filename = str(datetime.datetime.now().timestamp())
    filename = ".".join([filename, "mp3"])
    stream.download(output_path="YouTubeVideos", filename=filename)
    return os.path.join("YouTubeVideos", filename)


def download_audio_from_url(url: str) -> str:
    """
    This is a docstring for download_audio_from_url.

    Args:
        url (str): YouTube URL

    Returns:
        str: Path to the audio file
    """
    yt_object = YouTube(url)
    return download_audio_from_stream(
        yt_object.streams.filter(
            only_audio=True, file_extension='mp4'
        ).first()
    )


def download_audios_from_url(urls: List[str]) -> List[Dict[str, str]]:
    """
    This is a docstring for download_audios_from_url.

    Args:
        url (str): YouTube URL

    Returns:
        str: Path to the audio file
    """
    return [{"Link": link, "Audio": download_audio_from_url(link)} for link in urls]


def download_audios(query: str, howmany: str = 5) -> List[Dict[str, str]]:
    """
    This is a docstring for download_audios.

    Args:
        url (str): YouTube Query
        howmany (int): How many search results

    Returns:
        str: Path to the audio files
    """
    res = search_video(query, howmany)
    if len(res) != 0:
        return download_audios_from_url(res)
    else:
        return []


def get_transcript_from_url(url: str) -> str:
    """
    This is a docstring for get_transcript_from_url.

    Args:
        url (str): YouTube Query

    Returns:
        str: Path to the transcript files
    """
    return audio_to_transcript(download_audio_from_url(url))


def get_transcripts_from_url(urls: List[str]) -> List[Dict[str, str]]:
    """
    This is a docstring for get_transcripts_from_url.

    Args:
        url (List[str]): YouTube URLs

    Returns:
        str: Path to the transcript files
    """
    return [{"Link": link, "Transcript": get_transcript_from_url(link)} for link in urls]


def get_transcripts(query: str, howmany: int = 5) -> List[Dict[str, str]]:
    """
    This is a docstring for download_audios.

    Args:
        url (str): YouTube Query
        howmany (int): How many search results

    Returns:
        str: Path to the transcript files
    """
    res = search_video(query, howmany)
    if len(res) != 0:
        return get_transcripts_from_url(res)


if __name__ == "__main__":
    QUERY = str(input("What do you want to search: "))
    HOW_MANY = int(input("How many video do you want: "))
    print(get_transcripts(QUERY, HOW_MANY))
