import os
import random
import shutil
import time
import GenerateAudio
import GenerateTags
import GetSubtitles
import HandleVideo
import YTUpload


def handle_text(text, comment, driver):
    try:
        models = ["Puck","Fenrir","Orus","Aoede","en-US-Chirp-HD-F"]
        pick = random.sample(models,2)
        GenerateAudio.synthesize_speech(text, 'text', pick[0])
        GenerateAudio.synthesize_speech(comment + ". Subscribe for more", 'comment', pick[1])
        GenerateAudio.mp3_files("temp/text.mp3","temp/comment.mp3","temp/full.mp3")
        length, clip = HandleVideo.video_part("temp/full.mp3", "VID/video.mp4", "temp/cut.mp4")
        subtitles = GetSubtitles.get()
        HandleVideo.add_subtitles(subtitles, length, clip)
        title,description,tags = GenerateTags.get(text + comment)
        print(title)
        print(description)
        print(tags)
        YTUpload.upload_video(driver, title, description, tags)


    except:
        time.sleep(5)
        Exception()
        print("Error who cares")
        temp_dir = 'temp/'
        if os.path.exists(temp_dir):
            # Remove all contents within the directory
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                                    # Check if it is a file or directory and delete accordingly
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Removes a directory and all its contents
                else:
                    os.remove(file_path)  # Removes a file