import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3

from jarvis.config import VOICE_RATE

SAMPLE_RATE = 16000

_recognizer = sr.Recognizer()

_engine = pyttsx3.init()
_engine.setProperty("rate", VOICE_RATE)


def speak(text: str) -> None:
    print(f"JARVIS: {text}")
    _engine.say(text)
    _engine.runAndWait()


def _record(duration: float) -> sr.AudioData:
    audio = sd.rec(
        int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16"
    )
    sd.wait()
    return sr.AudioData(audio.tobytes(), SAMPLE_RATE, 2)


def listen(timeout=None, phrase_time_limit=None):
    """Record from the default microphone and return recognized text (lowercase),
    or None if nothing could be understood."""
    duration = phrase_time_limit or timeout or 4
    audio = _record(duration)

    try:
        text = _recognizer.recognize_google(audio)
        return text.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return None
