from elevenlabs import generate, Voice, VoiceSettings
from getcredentials import credentials


def ttsaudio(title, text, comment):
    print(title)
    print(text)
    print(comment)
    text = text.replace("\n", " ")
    comment = comment.replace("\n", " ")
    audio = generate(
        text=title + " " + text,
        voice=Voice(
            voice_id='ErXwobaYiN019PkySvjV',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2",
        api_key=credentials('elevenlabs_api_key')

    )
    audio1 = generate(
        text=comment,
        voice=Voice(
            voice_id='9F4C8ztpNUmXkdDDbz3J',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2",
        api_key=credentials('elevenlabs_api_key')
    )
    with open("example.mp3", "wb") as f:
        f.write(audio + audio1)
