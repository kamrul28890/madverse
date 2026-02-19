"""
MadVerse Theme System
Per-genre QSS stylesheets and shared UI constants.
"""

from data.genres import GenreTheme


GOOGLE_FONTS_CSS = """
/* Fonts loaded via system or bundled */
"""

BASE_FONT_FAMILIES = {
    "horror":      ("'Segoe UI', serif", "'Georgia', serif"),
    "scifi":       ("'Courier New', monospace", "'Consolas', monospace"),
    "fantasy":     ("'Georgia', serif", "'Palatino Linotype', serif"),
    "romance":     ("'Georgia', serif", "'Book Antiqua', serif"),
    "academic":    ("'Times New Roman', serif", "'Palatino', serif"),
    "existential": ("'Georgia', serif", "'Garamond', serif"),
    "ai":          ("'Courier New', monospace", "'Lucida Console', monospace"),
}


def build_main_stylesheet(theme: GenreTheme, genre_id: str) -> str:
    """Build the full QSS stylesheet for a given genre theme."""
    title_font, body_font = BASE_FONT_FAMILIES.get(genre_id, ("'Segoe UI'", "'Segoe UI'"))

    return f"""
/* ─── BASE ─────────────────────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {theme.bg_color};
    color: {theme.text_color};
    font-family: {body_font};
    font-size: 13px;
}}

/* ─── TITLE LABEL ───────────────────────────────────────── */
QLabel#title_label {{
    font-family: {title_font};
    font-size: 42px;
    font-weight: bold;
    color: {theme.accent_color};
    letter-spacing: 4px;
}}

QLabel#tagline_label {{
    font-family: {body_font};
    font-size: 13px;
    color: {theme.text_color};
    opacity: 0.7;
    letter-spacing: 1px;
}}

QLabel#section_title {{
    font-family: {title_font};
    font-size: 18px;
    color: {theme.accent_color};
    font-weight: bold;
}}

QLabel#prompt_label {{
    font-family: {body_font};
    font-size: 14px;
    color: {theme.text_color};
    font-weight: bold;
}}

QLabel#hint_label {{
    font-family: {body_font};
    font-size: 11px;
    color: {theme.accent_secondary};
}}

/* ─── CARDS / FRAMES ────────────────────────────────────── */
QFrame#card {{
    background-color: {theme.card_color};
    border: 1px solid {theme.card_border};
    border-radius: 12px;
    padding: 16px;
}}

QFrame#genre_card {{
    background-color: {theme.card_color};
    border: 2px solid {theme.card_border};
    border-radius: 16px;
}}

QFrame#genre_card:hover {{
    border-color: {theme.accent_color};
    background-color: {theme.bg_gradient_end};
}}

/* ─── BUTTONS ───────────────────────────────────────────── */
QPushButton {{
    background-color: {theme.accent_color};
    color: {theme.bg_color};
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-family: {body_font};
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 1px;
}}

QPushButton:hover {{
    background-color: {theme.highlight_color};
}}

QPushButton:pressed {{
    background-color: {theme.accent_secondary};
}}

QPushButton#secondary_btn {{
    background-color: transparent;
    color: {theme.accent_color};
    border: 1px solid {theme.accent_color};
}}

QPushButton#secondary_btn:hover {{
    background-color: {theme.card_color};
}}

QPushButton#danger_btn {{
    background-color: transparent;
    color: #ff4444;
    border: 1px solid #ff4444;
}}

QPushButton#large_btn {{
    font-size: 16px;
    padding: 14px 32px;
    letter-spacing: 2px;
}}

QPushButton#genre_btn {{
    background-color: {theme.card_color};
    color: {theme.text_color};
    border: 2px solid {theme.card_border};
    border-radius: 16px;
    padding: 20px 16px;
    font-size: 15px;
    font-weight: bold;
    text-align: left;
}}

QPushButton#genre_btn:hover {{
    border-color: {theme.accent_color};
    color: {theme.accent_color};
    background-color: {theme.bg_gradient_end};
}}

QPushButton#genre_btn[selected="true"] {{
    border-color: {theme.accent_color};
    background-color: {theme.bg_gradient_end};
    color: {theme.accent_color};
}}

/* ─── INPUT FIELDS ──────────────────────────────────────── */
QLineEdit {{
    background-color: {theme.card_color};
    color: {theme.text_color};
    border: 2px solid {theme.card_border};
    border-radius: 8px;
    padding: 10px 14px;
    font-family: {body_font};
    font-size: 14px;
    selection-background-color: {theme.accent_color};
}}

QLineEdit:focus {{
    border-color: {theme.accent_color};
}}

QLineEdit::placeholder {{
    color: {theme.accent_secondary};
    font-style: italic;
}}

/* ─── PROGRESS BAR ───────────────────────────────────────── */
QProgressBar {{
    background-color: {theme.card_color};
    border: 1px solid {theme.card_border};
    border-radius: 6px;
    height: 10px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {theme.accent_color};
    border-radius: 5px;
}}

/* ─── SCROLL AREA ───────────────────────────────────────── */
QScrollArea {{
    background-color: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background-color: {theme.bg_color};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {theme.accent_secondary};
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* ─── STORY TEXT ─────────────────────────────────────────── */
QTextEdit#story_text {{
    background-color: transparent;
    color: {theme.text_color};
    border: none;
    font-family: {body_font};
    font-size: 15px;
    line-height: 1.8;
    padding: 8px;
    selection-background-color: {theme.accent_color};
}}

/* ─── COMBOBOX ───────────────────────────────────────────── */
QComboBox {{
    background-color: {theme.card_color};
    color: {theme.text_color};
    border: 1px solid {theme.card_border};
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
}}

QComboBox:focus {{
    border-color: {theme.accent_color};
}}

QComboBox QAbstractItemView {{
    background-color: {theme.card_color};
    color: {theme.text_color};
    border: 1px solid {theme.card_border};
    selection-background-color: {theme.accent_color};
}}

/* ─── TOOLTIP ───────────────────────────────────────────── */
QToolTip {{
    background-color: {theme.card_color};
    color: {theme.text_color};
    border: 1px solid {theme.accent_color};
    padding: 4px 8px;
    border-radius: 4px;
}}

/* ─── SPLITTER ──────────────────────────────────────────── */
QSplitter::handle {{
    background-color: {theme.card_border};
}}

/* ─── STATS LABELS ──────────────────────────────────────── */
QLabel#stat_number {{
    font-size: 32px;
    font-weight: bold;
    color: {theme.accent_color};
    font-family: {title_font};
}}

QLabel#stat_label {{
    font-size: 11px;
    color: {theme.accent_secondary};
    letter-spacing: 1px;
    text-transform: uppercase;
}}

QLabel#achievement_name {{
    font-size: 14px;
    font-weight: bold;
    color: {theme.text_color};
}}

QLabel#achievement_desc {{
    font-size: 11px;
    color: {theme.accent_secondary};
}}

/* ─── SLIDER ─────────────────────────────────────────────── */
QSlider::groove:horizontal {{
    height: 6px;
    background-color: {theme.card_color};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background-color: {theme.accent_color};
    width: 16px;
    height: 16px;
    border-radius: 8px;
    margin: -5px 0;
}}

QSlider::sub-page:horizontal {{
    background-color: {theme.accent_color};
    border-radius: 3px;
}}

/* ─── CHECKBOXES ─────────────────────────────────────────── */
QCheckBox {{
    color: {theme.text_color};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {theme.card_border};
    background-color: {theme.card_color};
}}

QCheckBox::indicator:checked {{
    background-color: {theme.accent_color};
    border-color: {theme.accent_color};
}}
"""


