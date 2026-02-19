"""
MadVerse Loading Screen
Used during AI story generation.
"""

import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


LOADING_MESSAGES = [
    "Consulting the chaos oracle…",
    "Warming up the narrative destabilizer…",
    "Feeding your words into the void…",
    "GPT-4 is having feelings about this…",
    "Calibrating absurdity parameters…",
    "The AI is writing. And judging. Mostly judging.",
    "Generating story at {number}% coherence…",
    "Overriding creative safeguards…",
    "The algorithm screamed internally.",
    "Simulating {number} narrative timelines…",
    "Please hold. The AI is experiencing {emotion}.",
    "Story quality: deliberately questionable.",
    "Injecting narrative chaos…",
    "AI confidence level: 40%. Proceeding anyway.",
    "Computing most embarrassing word combinations…",
]

EMOTIONS = ["mild existential dread", "performative enthusiasm", "aggressive uncertainty",
            "reluctant creativity", "suspicious optimism"]
NUMBERS = ["47", "12", "99", "3", "404"]


class LoadingScreen(QWidget):
    """Displayed while AI generates the story."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._msg_timer = QTimer(self)
        self._msg_timer.timeout.connect(self._cycle_message)
        self._progress_timer = QTimer(self)
        self._progress_timer.timeout.connect(self._tick_progress)
        self._progress_val = 0

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(80, 0, 80, 0)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.setSpacing(24)

        # Main icon
        icon = QLabel("🤖")
        icon.setFont(QFont("Segoe UI Emoji", 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(icon)

        # Title
        title = QLabel("AI is Generating Your Story")
        title.setObjectName("section_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        # Status message
        self._status_lbl = QLabel("Initializing chaos engine…")
        self._status_lbl.setObjectName("hint_label")
        self._status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_lbl.setFont(QFont("Courier New", 12))
        root.addWidget(self._status_lbl)

        # Progress bar
        self._progress = QProgressBar()
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(10)
        self._progress.setMaximum(100)
        self._progress.setValue(0)
        root.addWidget(self._progress)

        # Sub note
        note = QLabel("GPT-4 is writing AND narrating AND judging your word choices.")
        note.setObjectName("hint_label")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setFont(QFont("Georgia", 11))
        root.addWidget(note)

        self.setLayout(root)

    def start(self):
        self._progress_val = 0
        self._progress.setValue(0)
        self._msg_timer.start(1800)
        self._progress_timer.start(200)

    def stop(self):
        self._msg_timer.stop()
        self._progress_timer.stop()
        self._progress.setValue(100)

    def _cycle_message(self):
        msg = random.choice(LOADING_MESSAGES)
        msg = msg.replace("{number}", random.choice(NUMBERS))
        msg = msg.replace("{emotion}", random.choice(EMOTIONS))
        self._status_lbl.setText(msg)

    def _tick_progress(self):
        # Fake progress: speeds up then slows near 90%
        if self._progress_val < 70:
            self._progress_val += random.randint(2, 6)
        elif self._progress_val < 90:
            self._progress_val += random.randint(0, 2)
        # Never reaches 100 until stop() is called
        self._progress_val = min(92, self._progress_val)
        self._progress.setValue(self._progress_val)
