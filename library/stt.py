import sounddevice as sd
import queue
import json
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

q = queue.Queue()
WAKE_PHRASE = "hey nerminal"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def is_wake(text):
    words = text.split()
    if len(words) < 1:
        return False
    phrase = " ".join(words[:2])
    return similar(phrase, WAKE_PHRASE) > 0.65


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    try:
        q.put_nowait(bytes(indata))
    except queue.Full:
        pass


def getMic():
    """Return system default input device or first real input mic"""
    try:
        default_input = sd.default.device[0]  # input device
        info = sd.query_devices(default_input)
        if info["max_input_channels"] > 0:
            return default_input
    except Exception:
        pass

    for i, dev in enumerate(sd.query_devices()):
        if dev["max_input_channels"] > 0 and not any(
            x in dev["name"].lower() for x in ["monitor", "default", "pipewire", "jack"]
        ):
            return i

    return None


class STTEngine:
    def __init__(self, model, blocksize=8000):
        self.rec = KaldiRecognizer(Model(model), 16000)
        self.blocksize = blocksize
        self.device = getMic()
        self.samplerate = 16000
        if self.device is None:
            raise RuntimeError("No suitable microphone found")
        self.stream = None
        print(f"Using microphone {self.device} with samplerate {self.samplerate}")

    def start_stream(self):
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            dtype="int16",
            channels=1,
            device=self.device,
            callback=callback,
        )
        self.stream.start()
        return self.stream

    def get_audio_data(self, timeout=0.1):
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            return None

    def process_audio(self, data):
        if data is None:
            return None
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            return result.get("text", "")
        return None

    def stop_stream(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
