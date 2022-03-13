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
    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return False
    stream = AudioDataStream(result)
    stream.save_to_wav_file(filename)
    return True


count = 0
empty_count = 0
move_count = 0
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
                    move_count += 1
                else:
                    print(f"{backup_filename} is empty")
            else:
                # touch file
                if empty_count == 0:
                    print("gen audio", filename)
                    if gen_speak(word, str(filename)):
                        count += 1
                        print("success", count, filename)
                    else:
                        empty_count += 1
                        print("empty file", empty_count, filename)
    shutil.rmtree("res/audio_bak", ignore_errors=True)
    print(
        f"move {move_count} files, gen {count} files, empty {empty_count} files")
