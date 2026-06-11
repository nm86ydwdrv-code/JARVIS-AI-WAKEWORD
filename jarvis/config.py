import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()
USER_NAME = os.getenv("USER_NAME", "Sir")
VOICE_RATE = int(os.getenv("VOICE_RATE", "180"))
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
