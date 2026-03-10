import sounddevice as sd
import queue
import json
import subprocess
import shutil
import time
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

q = queue.Queue()

model = Model("model/vosk-model-en-us-0.42-gigaspeech")
rec = KaldiRecognizer(model, 16000)

WAKE_PHRASE = "hey nerminal"
TIMEOUT_SECONDS = 5.0
STATE_IDLE = "IDLE"
STATE_LISTENING = "LISTENING"
current_state = STATE_IDLE
last_wake_time = 0

browsers = {
    "firefox": ["firefox"],
    "chrome": ["google-chrome", "chrome", "chrome.exe"],
    "brave": ["brave-browser", "brave", "brave.exe"],
    "edge": ["microsoft-edge", "msedge", "msedge.exe"],
}


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def is_wake(text):
    words = text.split()
    if len(words) < 1:
        return False
    phrase = " ".join(words[:2])
    return similar(phrase, WAKE_PHRASE) > 0.65


def find_browser(name):
    for cmd in browsers.get(name, []):
        if shutil.which(cmd):
            return cmd
    return None


def open_browser(name):
    cmd = find_browser(name)
    if cmd:
        subprocess.Popen([cmd])
        print(f"Opening {name}")
    else:
        print(f"{name} not found in PATH")


def extract_command(text):
    """
    Looks for 'open [browser]' anywhere in the text.
    Returns the browser name if found, else None.
    """
    words = text.split()
    for i, word in enumerate(words):
        if word == "open" and i + 1 < len(words):
            return words[i + 1]
    return None


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))


print("System Ready. Say 'Hey Nerminal' to start.")

with sd.RawInputStream(
    samplerate=16000,
    blocksize=4000,
    dtype="int16",
    channels=1,
    callback=callback,
):
    while True:
        try:
            data = q.get(timeout=0.1)
        except queue.Empty:
            if current_state == STATE_LISTENING:
                if time.time() - last_wake_time > TIMEOUT_SECONDS:
                    print("Timeout. Returning to Idle.")
                    current_state = STATE_IDLE
            continue

        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result())["text"]

            if not text:
                continue

            print("Heard:", text)
            current_time = time.time()
            if current_state == STATE_IDLE:
                if is_wake(text):
                    current_state = STATE_LISTENING
                    last_wake_time = current_time
                    print("Listening...")
                    browser = extract_command(text)
                    if browser:
                        open_browser(browser)
                        current_state = STATE_IDLE
                        print("Returning to Idle.")

            elif current_state == STATE_LISTENING:
                if current_time - last_wake_time > TIMEOUT_SECONDS:
                    current_state = STATE_IDLE
                    continue
                browser = extract_command(text)
                if browser:
                    open_browser(browser)
                else:
                    print("Command not recognized.")
                current_state = STATE_IDLE
                print("Returning to Idle.")
