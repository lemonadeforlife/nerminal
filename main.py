import subprocess
import sys
import threading
import shutil
import time
import webbrowser
from datetime import datetime
from library.stt import STTEngine, is_wake
from library.llm import LLMEngine
from library.tts import PiperTTS
from PySide6.QtWidgets import QApplication
from library.gui import NerminalGUI

TIMEOUT_SECONDS = 5.0
STATE_IDLE = "IDLE"
STATE_LISTENING = "LISTENING"

BROWSERS = {
    "firefox": ["firefox"],
    "chrome": ["google-chrome", "chrome", "chrome.exe"],
    "brave": ["brave-browser", "brave", "brave.exe"],
    "edge": ["microsoft-edge", "msedge", "msedge.exe"],
}


class VoiceAssistant:
    def __init__(self):
        self.stt = STTEngine()
        self.llm = LLMEngine()
        self.tts = PiperTTS()
        self.current_state = STATE_IDLE
        self.last_wake_time = 0
        self.is_speaking = False

    def find_browser(self, name):
        for cmd in BROWSERS.get(name, []):
            if shutil.which(cmd):
                return cmd
        return None

    def open_browser(self, name):
        cmd = self.find_browser(name)
        if cmd:
            subprocess.Popen([cmd])
            return True, f"Opening {name}"
        return False, f"{name} not found"

    def search_web(self, query, browser_name="firefox"):
        cmd = self.find_browser(browser_name)
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        if cmd:
            subprocess.Popen([cmd, url])
        else:
            webbrowser.open(url)
        return True, f"Searching for: {query}"

    def tell_time(self):
        now = datetime.now()
        return True, f"The current time is {now.strftime('%I:%M %p')}"

    def execute_action(self, action_data, user_text):
        if isinstance(action_data, str):
            action_data = {"action": action_data}

        action = action_data.get("action", "unknown")

        if action == "open_browser":
            browser = action_data.get("browser", user_text.split()[-1].lower())
            return self.open_browser(browser)

        elif action == "search_web":
            query = action_data.get("query", user_text)
            browser = action_data.get("browser", "firefox")
            return self.search_web(query, browser)

        elif action == "tell_time":
            return self.tell_time()

        else:
            response = self.llm.chat(user_text)
            return True, response

    def process_command(self, text):
        print(f"[CMD] Input: '{text}'")
        action_data = self.llm.route_command(text)
        print(f"[CMD] Action: {action_data}")
        success, response = self.execute_action(action_data, text)
        return response

    def run(self):
        print("System Ready. Say 'Hey Nerminal' to start.")
        self.tts.speak("System Ready")

        with self.stt.start_stream():
            while True:
                if self.tts.is_speaking:
                    time.sleep(0.02)
                    continue

                data = self.stt.get_audio_data(timeout=0.05)
                if data is None:
                    if self.current_state == STATE_LISTENING:
                        if time.time() - self.last_wake_time > TIMEOUT_SECONDS:
                            print("Timeout. Idle.")
                            self.current_state = STATE_IDLE
                            self.llm.clear_history()
                    continue

                text = self.stt.process_audio(data)
                if not text:
                    continue

                print("Heard:", text)
                current_time = time.time()

                if self.current_state == STATE_IDLE:
                    if is_wake(text):
                        print("[WAKE] Detected!")
                        self.tts.speak("Yes!")
                        self.current_state = STATE_LISTENING
                        self.last_wake_time = current_time
                        print("Listening...")

                elif self.current_state == STATE_LISTENING:
                    self.last_wake_time = current_time
                    response = self.process_command(text)
                    print("Assistant:", response)
                    self.tts.speak(response)
                    self.current_state = STATE_IDLE
                    print("Idle.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = NerminalGUI()
    gui.show()

    assistant = VoiceAssistant()
    t = threading.Thread(target=assistant.run, daemon=True)
    t.start()

    sys.exit(app.exec())
