"""
MadVerse Story Reveal Screen
Animated line-by-line text reveal with emphasis highlighting and action buttons.
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QSizePolicy,
    QFileDialog, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSignal as Signal
from PyQt6.QtGui import (QTextCharFormat, QColor, QFont, QTextCursor,
                          QTextDocument, QTextBlockFormat)

from data.genres import Genre
from ui.theme import get_story_type_format
from engine.story_engine import get_emphasis_ranges
from data.stats import get_tracker


class RevealTextWidget(QWidget):
    """
    Displays story parts one at a time with animation.
    """
    reveal_complete = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parts: list = []
        self._current_part_idx: int = 0
        self._theme = None
        self._reveal_timer = QTimer(self)
        self._reveal_timer.timeout.connect(self._reveal_next_part)
        self._all_revealed = False

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(32, 24, 32, 24)
        self._content_layout.setSpacing(0)
        self._content_layout.addStretch()

        self._scroll.setWidget(self._content)
        layout.addWidget(self._scroll)

    def start_reveal(self, parts: list, theme, speed_ms: int = 600):
        """Start revealing story parts."""
        # Clear previous content
        while self._content_layout.count() > 1:
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._parts = parts
        self._current_part_idx = 0
        self._theme = theme
        self._all_revealed = False

        if not parts:
            self.reveal_complete.emit()
            return

        self._reveal_timer.setInterval(speed_ms)
        self._reveal_timer.start()

    def reveal_all_instantly(self):
        """Show all parts immediately (for re-reads)."""
        self._reveal_timer.stop()
        while self._current_part_idx < len(self._parts):
            self._add_part_widget(self._parts[self._current_part_idx])
            self._current_part_idx += 1
        self._all_revealed = True
        self.reveal_complete.emit()

    def _reveal_next_part(self):
        if self._current_part_idx >= len(self._parts):
            self._reveal_timer.stop()
            self._all_revealed = True
            self.reveal_complete.emit()
            return

        part = self._parts[self._current_part_idx]
        self._add_part_widget(part)
        self._current_part_idx += 1

        # Scroll to bottom
        QTimer.singleShot(50, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        sb = self._scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _add_part_widget(self, part: dict):
        if not self._theme:
            return

        fmt = get_story_type_format(part["type"], self._theme)
        text = fmt["prefix"] + part["text"]
        emphasis_words = part.get("emphasis_words", [])

        # Create label container
        container = QFrame()
        container.setObjectName("story_part")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, fmt["margin_top"] * 2, 0, 2)
        container_layout.setSpacing(0)

        # Left accent line for special types
        if part["type"] in ("fourth_wall", "callback", "author_comment"):
            accent = QFrame()
            accent.setFixedWidth(3)
            accent.setFixedHeight(32)
            accent.setStyleSheet(f"background-color: {self._theme.accent_secondary}; border-radius: 2px;")
            container_layout.addWidget(accent)
            container_layout.addSpacing(8)

        label = RichTextLabel(text, emphasis_words, fmt, self._theme)
        label.setWordWrap(True)
        container_layout.addWidget(label)

        # Insert before the stretch
        stretch_idx = self._content_layout.count() - 1
        self._content_layout.insertWidget(stretch_idx, container)

    def is_complete(self) -> bool:
        return self._all_revealed

    def get_plain_text(self) -> str:
        return "\n\n".join(p["text"] for p in self._parts)


class RichTextLabel(QLabel):
    """Label with color-highlighted emphasis words."""

    def __init__(self, text: str, emphasis_words: list, fmt: dict, theme, parent=None):
        super().__init__(parent)
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Build rich text
        html = self._build_html(text, emphasis_words, fmt, theme)
        self.setText(html)
        self.setTextFormat(Qt.TextFormat.RichText)

        # Font
        f = QFont("Georgia", fmt["size"])
        f.setBold(fmt["bold"])
        f.setItalic(fmt["italic"])
        self.setFont(f)

    def _build_html(self, text: str, emphasis_words: list, fmt: dict, theme) -> str:
        import re
        if not emphasis_words:
            escaped = self._escape(text)
            return f'<span style="color:{fmt["color"]}; font-size:{fmt["size"]}pt; line-height:1.9;">{escaped}</span>'

        # Find emphasis ranges
        ranges = get_emphasis_ranges(text, emphasis_words)

        result = []
        last = 0
        for start, end in sorted(ranges):
            if start < last:
                continue
            # Normal text before
            normal = self._escape(text[last:start])
            result.append(f'<span style="color:{fmt["color"]};">{normal}</span>')
            # Emphasized word
            word = self._escape(text[start:end])
            result.append(
                f'<b><span style="color:{theme.highlight_color}; '
                f'background-color:{theme.card_color}; '
                f'border-radius:3px; padding:1px 3px;">{word}</span></b>'
            )
            last = end

        # Remaining text
        remaining = self._escape(text[last:])
        result.append(f'<span style="color:{fmt["color"]};">{remaining}</span>')

        body = "".join(result)
        return f'<span style="font-size:{fmt["size"]}pt; line-height:1.9;">{body}</span>'

    def _escape(self, text: str) -> str:
        return (text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))


class StoryRevealScreen(QWidget):
    """
    Full story reveal screen with controls.
    """
    play_again = pyqtSignal()          # same words, new story
    change_genre = pyqtSignal()        # back to genre select
    regenerate = pyqtSignal()          # same words + same genre, new random assembly
    achievement_unlocked = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._genre: Genre = None
        self._words: dict = {}
        self._parts: list = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ─── HEADER ───────────────────────────────────────
        header_frame = QFrame()
        header_frame.setObjectName("card")
        header_frame.setFixedHeight(64)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 8, 20, 8)

        self._genre_badge = QLabel("🎭  MadVerse Story")
        self._genre_badge.setFont(QFont("Georgia", 14, QFont.Weight.Bold))

        self._ai_indicator = QLabel("🤖 AI Generated")
        self._ai_indicator.setObjectName("hint_label")
        self._ai_indicator.setVisible(False)

        header_layout.addWidget(self._genre_badge)
        header_layout.addWidget(self._ai_indicator)
        header_layout.addStretch()

        # Speed control
        speed_lbl = QLabel("Speed:")
        speed_lbl.setObjectName("hint_label")

        self._speed_fast = QPushButton("Fast")
        self._speed_fast.setObjectName("secondary_btn")
        self._speed_fast.setFixedSize(60, 28)
        self._speed_fast.setCursor(Qt.CursorShape.PointingHandCursor)
        self._speed_fast.clicked.connect(lambda: self._set_speed("fast"))

        self._speed_slow = QPushButton("Slow")
        self._speed_slow.setObjectName("secondary_btn")
        self._speed_slow.setFixedSize(60, 28)
        self._speed_slow.setCursor(Qt.CursorShape.PointingHandCursor)
        self._speed_slow.clicked.connect(lambda: self._set_speed("slow"))

        self._skip_reveal_btn = QPushButton("⏭ Skip")
        self._skip_reveal_btn.setObjectName("secondary_btn")
        self._skip_reveal_btn.setFixedSize(70, 28)
        self._skip_reveal_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._skip_reveal_btn.clicked.connect(self._skip_reveal)

        header_layout.addWidget(speed_lbl)
        header_layout.addWidget(self._speed_fast)
        header_layout.addWidget(self._speed_slow)
        header_layout.addSpacing(8)
        header_layout.addWidget(self._skip_reveal_btn)

        root.addWidget(header_frame)

        # ─── STORY TEXT ───────────────────────────────────
        self._reveal_widget = RevealTextWidget()
        self._reveal_widget.reveal_complete.connect(self._on_reveal_complete)
        root.addWidget(self._reveal_widget, stretch=1)

        # ─── ACTION BUTTONS ───────────────────────────────
        self._action_frame = QFrame()
        self._action_frame.setObjectName("card")
        action_layout = QHBoxLayout(self._action_frame)
        action_layout.setContentsMargins(20, 12, 20, 12)
        action_layout.setSpacing(10)

        self._regen_btn = QPushButton("🔁  New Story (Same Words)")
        self._regen_btn.setObjectName("secondary_btn")
        self._regen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._regen_btn.clicked.connect(self._on_regenerate)

        self._again_btn = QPushButton("🎭  Change Words")
        self._again_btn.setObjectName("secondary_btn")
        self._again_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._again_btn.clicked.connect(self.play_again.emit)

        self._genre_btn = QPushButton("🎪  Change Genre")
        self._genre_btn.setObjectName("secondary_btn")
        self._genre_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._genre_btn.clicked.connect(self.change_genre.emit)

        self._save_btn = QPushButton("💾  Save Story")
        self._save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_btn.clicked.connect(self._on_save)

        self._copy_btn = QPushButton("📋  Copy")
        self._copy_btn.setObjectName("secondary_btn")
        self._copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._copy_btn.clicked.connect(self._on_copy)

        for btn in [self._regen_btn, self._again_btn, self._genre_btn]:
            action_layout.addWidget(btn)
        action_layout.addStretch()
        action_layout.addWidget(self._copy_btn)
        action_layout.addWidget(self._save_btn)

        self._action_frame.setVisible(False)
        root.addWidget(self._action_frame)

        self.setLayout(root)
        self._speed = 600  # ms between parts

    def show_story(self, genre: Genre, words: dict, parts: list, is_ai: bool = False):
        self._genre = genre
        self._words = words
        self._parts = parts

        self._genre_badge.setText(f"{genre.icon}  {genre.name}  —  MadVerse Story")
        self._ai_indicator.setVisible(is_ai)
        self._action_frame.setVisible(False)

        self._reveal_widget.start_reveal(parts, genre.theme, self._speed)

    def _on_reveal_complete(self):
        self._action_frame.setVisible(True)

    def _set_speed(self, speed: str):
        self._speed = 300 if speed == "fast" else 1000
        # Doesn't retroactively change current reveal, applies to next

    def _skip_reveal(self):
        self._reveal_widget.reveal_all_instantly()

    def _on_regenerate(self):
        new_ach = get_tracker().record_regeneration()
        if new_ach:
            self.achievement_unlocked.emit(new_ach)
        self.regenerate.emit()

    def _on_save(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Story", "madverse_story.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return

        text = self._build_save_text()
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            new_ach = get_tracker().record_save()
            if new_ach:
                self.achievement_unlocked.emit(new_ach)
            QMessageBox.information(self, "Saved!", f"Story saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    def _on_copy(self):
        text = self._build_save_text()
        QApplication.clipboard().setText(text)
        self._copy_btn.setText("✓ Copied!")
        QTimer.singleShot(2000, lambda: self._copy_btn.setText("📋  Copy"))

    def _build_save_text(self) -> str:
        lines = [
            "═" * 60,
            f"  MadVerse Story  ·  Genre: {self._genre.name}",
            "═" * 60,
            "",
        ]
        for part in self._parts:
            prefix = {
                "fourth_wall":  "  [aside] ",
                "author_comment": "  — ",
                "escalation":    "  *** ",
                "callback":      "  (note) ",
            }.get(part["type"], "  ")
            lines.append(prefix + part["text"])
            lines.append("")
        lines += [
            "═" * 60,
            "  Words used:",
        ]
        for k, v in self._words.items():
            lines.append(f"    {k}: {v}")
        lines.append("═" * 60)
        return "\n".join(lines)

    def get_words(self) -> dict:
        return self._words

    def get_genre(self) -> Genre:
        return self._genre
