import re

from jarvis import brain, commands
from jarvis.config import USER_NAME, WAKE_WORD
from jarvis.speech import listen, speak


def strip_wake_word(text: str) -> str:
    pattern = rf"^\s*{re.escape(WAKE_WORD)}\b[,]?\s*"
    return re.sub(pattern, "", text, flags=re.IGNORECASE).strip()


def handle_command(command: str) -> bool:
    """Process a command. Returns False if the assistant should shut down."""
    if not command:
        speak("I didn't catch that.")
        return True

    handled, response, should_exit = commands.handle(command, USER_NAME)
    if not handled:
        response = brain.ask(command)

    if response:
        speak(response)

    return not should_exit


def main():
    speak(f"JARVIS online. Say '{WAKE_WORD}' to wake me up, {USER_NAME}.")

    running = True
    while running:
        heard = listen(timeout=None, phrase_time_limit=4)
        if not heard:
            continue

        if WAKE_WORD not in heard:
            continue

        remainder = strip_wake_word(heard)
        if remainder:
            running = handle_command(remainder)
            continue

        speak("Yes?")
        command = listen(timeout=5, phrase_time_limit=8)
        running = handle_command(command or "")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
