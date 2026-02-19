"""
MadVerse Word Input Screen
Collects user words one at a time with progress, skip (random), and back navigation.
"""

import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QProgressBar, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QKeyEvent, QCursor

from data.genres import Genre


RANDOM_WORD_BANKS = {
    "noun":      ["spatula", "fog", "democracy", "lighthouse", "regret", "cheese",
                   "bureaucracy", "suitcase", "ceiling fan", "obelisk", "algorithm",
                   "tambourine", "sundial", "escalator", "brochure", "mayonnaise"],
    "noun2":     ["prophecy", "noodle", "catastrophe", "silence", "invoice",
                   "monument", "cabbage", "footnote", "diploma", "cobblestone"],
    "verb":      ["exploded", "wept", "malfunctioned", "vanished", "surrendered",
                   "combusted", "apologized", "wobbled", "sighed", "evaporated"],
    "verb2":     ["screaming", "calculating", "yearning", "hovering", "wobbling",
                   "optimizing", "sighing", "deteriorating", "spiraling", "flickering"],
    "adjective": ["soggy", "ominous", "lukewarm", "catastrophic", "beige",
                   "unnecessarily tall", "vaguely damp", "statistically significant",
                   "mildly haunted", "chronically late", "aggressively beige"],
    "adjective2":["unsettling", "magnificent", "structurally questionable",
                   "emotionally unavailable", "suspiciously normal", "conspicuously absent"],
    "name":      ["Gerald", "Zorp-9", "Professor Mist", "Bartholomew",
                   "Dr. Elsewhere", "UNIT-7", "Marigold", "The Narrator"],
    "location":  ["the basement", "Neptune", "IKEA", "the void", "a parking garage",
                   "the second floor", "medieval times", "a conference room",
                   "the produce aisle", "somewhere unspecified"],
    "emotion":   ["mild dread", "existential joy", "performative concern",
                   "reluctant enthusiasm", "aggressive indifference", "suspicious hope"],
    "sound":     ["SPLONK", "wubbadubba", "krrshh", "BONK", "squelch",
                   "zorp", "FLOMPF", "vrrrm", "plink", "THWONK"],
    "object":    ["broken kazoo", "novelty socks", "non-functional umbrella",
                   "laminated ID card", "decorative gourd", "charging cable",
                   "half a stapler", "unsolicited pamphlet"],
    "number":    ["7", "400", "0.003", "17", "42", "9,000", "3.14", "1"],
}


