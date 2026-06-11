import speech_recognition as sr
import pyttsx3

from jarvis.config import VOICE_RATE

_recognizer = sr.Recognizer()
_recognizer.energy_threshold = 300
_recognizer.dynamic_energy_threshold = True

_engine = pyttsx3.init()
_engine.setProperty("rate", VOICE_RATE)


def speak(text: str) -> None:
    print(f"JARVIS: {text}")
    _engine.say(text)
    _engine.runAndWait()


def listen(timeout=None, phrase_time_limit=None):
    """Listen on the default microphone and return recognized text (lowercase),
    or None if nothing could be understood."""
    with sr.Microphone() as source:
        _recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = _recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return None

    try:
        text = _recognizer.recognize_google(audio)
        return text.lower()
    except (sr.UnknownValueError, sr.RequestError):
        return None
