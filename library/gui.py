from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt


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
