import datetime
import os
import re
import subprocess
import webbrowser

import psutil

# Common apps -> launch command. Extend as needed.
APP_ALIASES = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "powershell": "powershell.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "spotify": "spotify.exe",
    "vs code": "code.exe",
    "visual studio code": "code.exe",
}

WEBSITE_ALIASES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "reddit": "https://reddit.com",
    "netflix": "https://netflix.com",
}


def _set_volume(level: float):
    """level: 0.0 - 1.0"""
    from ctypes import POINTER, cast

    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level)), None)


def _get_volume() -> float:
    from ctypes import POINTER, cast

    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def handle(text: str, user_name: str):
    """Try to handle `text` as a built-in command.

    Returns a tuple (handled, response, should_exit):
      handled      - True if this function dealt with the command
      response     - text to speak back (or None)
      should_exit  - True if the assistant should shut down
    """
    text = text.strip().lower()

    # Exit / shutdown
    if re.search(r"\b(exit|quit|shut down|shutdown|goodbye|go to sleep)\b", text):
        return True, f"Goodbye, {user_name}.", True

    # Time
    if "time" in text and "what" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return True, f"It's currently {now}.", False

    # Date
    if "date" in text and ("what" in text or "today" in text):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return True, f"Today is {today}.", False

    # Open website
    m = re.search(r"(?:open|go to|launch)\s+(?:the\s+)?website\s+(.+)", text)
    if not m:
        m = re.search(r"(?:open|go to)\s+([\w.\- ]+?)(?:\.com)?$", text)
        if m and m.group(1).strip() in WEBSITE_ALIASES:
            pass
        else:
            m = None
    if m:
        site = m.group(1).strip()
        url = WEBSITE_ALIASES.get(site)
        if url is None:
            if "." in site:
                url = "https://" + site
            else:
                url = f"https://{site}.com"
        webbrowser.open(url)
        return True, f"Opening {site}.", False

    # Open application
    m = re.search(r"(?:open|launch|start)\s+(.+)", text)
    if m:
        name = m.group(1).strip()
        if name in WEBSITE_ALIASES:
            webbrowser.open(WEBSITE_ALIASES[name])
            return True, f"Opening {name}.", False
        exe = APP_ALIASES.get(name)
        if exe:
            try:
                subprocess.Popen(exe)
                return True, f"Opening {name}.", False
            except OSError:
                return True, f"I couldn't find {name} on this system.", False
        return True, f"I don't know how to open {name} yet.", False

    # Volume control
    if "volume" in text or "mute" in text:
        if "mute" in text:
            _set_volume(0.0)
            return True, "Muted.", False
        if "max" in text or "full" in text:
            _set_volume(1.0)
            return True, "Volume set to maximum.", False
        m = re.search(r"(\d{1,3})\s*(?:percent|%)?", text)
        if m:
            level = int(m.group(1)) / 100
            _set_volume(level)
            return True, f"Volume set to {m.group(1)} percent.", False
        if "up" in text:
            _set_volume(min(1.0, _get_volume() + 0.1))
            return True, "Volume increased.", False
        if "down" in text:
            _set_volume(max(0.0, _get_volume() - 0.1))
            return True, "Volume decreased.", False

    # System stats
    if "cpu" in text or "system stat" in text or "performance" in text:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        return True, f"CPU usage is {cpu} percent, and memory usage is {mem} percent.", False

    if "battery" in text:
        battery = psutil.sensors_battery()
        if battery is None:
            return True, "I couldn't find a battery on this system.", False
        plugged = "charging" if battery.power_plugged else "not charging"
        return True, f"Battery is at {battery.percent} percent and {plugged}.", False

    # Not a built-in command
    return False, None, False
