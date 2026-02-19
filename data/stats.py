"""
MadVerse Stats & Achievements Tracker
Persists play stats and unlocks achievements.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


STATS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "stats.json")

ACHIEVEMENTS = [
    {
        "id": "first_story",
        "name": "Origin Story",
        "desc": "Generated your very first MadVerse tale.",
        "icon": "🌟",
        "condition": lambda s: s["total_stories"] >= 1,
    },
    {
        "id": "ten_stories",
        "name": "Prolific Chaos Merchant",
        "desc": "Generated 10 stories. Productivity, but wrong.",
        "icon": "📚",
        "condition": lambda s: s["total_stories"] >= 10,
    },
    {
        "id": "fifty_stories",
        "name": "Chaos Architect",
        "desc": "50 stories generated. You have a problem.",
        "icon": "🏛️",
        "condition": lambda s: s["total_stories"] >= 50,
    },
    {
        "id": "all_genres",
        "name": "Genre Omnivore",
        "desc": "Played every genre at least once.",
        "icon": "🎭",
        "condition": lambda s: len(s.get("genres_played", set())) >= 7,
    },
    {
        "id": "used_banana",
        "name": "Banana Connoisseur",
        "desc": "Used the word 'banana' in any story.",
        "icon": "🍌",
        "condition": lambda s: "banana" in [w.lower() for w in s.get("all_words_used", [])],
    },
    {
        "id": "horror_fan",
        "name": "Scared of Nothing",
        "desc": "Played Horror 5 times.",
        "icon": "🎃",
        "condition": lambda s: s.get("genre_counts", {}).get("horror", 0) >= 5,
    },
    {
        "id": "ai_explorer",
        "name": "Trust the Machine",
        "desc": "Used the AI Narrator genre.",
        "icon": "🤖",
        "condition": lambda s: s.get("genre_counts", {}).get("ai", 0) >= 1,
    },
    {
        "id": "ai_devotee",
        "name": "AI Devotee",
        "desc": "Used AI Narrator 5 times. Concerning.",
        "icon": "⚡",
        "condition": lambda s: s.get("genre_counts", {}).get("ai", 0) >= 5,
    },
    {
        "id": "saved_story",
        "name": "Literary Archivist",
        "desc": "Saved your first story to a file.",
        "icon": "💾",
        "condition": lambda s: s.get("stories_saved", 0) >= 1,
    },
    {
        "id": "same_words",
        "name": "New Story, Same Chaos",
        "desc": "Regenerated with the same words.",
        "icon": "🔁",
        "condition": lambda s: s.get("regenerations", 0) >= 1,
    },
    {
        "id": "chaos_session",
        "name": "Maximum Chaos",
        "desc": "Played 5 stories in a single session.",
        "icon": "🌪️",
        "condition": lambda s: s.get("session_stories", 0) >= 5,
    },
    {
        "id": "academic_pain",
        "name": "Peer Reviewed",
        "desc": "Survived the Academic genre 3 times.",
        "icon": "🏫",
        "condition": lambda s: s.get("genre_counts", {}).get("academic", 0) >= 3,
    },
    {
        "id": "existential_spiral",
        "name": "The Void Stares Back",
        "desc": "Played Existential 5 times. Are you okay?",
        "icon": "🧠",
        "condition": lambda s: s.get("genre_counts", {}).get("existential", 0) >= 5,
    },
    {
        "id": "word_recycler",
        "name": "Word Hoarder",
        "desc": "Used the same word 10+ times across stories.",
        "icon": "♻️",
        "condition": lambda s: any(v >= 10 for v in s.get("word_frequency", {}).values()),
    },
]


class StatsTracker:
    def __init__(self):
        self.data = self._load()
        self.session_stories = 0

    def _load(self) -> Dict:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    d = json.load(f)
                    # Convert lists back to sets where needed
                    d["genres_played"] = set(d.get("genres_played", []))
                    return d
            except Exception:
                pass
        return self._default_data()

    def _default_data(self) -> Dict:
        return {
            "total_stories": 0,
            "stories_saved": 0,
            "regenerations": 0,
            "genres_played": set(),
            "genre_counts": {},
            "all_words_used": [],
            "word_frequency": {},
            "unlocked_achievements": [],
            "session_stories": 0,
            "last_played": None,
            "favorite_genre": "none",
        }

    def _save(self):
        data = dict(self.data)
        data["genres_played"] = list(data["genres_played"])
        data["session_stories"] = self.session_stories
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def record_story(self, genre_id: str, words: Dict[str, str]) -> List[Dict]:
        """Record a story play and return newly unlocked achievements."""
        self.data["total_stories"] = self.data.get("total_stories", 0) + 1
        self.session_stories += 1
        self.data["session_stories"] = self.session_stories
        self.data["last_played"] = datetime.now().isoformat()

        # Genre tracking
        self.data["genres_played"].add(genre_id)
        gc = self.data.get("genre_counts", {})
        gc[genre_id] = gc.get(genre_id, 0) + 1
        self.data["genre_counts"] = gc

        # Update favorite genre
        self.data["favorite_genre"] = max(gc, key=gc.get)

        # Word tracking
        word_list = self.data.get("all_words_used", [])
        freq = self.data.get("word_frequency", {})
        for word in words.values():
            if word.strip():
                word_list.append(word.lower())
                freq[word.lower()] = freq.get(word.lower(), 0) + 1
        self.data["all_words_used"] = word_list[-500:]  # keep last 500
        self.data["word_frequency"] = freq

        newly_unlocked = self._check_achievements()
        self._save()
        return newly_unlocked

    def record_save(self):
        self.data["stories_saved"] = self.data.get("stories_saved", 0) + 1
        newly_unlocked = self._check_achievements()
        self._save()
        return newly_unlocked

    def record_regeneration(self):
        self.data["regenerations"] = self.data.get("regenerations", 0) + 1
        newly_unlocked = self._check_achievements()
        self._save()
        return newly_unlocked

    def _check_achievements(self) -> List[Dict]:
        """Check all achievements, return newly unlocked ones."""
        unlocked = self.data.get("unlocked_achievements", [])
        newly = []
        check_data = dict(self.data)
        check_data["session_stories"] = self.session_stories

        for ach in ACHIEVEMENTS:
            if ach["id"] not in unlocked:
                try:
                    if ach["condition"](check_data):
                        unlocked.append(ach["id"])
                        newly.append(ach)
                except Exception:
                    pass

        self.data["unlocked_achievements"] = unlocked
        return newly

    def get_most_used_word(self) -> str:
        freq = self.data.get("word_frequency", {})
        if not freq:
            return "none yet"
        return max(freq, key=freq.get)

    def get_stats_summary(self) -> Dict:
        return {
            "total_stories": self.data.get("total_stories", 0),
            "stories_saved": self.data.get("stories_saved", 0),
            "regenerations": self.data.get("regenerations", 0),
            "favorite_genre": self.data.get("favorite_genre") or "none",
            "most_used_word": self.get_most_used_word(),
            "genres_played": len(self.data.get("genres_played", set())),
            "achievements_unlocked": len(self.data.get("unlocked_achievements", [])),
            "total_achievements": len(ACHIEVEMENTS),
        }

    def get_all_achievements(self) -> List[Dict]:
        """Return all achievements with unlock status."""
        unlocked = self.data.get("unlocked_achievements", [])
        result = []
        for ach in ACHIEVEMENTS:
            result.append({
                **ach,
                "unlocked": ach["id"] in unlocked,
            })
        return result


# Singleton
_tracker: Optional[StatsTracker] = None

def get_tracker() -> StatsTracker:
    global _tracker
    if _tracker is None:
        _tracker = StatsTracker()
    return _tracker
