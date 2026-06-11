from anthropic import Anthropic

from jarvis.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, USER_NAME

_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

SYSTEM_PROMPT = (
    "You are JARVIS, a witty but efficient voice assistant inspired by the AI from "
    f"Iron Man. You are speaking with {USER_NAME}. Keep responses short (1-3 sentences) "
    "and conversational, since they will be read aloud by text-to-speech. "
    "Avoid markdown, code blocks, lists, or any formatting that doesn't make sense "
    "when spoken."
)

_history = []
MAX_HISTORY_TURNS = 10


def ask(prompt: str) -> str:
    if _client is None:
        return "My language model isn't configured. Please set ANTHROPIC_API_KEY in your .env file."

    _history.append({"role": "user", "content": prompt})

    try:
        response = _client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=300,
            system=SYSTEM_PROMPT,
            messages=_history[-MAX_HISTORY_TURNS * 2 :],
        )
    except Exception as exc:  # noqa: BLE001
        _history.pop()
        return f"I ran into a problem reaching my brain: {exc}"

    reply = "".join(block.text for block in response.content if block.type == "text").strip()
    _history.append({"role": "assistant", "content": reply})
    return reply
