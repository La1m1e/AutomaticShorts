import os
import ffmpeg
import random
from moviepy import VideoFileClip, AudioFileClip, TextClip, concatenate_videoclips, CompositeVideoClip


def video_part(mp3_file, video_file, output_file):
    audio_length = float(ffmpeg.probe(mp3_file, v='error', select_streams='a', show_entries='format=duration')['format']['duration'])
    video_length = float(ffmpeg.probe(video_file, v='error', show_entries='format=duration')['format']['duration'])
    max_start_time = video_length - audio_length - 2
    start_time = random.uniform(0, max_start_time)
    ffmpeg.input(video_file, ss=start_time, t=audio_length+1).output(output_file, c='copy').run()
    return audio_length


def combine_all(pairs, length, video_path ="temp/cut.mp4", audio_path ="temp/full.mp3"):
    clip = VideoFileClip(video_path).with_audio(AudioFileClip(audio_path))
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
    result.write_videofile("temp/result.mp4", codec='libx264', fps=clip.fps, threads = 10)
    result.close()
    os.remove("temp/cut.mp4")
    os.remove("temp/full.mp3")


