import base64
import os
import json
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from pydub import AudioSegment


def get_access_token():
    """Retrieve an access token using google-auth instead of gcloud CLI."""
    credentials = service_account.Credentials.from_service_account_file(
        "utility/regal-state-451711-k7-362c00248d16.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(Request())
    return credentials.token


def synthesize_speech(text, name, model):
    print(f"Debug: {name} {model} {text}")
    output_path = f'temp/{name}.mp3'
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    access_token = get_access_token()

    if not access_token:
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",
            "name": model
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        audio_content = response.json().get("audioContent")
        if audio_content:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(audio_content))
            print(f"MP3 file saved to {output_path}")
        else:
            print("balls")
    else:
        print(f"{response.status_code}, {response.text}")


def mp3_files(file1, file2, output_file):
    combined = AudioSegment.from_raw(file1, sample_width=2, frame_rate=24000, channels=1).fade_in(50) +  AudioSegment.silent(duration=800) + AudioSegment.from_raw(file2, sample_width=2, frame_rate=24000, channels=1).fade_in(50)
    combined.export(output_file, format="mp3", bitrate="320k")
    os.remove(file1)
    os.remove(file2)
