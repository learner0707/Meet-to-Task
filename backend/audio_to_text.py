import speech_recognition as sr
from pydub import AudioSegment
import os


def convert_audio_to_text(file_path):

    recognizer = sr.Recognizer()

    try:

        # Convert uploaded audio to WAV
        audio = AudioSegment.from_file(file_path)

        wav_path = file_path + ".wav"

        audio.export(wav_path, format="wav")

        with sr.AudioFile(wav_path) as source:

            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        print("Transcript:", text)

        return text

    except Exception as e:

        print("Audio processing error:", e)

        return ""