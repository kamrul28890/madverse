"""
MadVerse AI Worker Thread
Runs AI story generation in a background thread to keep UI responsive.
"""

from PyQt6.QtCore import QThread, pyqtSignal


class AIWorker(QThread):
    """
    Background thread for AI story generation.
    Emits finished(parts) or error(str).
    """
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, words: dict, sub_genre: str, parent=None):
        super().__init__(parent)
        self.words = words
        self.sub_genre = sub_genre
        self._engine = None

    def run(self):
        try:
            from engine.ai_engine import AIStoryEngine
            engine = AIStoryEngine(self.words, self.sub_genre)
            self._engine = engine
            parts = engine.generate()
            self.finished.emit(parts)
        except Exception as e:
            self.error.emit(str(e))

    def get_engine(self):
        return self._engine
