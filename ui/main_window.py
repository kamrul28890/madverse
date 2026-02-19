"""
MadVerse Main Window
Orchestrates navigation between screens using QStackedWidget.
Applies per-genre themes dynamically.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout, QFrame, QApplication,
    QCheckBox, QSlider
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont, QCloseEvent, QIcon

from data.genres import Genre, ALL_GENRES, GENRE_MAP
from data.stats import get_tracker
from ui.theme import build_main_stylesheet
from ui.background import AnimatedBackground
from ui.genre_select import GenreSelectScreen
from ui.word_input import WordInputScreen
from ui.story_reveal import StoryRevealScreen
from ui.stats_screen import StatsScreen, AchievementPopup
from ui.loading_screen import LoadingScreen
from engine.story_engine import StoryEngine
from audio.sounds import get_sound_manager

# Screen indices
SCREEN_GENRE   = 0
SCREEN_WORDS   = 1
SCREEN_LOADING = 2
SCREEN_STORY   = 3
SCREEN_STATS   = 4


class SettingsBar(QFrame):
    """Persistent top-right settings bar (sound toggle + volume)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_bar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        sound_mgr = get_sound_manager()

        self._sound_cb = QCheckBox("🔊 Sound")
        self._sound_cb.setChecked(sound_mgr.is_enabled())
        self._sound_cb.stateChanged.connect(
            lambda s: sound_mgr.set_enabled(s == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self._sound_cb)

        vol_lbl = QLabel("Vol:")
        vol_lbl.setObjectName("hint_label")
        layout.addWidget(vol_lbl)

        self._vol_slider = QSlider(Qt.Orientation.Horizontal)
        self._vol_slider.setFixedWidth(80)
        self._vol_slider.setRange(0, 100)
        self._vol_slider.setValue(70)
        self._vol_slider.valueChanged.connect(
            lambda v: sound_mgr.set_volume(v / 100)
        )
        layout.addWidget(self._vol_slider)

        self.setFixedHeight(36)


class MainWindow(QMainWindow):
    """Root window — 960×680, dark themed, genre-aware."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MadVerse")
        self.setMinimumSize(960, 680)
        self.resize(1100, 740)

        self._current_genre: Genre = None
        self._current_words: dict = {}
        self._current_parts: list = []
        self._ai_worker = None

        self._build_ui()
        self._apply_theme(ALL_GENRES[0])  # default theme

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ─── ANIMATED BACKGROUND ──────────────────────────
        self._bg = AnimatedBackground(central)
        self._bg.setGeometry(0, 0, self.width(), self.height())
        self._bg.lower()

        # ─── SETTINGS BAR ─────────────────────────────────
        self._settings_bar = SettingsBar()
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self._settings_bar)
        root.addLayout(top_bar)

        # ─── STACKED SCREENS ──────────────────────────────
        self._stack = QStackedWidget()

        self._genre_screen  = GenreSelectScreen()
        self._words_screen  = WordInputScreen()
        self._loading_screen = LoadingScreen()
        self._story_screen  = StoryRevealScreen()
        self._stats_screen  = StatsScreen()

        self._stack.addWidget(self._genre_screen)   # 0
        self._stack.addWidget(self._words_screen)   # 1
        self._stack.addWidget(self._loading_screen) # 2
        self._stack.addWidget(self._story_screen)   # 3
        self._stack.addWidget(self._stats_screen)   # 4

        root.addWidget(self._stack, stretch=1)

        # ─── WIRE SIGNALS ─────────────────────────────────
        self._genre_screen.genre_selected.connect(self._on_genre_selected)
        self._genre_screen.stats_requested.connect(self._show_stats)

        self._words_screen.words_collected.connect(self._on_words_collected)
        self._words_screen.back_requested.connect(lambda: self._go_to(SCREEN_GENRE))

        self._story_screen.play_again.connect(self._on_play_again)
        self._story_screen.change_genre.connect(self._on_change_genre)
        self._story_screen.regenerate.connect(self._on_regenerate)
        self._story_screen.achievement_unlocked.connect(self._show_achievements)

        self._stats_screen.back_requested.connect(lambda: self._go_to(SCREEN_GENRE))

        # ─── ACHIEVEMENT QUEUE ────────────────────────────
        self._achievement_queue: list = []
        self._achievement_showing = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._bg.setGeometry(0, 0, self.width(), self.height())

    # ─────────────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────────────

    def _go_to(self, screen_idx: int):
        self._stack.setCurrentIndex(screen_idx)
        get_sound_manager().play("click")

    def _apply_theme(self, genre: Genre):
        stylesheet = build_main_stylesheet(genre.theme, genre.id)
        self.setStyleSheet(stylesheet)
        self._bg.set_effect(genre.theme.effect, genre.theme)

    # ─────────────────────────────────────────────────────
    # FLOW: Genre → Words → Generate → Story
    # ─────────────────────────────────────────────────────

    def _on_genre_selected(self, genre: Genre):
        self._current_genre = genre
        self._apply_theme(genre)
        get_sound_manager().play("select")
        get_sound_manager().play_genre_theme(genre.id)
        self._words_screen.set_genre(genre)
        self._go_to(SCREEN_WORDS)

    def _on_words_collected(self, words: dict):
        self._current_words = words
        get_sound_manager().play("reveal")

        if self._current_genre.id == "ai":
            self._generate_ai_story()
        else:
            self._generate_local_story()

    def _generate_local_story(self):
        engine = StoryEngine(self._current_genre, self._current_words)
        self._current_parts = engine.generate()
        self._show_story(is_ai=False)

    def _generate_ai_story(self):
        self._go_to(SCREEN_LOADING)
        self._loading_screen.start()

        sub_genre = self._words_screen.get_ai_subgenre()

        from engine.ai_worker import AIWorker
        self._ai_worker = AIWorker(self._current_words, sub_genre)
        self._ai_worker.finished.connect(self._on_ai_finished)
        self._ai_worker.error.connect(self._on_ai_error)
        self._ai_worker.start()

    def _on_ai_finished(self, parts: list):
        self._loading_screen.stop()
        self._current_parts = parts
        self._show_story(is_ai=True)

    def _on_ai_error(self, error: str):
        self._loading_screen.stop()
        # Still show story (will show error message)
        from engine.ai_engine import AIStoryEngine
        engine = AIStoryEngine(self._current_words)
        self._current_parts = engine._error_story(error)
        self._show_story(is_ai=True)

    def _show_story(self, is_ai: bool = False):
        # Record stats
        new_ach = get_tracker().record_story(
            self._current_genre.id, self._current_words
        )

        self._story_screen.show_story(
            self._current_genre,
            self._current_words,
            self._current_parts,
            is_ai=is_ai,
        )
        self._go_to(SCREEN_STORY)
        get_sound_manager().play("complete")

        if new_ach:
            self._show_achievements(new_ach)

    def _on_regenerate(self):
        """Same words, same genre, new random story assembly."""
        if self._current_genre.id == "ai":
            self._generate_ai_story()
        else:
            self._generate_local_story()

    def _on_play_again(self):
        """Keep genre, get new words."""
        self._words_screen.set_genre(self._current_genre)
        self._go_to(SCREEN_WORDS)

    def _on_change_genre(self):
        """Go back to genre selection."""
        self._genre_screen.reset_selection()
        self._go_to(SCREEN_GENRE)

    # ─────────────────────────────────────────────────────
    # STATS
    # ─────────────────────────────────────────────────────

    def _show_stats(self):
        self._stats_screen.refresh()
        self._go_to(SCREEN_STATS)

    # ─────────────────────────────────────────────────────
    # ACHIEVEMENTS
    # ─────────────────────────────────────────────────────

    def _show_achievements(self, achievements: list):
        self._achievement_queue.extend(achievements)
        if not self._achievement_showing:
            self._pop_next_achievement()

    def _pop_next_achievement(self):
        if not self._achievement_queue:
            self._achievement_showing = False
            return

        self._achievement_showing = True
        ach = self._achievement_queue.pop(0)
        get_sound_manager().play("achievement")

        popup = AchievementPopup(ach, self)
        # Position bottom-right
        x = self.width() - popup.width() - 20
        y = self.height() - popup.height() - 20
        popup.move(x, y)
        popup.show_for(3500)

        # Chain next after delay
        QTimer.singleShot(4000, self._pop_next_achievement)

    def closeEvent(self, event: QCloseEvent):
        if self._ai_worker and self._ai_worker.isRunning():
            self._ai_worker.quit()
            self._ai_worker.wait(2000)
        super().closeEvent(event)
