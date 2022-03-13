import csv
import shutil
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import (AudioDataStream, SpeechConfig,
                                            SpeechSynthesisOutputFormat,
                                            SpeechSynthesizer)
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from config import ENV

speech_key = ENV.MS_TOKEN
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key, region=service_region)

speech_config.speech_synthesis_language = "en-US"
speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

audio_config = AudioOutputConfig(filename="/dev/null")
synthesizer = SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config)


def gen_speak(text, filename):
    result = synthesizer.speak_text_async(text).get()
    stream = AudioDataStream(result)
    stream.save_to_wav_file(filename)


count = 0
empty_count = 0
with open("res/picture.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    shutil.rmtree("res/audio_bak", ignore_errors=True)
    if Path("res/audio").exists():
        Path("res/audio").rename("res/audio_bak")

    for row in reader:
        chapter = row['Chapter']
        topic = row['Topic']
        words = row['words'].split('/')
        for word in words:
            backup_dir = Path("res/audio_bak").joinpath(chapter, topic)
            backup_filename = backup_dir.joinpath(f"{word}.wav")
            audio_dir = Path("res/audio").joinpath(chapter, topic)
            filename = audio_dir.joinpath(f"{word}.wav")
            audio_dir.mkdir(parents=True, exist_ok=True)
            if backup_filename.exists():
                # mv backup to new dir
                if backup_filename.stat().st_size > 0:
                    backup_filename.rename(filename)
                else:
                    print(f"{backup_filename} is empty")
            else:
                # touch file
                if empty_count == 0:
                    print("gen audio", filename)
                    gen_speak(word, str(filename))
                    if filename.stat().st_size == 0:
                        empty_count += 1
                        print("empty file", empty_count, filename)
                        filename.unlink()
                    else:
                        count += 1
                        print("success", count, filename)
    shutil.rmtree("res/audio_bak", ignore_errors=True)
    # gen_speak("runny nose", "file.wav")
