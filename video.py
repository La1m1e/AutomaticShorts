from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import random
from pydub import AudioSegment


def get_duration(file_path):
    audio = AudioSegment.from_mp3(file_path)
    duration_in_seconds = len(audio) / 1000
    return duration_in_seconds


def video():
    duration = get_duration('example.mp3')
    input_video_path = 'Untitled.mp4'
    input_audio_path = 'example.mp3'
    output_path = 'sounded.mp4'

    clip_duration = duration

    video_clip = VideoFileClip(input_video_path)

    start_time = random.uniform(0, video_clip.duration - clip_duration)

    random_clip = video_clip.subclip(start_time, start_time + clip_duration)

    audio_clip = AudioFileClip(input_audio_path)

    random_clip = random_clip.set_audio(audio_clip)

    random_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close video and audio clips
    video_clip.close()
    audio_clip.close()
