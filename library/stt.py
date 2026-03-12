import sounddevice as sd
import queue
import json
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

q = queue.Queue()

model = Model("model/vosk-model-en-us-0.42-gigaspeech")
rec = KaldiRecognizer(model, 16000)

WAKE_PHRASE = "hey nerminal"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def is_wake(text):
    """Check if text contains wake phrase"""
    words = text.split()
    if len(words) < 1:
        return False
    phrase = " ".join(words[:2])
    return similar(phrase, WAKE_PHRASE) > 0.65


def callback(indata, frames, time, status):
    """Audio callback - puts data in queue"""
    if status:
        print(status, flush=True)
    q.put(bytes(indata))


class STTEngine:
    def __init__(self, samplerate=16000, blocksize=4000):
        """Initialize STT engine"""
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.stream = None

    def start_stream(self):
        """Start audio input stream"""
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            dtype="int16",
            channels=1,
            callback=callback,
        )
        return self.stream

    def get_audio_data(self, timeout=0.1):
        """Get audio data from queue"""
        try:
            data = q.get(timeout=timeout)
            return data
        except queue.Empty:
            return None

    def process_audio(self, data):
        """Process audio data and return transcribed text if complete"""
        if data is None:
            return None

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            return result.get("text", "")

        return None

    def stop_stream(self):
        """Stop audio stream"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
