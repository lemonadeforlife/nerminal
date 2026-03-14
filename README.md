<p align="center">
  <img src="assets/nerminal_transparent.png" width=50%>
  <h1 align="center">Nerminal</h1>
</p>
Nerminal is a lightweight offline voice assistant written in Python.
It listens for the wake phrase "hey nerminal", then executes simple system commands like opening a web browser.

The project uses the Vosk speech recognition engine to convert microphone audio into text and trigger commands locally. No internet connection is required.

> [!IMPORTANT]
> ⚠️ Nerminal is currently in early development. Features are experimental and the project is still evolving.

# Features
- Offline speech recognition (Vosk)
- Wake phrase activation ("hey nerminal")
- Local quantized LLM integration
- Text-to-speech responses
- Simple command execution system
- Open applications via voice commands
- Fuzzy wake-word detection (tolerates STT mistakes)
- Cross-platform support (Linux & Windows)
- Lightweight and efficient Python implementation
- Fully offline capable

# Example Usage
Speak the wake phrase:

> hey nerminal

Then give command:
> open firefox

Ask something conversational:
> what is a black hole

Nerminal will respond using the local LLM and speak the answer.

# Project Structure
```
├── library
│   ├── __init__.py
│   ├── llm.py
│   ├── stt.py
│   └── tts.py
├── main.py
├── model
│   ├── mosaicml-mpt-7b-instruct-Q4_K_M.gguf
│   ├── piper
│   │   └── hfc_female
│   │       ├── en_US-hfc_female-medium.onnx
│   │       └── en_US-hfc_female-medium.onnx.json
│   └── vosk-model-en-us-0.42-gigaspeech
├── nerminal.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```

# Download Required Models
Nerminal requires three offline models.
### espeak-ng
#### Windows 10/11
for Windows user download latest espeak-ng from [here](https://github.com/espeak-ng/espeak-ng/releases/latest)

#### Linux
To install precompiled package of eSpeak NG on Linux, use standard package manager of your
distribution. (Probably is very high, eSpeak NG will be included in package repository).

E.g. for Debian-like distribution (e.g. Ubuntu, Mint, etc.) execute command:

    sudo apt-get install espeak-ng

For RedHat-like distribution (e.g. CentOS, Fedora, etc.) execute command:

    sudo yum install espeak-ng
    
For ArchLinux-like distribution (e.g. SteamOS, EndeavourOS, etc.) execute command:

    sudo pacman -S espeak-ng

### Vosk Speech Recognition Model
Download from [here](https://alphacephei.com/vosk/models) & Extract it into:
```
model/vosk-model-en-us-0.42-gigaspeech
```

### Piper Text-to-Speech Voice
Download from [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices) huggingface repo

Example voice used in this project:
```
model/piper/hfc_female/
```

### LLM Model
Download the quantized GGUF model from [maddes8cht/mosaicml-mpt-7b-instruct-gguf](https://huggingface.co/maddes8cht/mosaicml-mpt-7b-instruct-gguf) huggingface repo
Place it inside:
```
model/
```

# Build Nerminal
## 1. Install uv
Nerminal uses **uv** to manage the Python environment and dependencies.
Install it with:
```
pip install uv
```
or on Linux/macOS:
```
curl -Ls https://astral.sh/uv/install.sh | sh
```

## 2. Clone the Repository
```
git clone https://github.com/lemonadeforlife/nerminal.git
cd nerminal
```
## 3. Install Project Dependencies
This will automatically create a virtual environment and install all dependencies defined in `pyproject.toml`.
```
uv sync
```

## 4. Run Nerminal
Start the assistant with:
```bash
uv run main.py
```

Once running, say the wake phrase:
> hey nerminal

# Future Plans
- [x] More voice commands
- [x] Application launcher
- [ ] Plugin system for custom commands
- [x] Improved wake-word detection
- [x] GUI interface
- [x] Implement small scaled qunatized LLM
- [ ] Better conversation memory
- [x] Smarter command routing (LLM + rules)
- [ ] More system integrations
- [x] Performance improvements for low-power machines

