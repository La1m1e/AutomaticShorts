import requests
from moviepy.config import change_settings
from moviepy.editor import *
from getcredentials import credentials
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


def gettimestamps():
    url = "https://transcribe.whisperapi.com"
    headers = {
        'Authorization': f'Bearer {credentials('whisperapi_key')}'
    }
    file = {'file': open('example.mp3', 'rb')}
    data = {
        "fileType": "mp3",
        "diarization": "false",
        "numSpeakers": "2",
        "initialPrompt": "",
        "language": "en",
        "task": "transcribe",
        "callbackURL": ""
    }
    response = requests.post(url, headers=headers, files=file, data=data)
    return response.json()


def extract_word_time_combinations():
    data = gettimestamps()
    combinations = []

    for segment in data['segments']:
        whole_word_timestamps = segment['whole_word_timestamps']

        for word_timestamp in whole_word_timestamps:
            word = word_timestamp['word']
            timestamp = word_timestamp['timestamp']
            combinations.append((word, timestamp))
    print(combinations)
    return combinations


def subtitles():
    word_list = extract_word_time_combinations()

    video_path = "sounded.mp4"
    video = VideoFileClip(video_path)

    text_clips = []

    for i in range(len(word_list) - 1):
        start_time = word_list[i][1]
        end_time = word_list[i + 1][1]
        word = word_list[i][0]

        txt_clip = TextClip(word, fontsize=140, color='white', font='MilkMango.ttf', method='label')
        duration = end_time - start_time
        txt_clip = txt_clip.set_duration(duration)
        text_clips.append(txt_clip)

    final_clip = concatenate_videoclips(text_clips, method="compose")
    result = CompositeVideoClip([video, final_clip.set_position('center')])
    result.write_videofile("result_video_with_text.mp4", codec='libx264', fps=video.fps)
