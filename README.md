<h1 align="center">Nerminal</h1>
Nerminal is a lightweight offline voice assistant written in Python.
It listens for the wake phrase "hey nerminal", then executes simple system commands like opening a web browser.

The project uses the Vosk speech recognition engine to convert microphone audio into text and trigger commands locally. No internet connection is required.

> [!IMPORTANT]
> ⚠️ Nerminal is currently in early development. Features are experimental and the project is still evolving.

# Features
- Offline speech recognition
- Wake phrase activation (hey nerminal)
- Cross-platform (Linux and Windows)
- Opens applications (for now browsers)
- Fuzzy wake-word detection to tolerate speech recognition errors
- Simple, lightweight & efficient Python implementation

# Example Usage
Speak the wake phrase:
```
hey nerminal
```
Then give command:
```
open firefox
```

# Project Structure
```
nerminal/
|
├── main.py
├── model/
|   └── add your vosk model here
└── ReadMe.md
```

# Future Plans
- [ ] More voice commands
- [ ] Application launcher
- [ ] Plugin system for custom commands
- [ ] Improved wake-word detection
- [ ] GUI interface
- [ ] Implement small scaled qunatized LLM