class WordInputScreen(QWidget):
    """
    Presents word prompts one at a time.
    Emits words_collected({key: value}) when complete.
    Emits back_requested() when user goes back to genre select.
    """
    words_collected = pyqtSignal(dict)
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._genre: Genre = None
        self._prompts: list = []
        self._current_idx: int = 0
        self._words: dict = {}
        self._ai_subgenre: str = "chaotic absurdist"
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(80, 40, 80, 40)
        root.setSpacing(0)

        # ─── HEADER ───────────────────────────────────────
        hdr = QHBoxLayout()
        self._back_btn = QPushButton("← Back")
        self._back_btn.setObjectName("secondary_btn")
        self._back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._back_btn.setFixedWidth(100)
        self._back_btn.clicked.connect(self.back_requested.emit)

        self._genre_label = QLabel("")
        self._genre_label.setObjectName("section_title")
        self._genre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hdr.addWidget(self._back_btn)
        hdr.addStretch()
        hdr.addWidget(self._genre_label)
        hdr.addStretch()
        hdr.addSpacing(100)  # balance the back button

        root.addLayout(hdr)
        root.addSpacing(24)

        # ─── PROGRESS ─────────────────────────────────────
        prog_layout = QHBoxLayout()
        self._progress_label = QLabel("Word 1 of 12")
        self._progress_label.setObjectName("hint_label")
        self._progress_bar = QProgressBar()
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(8)

        prog_layout.addWidget(self._progress_label)
        prog_layout.addWidget(self._progress_bar)
        root.addLayout(prog_layout)
        root.addSpacing(40)

        # ─── MAIN INPUT CARD ──────────────────────────────
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(16)

        # Corruption label (fun status line)
        self._corruption_label = QLabel("Preparing story corruption…")
        self._corruption_label.setObjectName("hint_label")
        self._corruption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self._corruption_label)
        card_layout.addSpacing(8)

        # Prompt type badge
        self._type_badge = QLabel("NOUN")
        self._type_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._type_badge.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        self._type_badge.setFixedHeight(28)
        card_layout.addWidget(self._type_badge)

        # The actual prompt label
        self._prompt_label = QLabel("Give me a noun")
        self._prompt_label.setObjectName("prompt_label")
        self._prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._prompt_label.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
        self._prompt_label.setWordWrap(True)
        card_layout.addWidget(self._prompt_label)

        # Input field
        self._input = QLineEdit()
        self._input.setFixedHeight(52)
        self._input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._input.setFont(QFont("Georgia", 16))
        self._input.returnPressed.connect(self._on_next)
        card_layout.addWidget(self._input)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._skip_btn = QPushButton("🎲  Random")
        self._skip_btn.setObjectName("secondary_btn")
        self._skip_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._skip_btn.clicked.connect(self._on_skip)

        self._next_btn = QPushButton("Next →")
        self._next_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._next_btn.clicked.connect(self._on_next)
        self._next_btn.setFixedWidth(140)

        btn_row.addWidget(self._skip_btn)
        btn_row.addStretch()
        btn_row.addWidget(self._next_btn)
        card_layout.addLayout(btn_row)

        root.addWidget(card)
        root.addSpacing(20)

        # ─── AI SUBGENRE (only visible for AI genre) ──────
        self._ai_frame = QFrame()
        ai_layout = QVBoxLayout(self._ai_frame)
        ai_layout.setContentsMargins(0, 0, 0, 0)
        ai_layout.setSpacing(8)

        ai_lbl = QLabel("🤖  AI Sub-Genre / Mood")
        ai_lbl.setObjectName("prompt_label")
        ai_layout.addWidget(ai_lbl)

        self._ai_combo_label = QLabel("chaotic absurdist")
        self._ai_combo_label.setFont(QFont("Courier New", 12))
        self._ai_combo_label.setObjectName("hint_label")
        ai_layout.addWidget(self._ai_combo_label)

        # Cycle button
        self._ai_cycle_btn = QPushButton("Shuffle Sub-Genre 🔀")
        self._ai_cycle_btn.setObjectName("secondary_btn")
        self._ai_cycle_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._ai_cycle_btn.clicked.connect(self._cycle_ai_subgenre)
        ai_layout.addWidget(self._ai_cycle_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        root.addWidget(self._ai_frame)
        self._ai_frame.setVisible(False)

        root.addStretch()
        self.setLayout(root)

        # Corruption messages cycling
        self._corruption_messages = [
            "Preparing story corruption…",
            "Harvesting your words for maximum chaos…",
            "Loading narrative destabilizer…",
            "Calibrating absurdity engine…",
            "Warming up the randomizer…",
            "Consulting the chaos oracle…",
            f"Story quality: deteriorating (as intended)…",
        ]
        self._corruption_idx = 0
        self._corruption_timer = QTimer(self)
        self._corruption_timer.timeout.connect(self._cycle_corruption)
        self._corruption_timer.start(2500)

    def set_genre(self, genre: Genre):
        self._genre = genre
        self._prompts = genre.word_prompts
        self._current_idx = 0
        self._words = {}
        self._genre_label.setText(f"{genre.icon}  {genre.name}")
        self._progress_bar.setMaximum(len(self._prompts))
        self._progress_bar.setValue(0)
        self._ai_frame.setVisible(genre.id == "ai")
        self._update_prompt()

    def _update_prompt(self):
        if self._current_idx >= len(self._prompts):
            self._finish()
            return

        prompt = self._prompts[self._current_idx]
        total = len(self._prompts)
        idx = self._current_idx + 1

        self._progress_label.setText(f"Word {idx} of {total}")
        self._progress_bar.setValue(self._current_idx)
        self._prompt_label.setText(prompt["label"])
        self._input.setPlaceholderText(prompt["placeholder"])
        self._input.clear()
        self._input.setFocus()

        # Type badge
        type_labels = {
            "noun": "📦  NOUN",
            "verb": "⚡  VERB",
            "adj":  "🎨  ADJECTIVE",
            "name": "👤  NAME",
            "location": "📍  LOCATION",
            "emotion": "💭  EMOTION",
            "sound":  "🔊  SOUND",
            "object": "🔧  OBJECT",
            "number": "🔢  NUMBER",
        }
        badge = type_labels.get(prompt["type"], f"  {prompt['type'].upper()}")
        self._type_badge.setText(badge)

        # Update next button label on last item
        if self._current_idx == len(self._prompts) - 1:
            self._next_btn.setText("Generate! 🎭")
        else:
            self._next_btn.setText("Next →")

    def _on_next(self):
        text = self._input.text().strip()
        if not text:
            # Require input or use random
            self._on_skip()
            return

        key = self._prompts[self._current_idx]["key"]
        self._words[key] = text
        self._current_idx += 1
        self._update_prompt()

    def _on_skip(self):
        prompt = self._prompts[self._current_idx]
        key = prompt["key"]
        word_type = prompt["type"]
        bank = RANDOM_WORD_BANKS.get(word_type, RANDOM_WORD_BANKS["noun"])
        random_word = random.choice(bank)
        self._input.setText(random_word)

    def _cycle_ai_subgenre(self):
        from engine.ai_engine import AI_SUB_GENRES
        idx = AI_SUB_GENRES.index(self._ai_subgenre) if self._ai_subgenre in AI_SUB_GENRES else 0
        self._ai_subgenre = AI_SUB_GENRES[(idx + 1) % len(AI_SUB_GENRES)]
        self._ai_combo_label.setText(self._ai_subgenre)

    def _finish(self):
        self._progress_bar.setValue(len(self._prompts))
        self.words_collected.emit(self._words)

    def _cycle_corruption(self):
        self._corruption_idx = (self._corruption_idx + 1) % len(self._corruption_messages)
        self._corruption_label.setText(self._corruption_messages[self._corruption_idx])

    def get_ai_subgenre(self) -> str:
        return self._ai_subgenre