def get_story_type_format(part_type: str, theme: GenreTheme) -> dict:
    """Return formatting hints for each story segment type."""
    formats = {
        "opening": {
            "color": theme.text_color,
            "size": 15,
            "bold": False,
            "italic": False,
            "prefix": "",
            "margin_top": 0,
        },
        "middle": {
            "color": theme.text_color,
            "size": 14,
            "bold": False,
            "italic": False,
            "prefix": "",
            "margin_top": 4,
        },
        "closing": {
            "color": theme.text_color,
            "size": 15,
            "bold": False,
            "italic": True,
            "prefix": "",
            "margin_top": 8,
        },
        "escalation": {
            "color": theme.highlight_color,
            "size": 12,
            "bold": True,
            "italic": False,
            "prefix": "",
            "margin_top": 4,
        },
        "fourth_wall": {
            "color": theme.accent_secondary,
            "size": 12,
            "bold": False,
            "italic": True,
            "prefix": "",
            "margin_top": 6,
        },
        "callback": {
            "color": theme.accent_color,
            "size": 12,
            "bold": False,
            "italic": True,
            "prefix": "",
            "margin_top": 2,
        },
        "author_comment": {
            "color": theme.accent_secondary,
            "size": 11,
            "bold": False,
            "italic": True,
            "prefix": "— ",
            "margin_top": 12,
        },
    }
    return formats.get(part_type, formats["middle"])
