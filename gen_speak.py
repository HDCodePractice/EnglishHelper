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

audio_config = AudioOutputConfig(filename="file.wav")
synthesizer = SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config)

text = "runny nose"
result = synthesizer.speak_text_async(text).get()
stream = AudioDataStream(result)
stream.save_to_wav_file("file.wav")
