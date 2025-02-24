import os
import requests
from dotenv import load_dotenv

load_dotenv()
class Pair:
    def __init__(self, word, time_):
        self.word = word
        self.time_ = time_

def get():
    url = "https://transcribe.whisperapi.com"
    headers = {
        "Authorization": f"{os.getenv("WHISPER_API")}"
    }
    data = {
        "language": "english"
    }
    with open("temp/full.mp3", "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, headers=headers, files=files, data=data).json()

    pairs = []

    for segment in response['segments']:
        for timestamp in segment['whole_word_timestamps']:
            word = timestamp['word']
            time_ = timestamp['start']
            pairs.append(Pair(word, time_))
    return pairs
