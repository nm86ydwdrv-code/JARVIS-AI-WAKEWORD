import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3

from jarvis.config import VOICE_RATE

SAMPLE_RATE = 16000

_recognizer = sr.Recognizer()


def speak(text: str) -> None:
    print(f"JARVIS: {text}")
    # Re-create the engine each call: on Windows (SAPI5), reusing a single
    # pyttsx3 engine across multiple runAndWait() calls causes it to stop
    # producing audio after the first utterance.
    engine = pyttsx3.init()
    engine.setProperty("rate", VOICE_RATE)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def _record(duration: float) -> sr.AudioData:
    audio = sd.rec(
        int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16"
    )
    sd.wait()
    audio = audio.flatten()

    # Boost quiet microphone input so recognition has a better chance.
    peak = int(np.abs(audio).max())
    if 0 < peak < 32767:
        audio = (audio.astype(np.float32) * (32767.0 / peak * 0.9)).astype(np.int16)

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
