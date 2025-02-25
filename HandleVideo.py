import os
import random
from moviepy import VideoFileClip, AudioFileClip, TextClip, concatenate_videoclips, CompositeVideoClip


def video_part(mp3_file, video_file, output_file):
    audio_clip = AudioFileClip(mp3_file)
    video_clip = VideoFileClip(video_file)
    max_start_time = video_clip.duration - audio_clip.duration - 2
    start_time = random.uniform(0, max_start_time)
    clip = video_clip.subclipped(start_time,start_time+audio_clip.duration)
    clip = clip.with_audio(audio_clip)
    return audio_clip.duration, clip


def add_subtitles(pairs, length, clip):
    text_clips = []
    txt_clip = TextClip(text='', font_size=140, color='white', font='MilkMango.ttf', duration=pairs[0].time_)
    text_clips.append(txt_clip)
    for idx, instance in enumerate(pairs):
        start = instance.time_
        if idx == len(pairs) - 1:
            end = length
        else:
            end = pairs[idx + 1].time_
        word = instance.word
        duration = end - start
        txt_clip = TextClip(text=word, font_size=140, color='white', font='MilkMango.ttf', duration=duration)
        text_clips.append(txt_clip)
    final_clip = concatenate_videoclips(text_clips, method="compose")
    result = CompositeVideoClip([clip, final_clip.with_position('center')])
    if result.duration > 180:
        result = result.subclipped(0,180)
    result.write_videofile("temp/result.mp4", codec='libx264', fps=clip.fps, threads = 10)
    result.close()
    os.remove("temp/full.mp3")


