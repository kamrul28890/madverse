"""
MadVerse Stats & Achievements Screen
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QGridLayout,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor

from data.stats import get_tracker, ACHIEVEMENTS


class StatBox(QFrame):
    """A single stat display box."""
    def __init__(self, number: str, label: str, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedHeight(100)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        num_lbl = QLabel(str(number))
        num_lbl.setObjectName("stat_number")
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label.upper())
        lbl.setObjectName("stat_label")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(num_lbl)
        layout.addWidget(lbl)


class AchievementCard(QFrame):
    """Single achievement display."""
    def __init__(self, ach: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumHeight(70)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)

        unlocked = ach.get("unlocked", False)

        # Icon
        icon_lbl = QLabel(ach["icon"] if unlocked else "🔒")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 22))
        icon_lbl.setFixedWidth(40)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_lbl)

        # Text
        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        name_lbl = QLabel(ach["name"])
        name_lbl.setObjectName("achievement_name")
        if not unlocked:
            name_lbl.setStyleSheet("color: #666666;")

        desc_lbl = QLabel(ach["desc"])
        desc_lbl.setObjectName("achievement_desc")
        if not unlocked:
            desc_lbl.setStyleSheet("color: #444444;")

        text_col.addWidget(name_lbl)
        text_col.addWidget(desc_lbl)
        layout.addLayout(text_col)
        layout.addStretch()

        # Status badge
        if unlocked:
            badge = QLabel("✓ UNLOCKED")
            badge.setStyleSheet("color: #00cc66; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        else:
            badge = QLabel("LOCKED")
            badge.setStyleSheet("color: #555555; font-size: 10px; letter-spacing: 1px;")
        badge.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(badge)

        # Dim locked cards
        if not unlocked:
            self.setStyleSheet(self.styleSheet() + "QFrame { opacity: 0.5; }")


class StatsScreen(QWidget):
    """Full stats and achievements screen."""
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 28, 40, 28)
        root.setSpacing(0)

        # ─── HEADER ───────────────────────────────────────
        hdr = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("secondary_btn")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.back_requested.emit)

        title = QLabel("📊  Stats & Achievements")
        title.setObjectName("section_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hdr.addWidget(back_btn)
        hdr.addStretch()
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addSpacing(100)
        root.addLayout(hdr)
        root.addSpacing(24)

        # ─── STATS GRID ───────────────────────────────────
        tracker = get_tracker()
        summary = tracker.get_stats_summary()

        stats_grid = QGridLayout()
        stats_grid.setSpacing(12)

        stat_data = [
            (str(summary["total_stories"]),         "Stories Generated"),
            (str(summary["stories_saved"]),          "Stories Saved"),
            (str(summary["regenerations"]),          "Regenerations"),
            (summary["favorite_genre"].title() if summary["favorite_genre"] != "none" else "—",
                                                     "Favorite Genre"),
            (summary["most_used_word"].title() if summary["most_used_word"] != "none yet" else "—",
                                                     "Most Used Word"),
            (f"{summary['achievements_unlocked']}/{summary['total_achievements']}",
                                                     "Achievements"),
        ]

        for i, (num, lbl) in enumerate(stat_data):
            box = StatBox(num, lbl)
            stats_grid.addWidget(box, i // 3, i % 3)

        root.addLayout(stats_grid)
        root.addSpacing(28)

        # ─── ACHIEVEMENTS ─────────────────────────────────
        ach_title = QLabel("🏆  Achievements")
        ach_title.setObjectName("section_title")
        root.addWidget(ach_title)
        root.addSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 8, 0)
        scroll_layout.setSpacing(8)

        achievements = tracker.get_all_achievements()
        # Sort: unlocked first
        achievements.sort(key=lambda a: (0 if a["unlocked"] else 1, a["name"]))

        for ach in achievements:
            card = AchievementCard(ach)
            scroll_layout.addWidget(card)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        root.addWidget(scroll, stretch=1)
        self.setLayout(root)

    def refresh(self):
        """Rebuild the screen with fresh data."""
        # Clear and rebuild
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._build_ui()


class AchievementPopup(QFrame):
    """Floating achievement notification."""
    def __init__(self, ach: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedSize(320, 80)
        self.setStyleSheet("""
            QFrame {
                background-color: #1a2a1a;
                border: 2px solid #00cc66;
                border-radius: 12px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        icon_lbl = QLabel(ach["icon"])
        icon_lbl.setFont(QFont("Segoe UI Emoji", 24))
        layout.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        unlocked_lbl = QLabel("🏆 ACHIEVEMENT UNLOCKED!")
        unlocked_lbl.setStyleSheet("color: #00cc66; font-size: 10px; font-weight: bold; letter-spacing: 1px;")

        name_lbl = QLabel(ach["name"])
        name_lbl.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: bold;")

        text_col.addWidget(unlocked_lbl)
        text_col.addWidget(name_lbl)
        layout.addLayout(text_col)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Auto-hide
        self._hide_timer = None
        from PyQt6.QtCore import QTimer
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._fade_out)

    def show_for(self, ms: int = 3500):
        self.show()
        self._hide_timer.start(ms)

    def _fade_out(self):
        self.hide()
        self.deleteLater()
