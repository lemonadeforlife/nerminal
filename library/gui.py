import os
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
)
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt


MODELS_JSON = "models.json"

REQUIRED_FILES = {
    "piper_model": "model/piper/en_US-hfc_female-medium.onnx",
    "piper_config": "model/piper/hfc_female/en_US-hfc_female-medium.onnx.json",
    "vosk_model": "model/vosk-model-en-us-0.42-gigaspeech",
    "llm_model": "model/mosaicml-mpt-7b-instruct-Q4_K_M.gguf",
}


def load_models():
    if os.path.exists(MODELS_JSON):
        with open(MODELS_JSON, "r") as f:
            paths = json.load(f)
        return paths
    return REQUIRED_FILES.copy()


def check_models(paths):
    missing = []
    for name, path in paths.items():
        if not os.path.exists(path):
            missing.append(name)
    return missing


def ensure_models():
    paths = load_models()
    missing = check_models(paths)

    if missing:
        print("Some models are missing:", missing)

        app = QApplication.instance() or QApplication([])
        selector = ModelSelector()
        selector.show()
        app.exec()

        # If user closed the GUI without clicking Start, exit
        if not selector.success:
            print("Model selection cancelled by user. Exiting.")
            sys.exit(0)

        # Reload updated paths from REQUIRED_FILES
        paths = REQUIRED_FILES.copy()

    return paths


class ModelSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Model Paths")
        self.setMinimumSize(500, 200)

        self.inputs = {}
        self.success = False  # Track if user clicked Start

        layout = QVBoxLayout()

        for name, default_path in REQUIRED_FILES.items():
            row = QVBoxLayout()

            label = QLabel(name)
            field = QLineEdit(default_path)
            browse = QPushButton("Browse")

            if name == "vosk_model":
                browse.clicked.connect(lambda _, f=field: self.select_folder(f))
            else:
                browse.clicked.connect(lambda _, f=field: self.select_file(f))

            row.addWidget(label)
            row.addWidget(field)
            row.addWidget(browse)
            layout.addLayout(row)

            self.inputs[name] = field

        start_btn = QPushButton("Start Nerminal")
        start_btn.clicked.connect(self.on_start)
        layout.addWidget(start_btn)

        self.setLayout(layout)

    def select_file(self, field):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            field.setText(path)

    def select_folder(self, field):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            field.setText(path)

    def on_start(self):
        for name, field in self.inputs.items():
            REQUIRED_FILES[name] = field.text()
        self.success = True
        self.close()


class NerminalGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nerminal")
        self.setFixedSize(720, 540)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.bg_label = QLabel(self)
        self.bg_label.setAlignment(Qt.AlignCenter)
        movie = QMovie("assets/background.gif")
        self.bg_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.bg_label)
