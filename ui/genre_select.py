"""
MadVerse Genre Selection Screen
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGridLayout, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QFont, QCursor

from data.genres import ALL_GENRES, Genre, GenreTheme
from ui.theme import build_main_stylesheet


class GenreCard(QPushButton):
    """A clickable genre selection card."""

    def __init__(self, genre: Genre, parent=None):
        super().__init__(parent)
        self.genre = genre
        self.setObjectName("genre_btn")
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(110)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        # Icon + name row
        top_row = QHBoxLayout()
        icon_lbl = QLabel(genre.icon)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 26))
        icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        name_lbl = QLabel(f"  {genre.name}")
        name_lbl.setFont(QFont("Georgia", 15, QFont.Weight.Bold))
        name_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        top_row.addWidget(icon_lbl)
        top_row.addWidget(name_lbl)
        top_row.addStretch()

        # Tagline
        tag_lbl = QLabel(genre.tagline)
        tag_lbl.setWordWrap(True)
        tag_lbl.setFont(QFont("Georgia", 10))
        tag_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        tag_lbl.setObjectName("hint_label")

        layout.addLayout(top_row)
        layout.addWidget(tag_lbl)

        self.setLayout(layout)


class GenreSelectScreen(QWidget):
    """
    Full genre selection screen.
    Emits genre_selected(Genre) when the user picks a genre and clicks Start.
    """
    genre_selected = pyqtSignal(object)  # Genre
    stats_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_genre: Genre = None
        self._cards: list[GenreCard] = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(48, 32, 48, 32)
        root.setSpacing(0)

        # ─── HEADER ───────────────────────────────────────
        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("MadVerse")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tagline = QLabel("Genre-Based Randomized Mad Libs  ·  Where words go to misbehave.")
        tagline.setObjectName("tagline_label")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(title)
        header.addWidget(tagline)
        header.addSpacing(24)

        choose_lbl = QLabel("Choose Your Genre")
        choose_lbl.setObjectName("section_title")
        choose_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(choose_lbl)

        root.addLayout(header)
        root.addSpacing(16)

        # ─── GENRE GRID ───────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(14)
        grid.setContentsMargins(0, 0, 0, 0)

        for i, genre in enumerate(ALL_GENRES):
            card = GenreCard(genre)
            card.clicked.connect(lambda checked, g=genre, c=card: self._on_genre_clicked(g, c))
            self._cards.append(card)
            row, col = divmod(i, 3)
            grid.addWidget(card, row, col)

        root.addLayout(grid)
        root.addSpacing(24)

        # ─── BOTTOM ROW ───────────────────────────────────
        bottom = QHBoxLayout()
        bottom.setSpacing(12)

        self._stats_btn = QPushButton("📊  Stats & Achievements")
        self._stats_btn.setObjectName("secondary_btn")
        self._stats_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._stats_btn.clicked.connect(self.stats_requested.emit)

        self._start_btn = QPushButton("🎭  START MADNESS")
        self._start_btn.setObjectName("large_btn")
        self._start_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._start_btn.clicked.connect(self._on_start)
        self._start_btn.setEnabled(False)

        bottom.addWidget(self._stats_btn)
        bottom.addStretch()
        bottom.addWidget(self._start_btn)

        root.addLayout(bottom)
        self.setLayout(root)

    def _on_genre_clicked(self, genre: Genre, card: GenreCard):
        for c in self._cards:
            c.setChecked(False)
            c.setProperty("selected", "false")
            c.style().unpolish(c)
            c.style().polish(c)

        card.setChecked(True)
        card.setProperty("selected", "true")
        card.style().unpolish(card)
        card.style().polish(card)

        self._selected_genre = genre
        self._start_btn.setEnabled(True)

    def _on_start(self):
        if self._selected_genre:
            self.genre_selected.emit(self._selected_genre)

    def reset_selection(self):
        for c in self._cards:
            c.setChecked(False)
            c.setProperty("selected", "false")
            c.style().unpolish(c)
            c.style().polish(c)
        self._selected_genre = None
        self._start_btn.setEnabled(False)
