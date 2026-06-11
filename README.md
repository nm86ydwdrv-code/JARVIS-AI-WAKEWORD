# JARVIS AI Wake Word Assistant

A Python voice assistant that listens for a wake word ("jarvis" by default),
then handles built-in commands (open apps/websites, time, date, volume,
system stats, battery) or falls back to Claude (Anthropic) for general
conversation.

## Setup

1. Install Python 3.10+.
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

   On Windows, if `PyAudio` fails to install via pip, install it via a
   prebuilt wheel: `pip install pipwin && pipwin install pyaudio`.

3. Copy `.env.example` to `.env` and fill in your Anthropic API key:

   ```
   copy .env.example .env
   ```

4. Run the assistant:

   ```
   python main.py
   ```

## Usage

Say "Jarvis" to wake the assistant, then speak your command. Examples:

- "Jarvis, what time is it?"
- "Jarvis, open notepad"
- "Jarvis, open youtube"
- "Jarvis, set volume to 50 percent"
- "Jarvis, what's the CPU usage?"
- "Jarvis, tell me a joke" (handled by Claude)
- "Jarvis, goodbye" (shuts down)

You can also say the wake word and command together in one breath, e.g.
"Jarvis what time is it".

## Configuration

Edit `.env` to customize:

- `ANTHROPIC_API_KEY` - your Claude API key
- `WAKE_WORD` - the word that activates the assistant
- `USER_NAME` - what JARVIS calls you
- `VOICE_RATE` - text-to-speech speed
- `CLAUDE_MODEL` - which Claude model to use

## Extending

- Add more apps to `APP_ALIASES` and websites to `WEBSITE_ALIASES` in
  `jarvis/commands.py`.
- Add new built-in commands inside `jarvis/commands.py`'s `handle()`
  function.
