# library/tts.py
import io
import wave
import sounddevice as sd
import soundfile as sf
import time
from piper import PiperVoice


class PiperTTS:
    def __init__(
        self,
        model_path="model/piper/hfc_female/en_US-hfc_female-medium.onnx",
        config_path=None,
    ):
        """
        Load a Piper voice model using the official Python API.
        """
        self.is_speaking = False
        print("Loading Piper TTS voice model…")
        self.voice = PiperVoice.load(
            model_path=model_path,
            config_path=config_path,
        )
        self.sample_rate = self.voice.config.sample_rate
        print(f"Piper loaded (sample rate: {self.sample_rate} Hz).")

    def speak(self, text: str):
        """
        Generate speech for `text` and play it
        """
        if not text:
            return

        self.is_speaking = True

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)

            self.voice.synthesize_wav(text, wav_file)

        buffer.seek(0)
        data, fs = sf.read(buffer, dtype="float32")

        sd.play(data, fs)
        sd.wait()
        time.sleep(0.3)
        self.is_speaking = False
