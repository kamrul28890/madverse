"""
MadVerse Story Engine
Handles randomized story assembly, humor amplifiers, callbacks, and escalation.
"""

import random
import re
from typing import Dict, List, Tuple, Optional
from data.genres import Genre


class StoryEngine:
    """
    Assembles a randomized story from genre templates and user-provided words.
    Injects humor amplifiers: callbacks, escalation, fourth-wall breaks, mismatches.
    """

    def __init__(self, genre: Genre, words: Dict[str, str]):
        self.genre = genre
        self.words = words
        self._used_callbacks: List[str] = []  # words that have appeared (for callbacks)
        self._story_parts: List[Dict] = []     # assembled story segments

    # ─────────────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────────────

    def generate(self) -> List[Dict]:
        """
        Returns a list of story segment dicts:
          {
            'text': str,
            'type': 'opening' | 'middle' | 'closing' | 'escalation' |
                    'fourth_wall' | 'callback' | 'author_comment',
            'emphasis_words': [str],  # words to visually highlight
          }
        """
        self._story_parts = []

        # 1. Opening
        opening = self._pick_and_fill(self.genre.opening_templates)
        self._add_part(opening, "opening")

        # 2. Middle (2–5 sentences, randomly ordered)
        pool = list(self.genre.middle_templates)
        random.shuffle(pool)
        count = random.randint(2, min(5, len(pool)))
        selected = pool[:count]

        for i, template in enumerate(selected):
            # Occasionally inject escalation prefix
            prefix = ""
            if i > 0 and random.random() < 0.35:
                esc = random.choice(self.genre.escalation_lines)
                prefix = self._fill(esc) + " "
                self._add_part(prefix.strip(), "escalation")

            filled = self._fill(template)

            # Random capitalization of the user's noun for dramatic effect
            filled = self._dramatic_capitalize(filled)

            self._add_part(filled, "middle")

            # Callback: reuse an earlier emphasized word in a new context
            if i == len(selected) - 2 and self._used_callbacks:
                cb = self._build_callback()
                if cb:
                    self._add_part(cb, "callback")

            # Fourth-wall break: ~25% chance per middle sentence
            if random.random() < 0.25 and self.genre.fourth_wall_lines:
                fw = random.choice(self.genre.fourth_wall_lines)
                fw_filled = self._fill(fw)
                self._add_part(fw_filled, "fourth_wall")

        # 3. Closing
        closing = self._pick_and_fill(self.genre.closing_templates)
        self._add_part(closing, "closing")

        # 4. Always end with a fourth-wall or author comment
        final_comments = [
            f"The {self.words.get('noun', 'noun')} could not be reached for comment.",
            f"This story was {self.words.get('adjective', 'adjective')} and we stand by it.",
            f"No {self.words.get('noun2', 'nouns')} were harmed in the making of this narrative.",
            f"Statistics show that {self.words.get('number', '0')}% of readers survived this story.",
            f"The author's feelings about the {self.words.get('object', 'object')} remain unresolved.",
        ]
        self._add_part(random.choice(final_comments), "author_comment")

        return self._story_parts

    # ─────────────────────────────────────────────────────────
    # INTERNAL HELPERS
    # ─────────────────────────────────────────────────────────

    def _pick_and_fill(self, templates: List[str]) -> str:
        if not templates:
            return ""
        template = random.choice(templates)
        return self._fill(template)

    def _fill(self, template: str) -> str:
        """Replace {key} placeholders with user words."""
        result = template
        for key, value in self.words.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, value)
                if value not in self._used_callbacks:
                    self._used_callbacks.append(value)
        # Clean up any unfilled placeholders
        result = re.sub(r'\{[^}]+\}', '___', result)
        return result

    def _dramatic_capitalize(self, text: str) -> str:
        """Randomly capitalize the user's noun for dramatic effect (30% chance)."""
        noun = self.words.get('noun', '')
        if noun and random.random() < 0.3 and noun.lower() in text.lower():
            text = re.sub(re.escape(noun), noun.upper(), text, count=1, flags=re.IGNORECASE)
        return text

    def _build_callback(self) -> Optional[str]:
        """Build a callback joke referencing a previously used word."""
        if not self._used_callbacks:
            return None
        word = random.choice(self._used_callbacks)
        templates = [
            f"(Yes, that {word} again. It keeps coming up. Nobody knows why.)",
            f"The {word}. Always the {word}. We should have seen this coming.",
            f"Historians would later identify the {word} as the turning point. Historians were baffled.",
            f"It bears repeating: the {word} was there before any of this started.",
            f"The {word} had been quietly {self.words.get('verb2', 'waiting')} this entire time.",
        ]
        return random.choice(templates)

    def _add_part(self, text: str, part_type: str):
        if not text.strip():
            return

        # Identify emphasis words (user's adjective, noun, name)
        emphasis = []
        for key in ['noun', 'adjective', 'name', 'emotion']:
            val = self.words.get(key, '')
            if val and val.lower() in text.lower():
                emphasis.append(val)

        # Also emphasize ALL-CAPS words
        caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
        emphasis.extend(caps_words)

        self._story_parts.append({
            'text': text,
            'type': part_type,
            'emphasis_words': list(set(emphasis)),
        })


def get_emphasis_ranges(text: str, words: List[str]) -> List[Tuple[int, int]]:
    """
    Returns list of (start, end) character ranges for words to highlight.
    """
    ranges = []
    for word in words:
        if not word:
            continue
        for match in re.finditer(re.escape(word), text, re.IGNORECASE):
            ranges.append((match.start(), match.end()))
    # Also highlight ALL-CAPS sequences
    for match in re.finditer(r'\b[A-Z]{3,}\b', text):
        ranges.append((match.start(), match.end()))
    return sorted(set(ranges))
