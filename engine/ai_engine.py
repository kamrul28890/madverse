"""
MadVerse AI Story Engine
Uses Azure OpenAI GPT-4 to generate AND narrate the story with a creative twist.
"""

import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional

try:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import keys
    AZURE_KEY = keys.azure_openai_key
    AZURE_ENDPOINT = keys.azure_openai_endpoint
except Exception:
    AZURE_KEY = ""
    AZURE_ENDPOINT = ""


SYSTEM_PROMPT = """You are MadVerse AI — a chaotic, self-aware story narrator who generates hilariously absurd Mad Libs stories.

You will receive a set of user-provided words and a chosen sub-genre/mood. Your job is to:
1. Generate a short mad-libs style story (5-8 sentences) using ALL the provided words, weaving them in naturally but in unexpected, funny, or wrong grammatical contexts.
2. Add an "AI twist" — at least one moment where you break the fourth wall and comment on how chaotic the story is becoming.
3. End with a "narrator commentary" — 1 sentence where you, as the AI, reflect on what just happened.

RULES:
- Use every single provided word at least once
- Use some words in the wrong grammatical form on purpose (for comedy)
- Randomly capitalize IMPORTANT words for dramatic effect
- Add parenthetical side-comments from the narrator mid-story
- The story should escalate from mildly chaotic to completely unhinged
- The final narrator commentary should sound like a confused but proud AI

OUTPUT FORMAT (JSON only, no markdown):
{
  "story_parts": [
    {"text": "...", "type": "opening"},
    {"text": "...", "type": "middle"},
    {"text": "...", "type": "middle"},
    {"text": "...", "type": "fourth_wall"},
    {"text": "...", "type": "middle"},
    {"text": "...", "type": "escalation"},
    {"text": "...", "type": "closing"},
    {"text": "...", "type": "author_comment"}
  ],
  "ai_reflection": "One sentence from the AI about what just happened",
  "chaos_level": 1-10,
  "best_word": "the word you enjoyed using most"
}

Types available: opening, middle, closing, fourth_wall, escalation, callback, author_comment
"""


class AIStoryEngine:
    """
    Generates a full MadVerse story using Azure OpenAI GPT-4.
    Returns same format as StoryEngine for compatibility.
    """

    def __init__(self, words: Dict[str, str], sub_genre: str = "chaotic absurdist"):
        self.words = words
        self.sub_genre = sub_genre
        self.ai_reflection: Optional[str] = None
        self.chaos_level: int = 0
        self.best_word: Optional[str] = None
        self.error: Optional[str] = None

    def generate(self) -> List[Dict]:
        """
        Calls GPT-4 and returns story parts in the same format as StoryEngine.
        On error, returns a fallback error story.
        """
        if not AZURE_KEY or not AZURE_ENDPOINT:
            return self._error_story("API keys not configured. Check keys.py.")

        user_message = self._build_user_message()

        payload = json.dumps({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1200,
            "temperature": 1.1,
            "top_p": 0.95,
        }).encode("utf-8")

        req = urllib.request.Request(
            AZURE_ENDPOINT,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "api-key": AZURE_KEY,
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return self._error_story(f"HTTP {e.code}: {body[:200]}")
        except Exception as e:
            return self._error_story(str(e))

        # Parse GPT response
        try:
            content = data["choices"][0]["message"]["content"]
            # Strip any markdown code fences
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            parsed = json.loads(content)
        except Exception as e:
            return self._error_story(f"Failed to parse AI response: {e}")

        # Store metadata
        self.ai_reflection = parsed.get("ai_reflection", "")
        self.chaos_level = parsed.get("chaos_level", 5)
        self.best_word = parsed.get("best_word", "")

        parts = parsed.get("story_parts", [])
        if not parts:
            return self._error_story("AI returned empty story.")

        # Inject emphasis words into each part
        for part in parts:
            emphasis = []
            for word in self.words.values():
                if word and word.lower() in part.get("text", "").lower():
                    emphasis.append(word)
            part["emphasis_words"] = emphasis

        # Add reflection as author_comment if present
        if self.ai_reflection:
            parts.append({
                "text": f"🤖 AI REFLECTION: {self.ai_reflection}",
                "type": "author_comment",
                "emphasis_words": [],
            })

        return parts

    def _build_user_message(self) -> str:
        word_list = "\n".join(
            f"  - {k}: \"{v}\"" for k, v in self.words.items() if v.strip()
        )
        return (
            f"Sub-genre/mood: {self.sub_genre}\n\n"
            f"User-provided words:\n{word_list}\n\n"
            "Generate the story now."
        )

    def _error_story(self, message: str) -> List[Dict]:
        self.error = message
        return [
            {
                "text": "🤖 The AI attempted to generate your story...",
                "type": "opening",
                "emphasis_words": [],
            },
            {
                "text": f"...but encountered an error: {message}",
                "type": "middle",
                "emphasis_words": [],
            },
            {
                "text": "The AI is deeply sorry and slightly embarrassed about this.",
                "type": "closing",
                "emphasis_words": ["sorry", "embarrassed"],
            },
            {
                "text": "🤖 AI NOTE: I tried. I really did. The API had other plans.",
                "type": "author_comment",
                "emphasis_words": [],
            },
        ]


AI_SUB_GENRES = [
    "chaotic absurdist",
    "overly dramatic",
    "fake academic",
    "corporate memo gone wrong",
    "motivational poster disaster",
    "nature documentary narrator",
    "conspiracy theorist",
    "exhausted robot",
    "enthusiastic toddler",
    "passive-aggressive office AI",
]
