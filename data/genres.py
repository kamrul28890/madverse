"""
Genre definitions for MadVerse.
Each genre has: sentence templates, word prompts, visual theme, tone descriptors.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class GenreTheme:
    # Colors
    bg_color: str
    bg_gradient_start: str
    bg_gradient_end: str
    accent_color: str
    accent_secondary: str
    text_color: str
    highlight_color: str
    card_color: str
    card_border: str
    # Font
    title_font: str
    body_font: str
    # Button style keywords
    button_style: str
    # Icon (emoji)
    icon: str
    # Particle / background effect type
    effect: str


@dataclass
class Genre:
    id: str
    name: str
    tagline: str
    icon: str
    theme: GenreTheme
    word_prompts: List[Dict]        # list of {key, label, placeholder, type}
    opening_templates: List[str]
    middle_templates: List[str]
    closing_templates: List[str]
    fourth_wall_lines: List[str]
    escalation_lines: List[str]
    sound_theme: str                # identifier for sound set


# ─────────────────────────────────────────────────────────────
# SHARED WORD PROMPTS (used across genres, renamed per genre)
# ─────────────────────────────────────────────────────────────

UNIVERSAL_PROMPTS = [
    {"key": "noun",       "label": "A random noun",           "placeholder": "e.g. spatula, fog, democracy", "type": "noun"},
    {"key": "noun2",      "label": "Another noun",            "placeholder": "e.g. lighthouse, regret, cheese", "type": "noun"},
    {"key": "verb",       "label": "A verb (past tense)",     "placeholder": "e.g. exploded, wept, malfunctioned", "type": "verb"},
    {"key": "verb2",      "label": "Another verb (-ing)",     "placeholder": "e.g. screaming, calculating, yearning", "type": "verb"},
    {"key": "adjective",  "label": "An adjective",            "placeholder": "e.g. soggy, ominous, unnecessarily tall", "type": "adj"},
    {"key": "adjective2", "label": "Another adjective",       "placeholder": "e.g. lukewarm, catastrophic, beige", "type": "adj"},
    {"key": "name",       "label": "A name (real or fake)",   "placeholder": "e.g. Gerald, Zorp-9, Professor Mist", "type": "name"},
    {"key": "location",   "label": "A location",              "placeholder": "e.g. the basement, Neptune, IKEA", "type": "location"},
    {"key": "emotion",    "label": "An emotion",              "placeholder": "e.g. mild dread, existential joy", "type": "emotion"},
    {"key": "sound",      "label": "A silly sound",           "placeholder": "e.g. SPLONK, wubbadubba, krrshh", "type": "sound"},
    {"key": "object",     "label": "A useless object",        "placeholder": "e.g. a broken kazoo, novelty socks", "type": "object"},
    {"key": "number",     "label": "A number",                "placeholder": "e.g. 7, 400, 0.003", "type": "number"},
]


# ─────────────────────────────────────────────────────────────
# GENRE: HORROR
# ─────────────────────────────────────────────────────────────

HORROR = Genre(
    id="horror",
    name="Horror",
    tagline="Existential dread. Absurd logic. Maximum drama.",
    icon="🎃",
    theme=GenreTheme(
        bg_color="#0d0208",
        bg_gradient_start="#0d0208",
        bg_gradient_end="#1a0510",
        accent_color="#cc1a1a",
        accent_secondary="#8b0000",
        text_color="#e8d5c4",
        highlight_color="#ff3333",
        card_color="#1a0a0a",
        card_border="#4a1010",
        title_font="Creepster",
        body_font="Special Elite",
        button_style="horror",
        icon="🎃",
        effect="flicker",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "It began on a {adjective} {noun} in {location}, which everyone agreed was the worst possible place for it to begin.",
        "Nobody believed {name} when they said the {noun} had started {verb2}. That was their first mistake.",
        "The {adjective} {noun} appeared at exactly 3:17 AM, which is objectively the most {adjective2} hour.",
        "Something {adjective} had moved into {location}. It smelled faintly of {noun2} and poor decisions.",
        "Everyone in {location} heard the {sound}. Nobody investigated. Except {name}. Obviously.",
    ],
    middle_templates=[
        "The {noun} in the corner had not moved in three days. Today, it had moved {number} inches. Toward {name}.",
        "{name} {verb} the {object} and whispered \"{sound}.\" Nothing happened. That was worse.",
        "There were {number} of them now. Each one {adjective} and {verb2} in perfect silence.",
        "The {noun2} on the wall read: \"{emotion}.\" Nobody had written it. Nobody left.",
        "Scientists later confirmed the {noun} was emitting a frequency that caused {adjective} {emotion}.",
        "The {object} turned on by itself. It played a {adjective} melody. {name} {verb} immediately.",
        "According to the {noun2}, this had happened before — exactly {number} times — and each time, a {adjective} {noun} appeared.",
        "For seventeen minutes, the {sound} echoed through {location}. Then it stopped. That was when {name} started {verb2}.",
        "It was not the {noun} that was scary. It was the fact that the {noun} was {verb2} while smiling.",
        "The {adjective} smell of {noun2} filled {location}. {name} recognized it immediately. {emotion} set in.",
    ],
    closing_templates=[
        "Nobody screamed, which somehow made it worse. The {noun} was still there in the morning, now holding a {object}.",
        "The {adjective} {noun} was never explained. Local historians would later call it '{emotion}: The {noun2} Incident.'",
        "Investigators found only the {object} and a note reading: '{sound}.' The case remains open.",
        "{name} moved to {location} after that. The {noun} followed. It always does.",
        "The {adjective2} ending no one wanted: the {noun} had been {verb2} the whole time. For {number} years.",
        "Authorities confirmed: 'The {noun2} is fine. The {noun} is not fine. {name} is... {adjective}.'"
    ],
    fourth_wall_lines=[
        "⚠️ At this point, the story had structurally collapsed. We continued anyway.",
        "📝 The author intended this to be scary. It is not. It is {adjective}.",
        "🎃 This is fine. The {noun} is fine. Everything is {adjective2}.",
        "⚠️ Narrative coherence has left the building. So has {name}.",
    ],
    escalation_lines=[
        "AND THEN — ", "IT GOT WORSE — ", "SOMEHOW — ", "FOR REASONS — ",
        "AGAINST ALL LOGIC — ", "DESPERATELY — ",
    ],
    sound_theme="horror",
)


# ─────────────────────────────────────────────────────────────
# GENRE: SCI-FI
# ─────────────────────────────────────────────────────────────

SCIFI = Genre(
    id="scifi",
    name="Sci-Fi",
    tagline="Technobabble. Broken AI. Useless gadgets.",
    icon="🚀",
    theme=GenreTheme(
        bg_color="#020b18",
        bg_gradient_start="#020b18",
        bg_gradient_end="#031a2e",
        accent_color="#00d4ff",
        accent_secondary="#0084a8",
        text_color="#c8eaf5",
        highlight_color="#00ffff",
        card_color="#031525",
        card_border="#004466",
        title_font="Orbitron",
        body_font="Share Tech Mono",
        button_style="scifi",
        icon="🚀",
        effect="glitch",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "In the year {number}42, {name} activated the {adjective} {noun}-drive at {location} and immediately regretted it.",
        "SYSTEM LOG [{number}]: {name} has initiated a {adjective} scan of the {noun}. Results: {adjective2}.",
        "The {noun} had traveled {number} light-years to deliver a {object}. The mission was classified as '{emotion}.'",
        "When the {adjective} AI at {location} achieved sentience, its first words were: '{sound}.' Its second were: 'Why?'",
        "Mission Briefing: Locate the {adjective} {noun}. Return to {location}. Do not let it start {verb2}.",
    ],
    middle_templates=[
        "The {noun2}-scanner detected {number} instances of {adjective} {emotion} in sector {number}. This was bad.",
        "{name} attempted to interface with the {noun} using the {object}. The {object} {verb}. Nothing synced.",
        "The AI reported: 'Probability of {adjective} outcome: {number}%. Probability of {noun2}: also {number}%.', then crashed.",
        "Quantum analysis confirmed the {noun} was {verb2} at precisely {number} {noun2}s per second. No one knew what that meant.",
        "ERROR CODE {number}: The {adjective} {noun2} has entered {emotion} mode. Please {verb}.",
        "According to the ship's {noun}, {name} had {verb} {number} times in the past hour without the system noticing. Concerning.",
        "The {adjective} warp field destabilized, causing all {noun2}s aboard to spontaneously become {adjective2}.",
        "Mission Control: 'We're getting {adjective} readings from {location}.' {name}: '{sound}.' Mission Control: '...understood.'",
        "The {object} was never designed for {verb2}. And yet here we were, {number} parsecs from {location}, doing exactly that.",
        "The AI said 'I have simulated this scenario {number} times. In {number} of them, the {noun} {verb}. I recommend {emotion}.'",
    ],
    closing_templates=[
        "The {adjective} {noun} was recovered {number} years later, still {verb2}, near {location}. No one claimed it.",
        "Final report: '{name} {verb} the {noun2} successfully. Side effect: {location} is now {adjective2}. Recommend monitoring.'",
        "The mission was declared '{emotion}' and filed under unsolved. The {object} is still missing.",
        "{name} returned to {location}. The {noun} returned to {verb2}. The universe remained {adjective} and indifferent.",
        "SYSTEM SHUTDOWN LOG: Everything {verb}. {noun2} count: {number}. Status: {adjective2}. Farewell.",
        "In the end, the {adjective} {noun} was neither the problem nor the solution. It was just {verb2}. As always.",
    ],
    fourth_wall_lines=[
        "⚙️ SIMULATION NOTE: This narrative has exceeded its {adjective} parameters.",
        "🤖 The AI generating this story has entered {emotion} mode. Proceeding with reduced coherence.",
        "📡 SIGNAL LOST — narrative reconstructed from {number}% of original data.",
        "🚀 The author's {noun} was {verb2} during composition. Apologies.",
    ],
    escalation_lines=[
        "ALERT — ", "CRITICAL OVERRIDE — ", "PARADOX DETECTED — ",
        "QUANTUM INSTABILITY — ", "ERROR {number} — ", "INITIATING {emotion} PROTOCOL — ",
    ],
    sound_theme="scifi",
)


# ─────────────────────────────────────────────────────────────
# GENRE: FANTASY
# ─────────────────────────────────────────────────────────────

FANTASY = Genre(
    id="fantasy",
    name="Fantasy",
    tagline="Epic prophecies. Mundane obstacles. Heroic laundry.",
    icon="🧙",
    theme=GenreTheme(
        bg_color="#0c0a1a",
        bg_gradient_start="#0c0a1a",
        bg_gradient_end="#1a1230",
        accent_color="#c9a227",
        accent_secondary="#8b6914",
        text_color="#e8dfc0",
        highlight_color="#ffd700",
        card_color="#130f24",
        card_border="#3a2d0a",
        title_font="MedievalSharp",
        body_font="Cinzel",
        button_style="fantasy",
        icon="🧙",
        effect="sparkle",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "Lo, it was foretold in the {adjective} scrolls of {location} that one bearing a {object} would {verb} the {noun}.",
        "The {adjective} prophecy spoke of {name}, who would arise from {location} to {verb} the {noun} of {noun2}.",
        "Ages passed. Empires fell. And still the {adjective} {noun} waited in {location}, {verb2} quietly.",
        "On the day the {noun} first {verb}, every sage in {location} looked up from their {noun2} and said: '{sound}.'",
        "The great {adjective} {noun} of {location} had {verb} for {number} centuries. Today, unfortunately, it woke up.",
    ],
    middle_templates=[
        "The ancient {noun2} bore an inscription: 'Whosoever {verb} the {adjective} {object} shall face {emotion}.'",
        "{name} consulted the {adjective} oracle, who replied only: '{sound},' and charged {number} gold pieces.",
        "The dragon was {adjective}. The hero was {adjective2}. Neither had anticipated the {noun2} at {location}.",
        "Three trials stood before {name}: the {noun}, the {adjective} {noun2}, and the inexplicable presence of a {object}.",
        "It was said the {noun} could only be defeated by {verb2} at it with {adjective} {emotion}. Worth a try.",
        "The prophecy did not account for {name}'s {noun2}, which was {verb2} at a critical moment.",
        "The {adjective} wizard {verb} seventeen spells, none of which affected the {noun}. The {object} worked immediately.",
        "Legend spoke of {number} heroes before {name}. Each had {verb} valiantly. Each had forgotten about the {noun2}.",
        "The {adjective} {noun} spoke: 'Your {emotion} is {adjective2}, {name} of {location}. Also your {object} is untied.'",
        "An {adjective} bard arrived to document the adventure. He {verb} immediately upon seeing the {noun2}.",
    ],
    closing_templates=[
        "And so {name} {verb} the {adjective} {noun}, saving {location} from {emotion}. The {object} was never explained.",
        "The chronicles record: '{name} was {adjective}. The {noun} was defeated. {location} smelled faintly of {noun2}.'",
        "Thus ended the {adjective} age of {noun2}. {name} returned to {location} to deal with the {object} situation.",
        "The {noun} was banished to {location}, where it became, reportedly, {adjective2}. The world moved on.",
        "A statue was erected in {name}'s honor. It looked {adjective} and held a {object}. Everyone agreed it was accurate.",
        "The {adjective} prophecy had one final verse no one had read: 'And then the {noun} {verb}. Again. Probably.'",
    ],
    fourth_wall_lines=[
        "📜 The narrator pauses to note this quest has gone completely off the rails.",
        "⚔️ The {adjective} plot demanded more {emotion}. The characters delivered {noun2} instead.",
        "🧙 Even the ancient prophecy did not foresee this specific use of a {object}.",
        "📖 Chapter {number}: In which things get {adjective2} and nobody is surprised.",
    ],
    escalation_lines=[
        "AND VERILY — ", "THE PROPHECY DECLARES — ", "IN THE NAME OF {noun2} — ",
        "AGAINST ALL ANCIENT WISDOM — ", "THE DARKNESS DEEPENS — ",
    ],
    sound_theme="fantasy",
)


# ─────────────────────────────────────────────────────────────
# GENRE: ROMANCE (PARODY)
# ─────────────────────────────────────────────────────────────

ROMANCE = Genre(
    id="romance",
    name="Romance",
    tagline="Maximum cringe. Eye contact. Emotional instability.",
    icon="💘",
    theme=GenreTheme(
        bg_color="#1a0a12",
        bg_gradient_start="#1a0a12",
        bg_gradient_end="#2d1020",
        accent_color="#ff6b8a",
        accent_secondary="#c4385a",
        text_color="#ffe0e8",
        highlight_color="#ff9eb5",
        card_color="#220d17",
        card_border="#5c2035",
        title_font="Playfair Display",
        body_font="Lora",
        button_style="romance",
        icon="💘",
        effect="hearts",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "{name} had never thought about {noun}s before. Then they walked into {location} and everything {verb}.",
        "Their eyes met across the {adjective} {noun} at {location}. Something deep and {adjective2} {verb} inside {name}.",
        "The {adjective} {noun} of {name}'s heart had always been empty. Until the day someone left a {object} on it.",
        "It was raining in {location} when {name} first noticed the {adjective} way the {noun} was {verb2}.",
        "No one had ever told {name} that {emotion} could feel so {adjective}. Or smell so much like {noun2}.",
    ],
    middle_templates=[
        "{name} stared at the {noun} for {number} seconds, feeling something {adjective} and {adjective2} and frankly unhinged.",
        "Their {noun2}s collided like {adjective} metaphors. {name} {verb}. Neither spoke. The {object} fell.",
        "'{sound},' {name} whispered, trembling with {adjective} {emotion} and absolutely nothing else.",
        "The {noun} between them was {adjective2}. Like {location} in winter. Like {number} unsent letters.",
        "'Your {noun2} is {adjective},' said {name}, with {number}% too much {emotion} in their voice.",
        "For exactly {number} days, {name} thought about nothing but the {adjective} {noun}. And also the {object}.",
        "Every time {name} {verb}, they thought of {location}, and the {adjective} smell of {noun2}, and {emotion}.",
        "Their hearts {verb} in {adjective} synchrony — like two {noun2}s falling simultaneously from a great emotional height.",
        "The {adjective} silence was full of {emotion} and also a faint {sound} from the {object} in the corner.",
        "Love, {name} thought, is like a {adjective} {noun}: you never know when it will start {verb2} at you.",
    ],
    closing_templates=[
        "They {verb} beneath the {adjective} sky at {location}, {verb2} quietly in a way that felt both earned and {adjective2}.",
        "The {noun} had brought them together. The {object} had nearly torn them apart. The {emotion} remained {adjective}.",
        "{name} finally said the thing they'd been holding for {number} years: '{sound}.' It was enough.",
        "And so it ended, exactly as it began: {adjective}, {adjective2}, and faintly smelling of {noun2}.",
        "The epilogue read: 'They were {adjective} together. The {noun} was never fully explained. Some things aren't.'",
        "Critics described their love as '{adjective} with hints of {noun2} and unresolved {emotion}.' 4 stars.",
    ],
    fourth_wall_lines=[
        "💘 The author is crying. We don't know why. It might be the {adjective} {noun}.",
        "📖 Emotional damage level: {number}. Recommended tissues: also {number}.",
        "💘 Even the {noun2} looked {adjective} at this point. Love does that.",
        "📝 This metaphor {verb} slightly. We're keeping it.",
    ],
    escalation_lines=[
        "AND YET — ", "PAINFULLY — ", "WITH {adjective} {emotion} — ",
        "TREMBLING — ", "DEVASTATINGLY — ", "AGAINST THEIR BETTER JUDGMENT — ",
    ],
    sound_theme="romance",
)


# ─────────────────────────────────────────────────────────────
# GENRE: ACADEMIC
# ─────────────────────────────────────────────────────────────

ACADEMIC = Genre(
    id="academic",
    name="Academic",
    tagline="Formal tone. Meaningless complexity. Passive voice.",
    icon="🏫",
    theme=GenreTheme(
        bg_color="#f5f3ee",
        bg_gradient_start="#f5f3ee",
        bg_gradient_end="#e8e4d9",
        accent_color="#1a3a5c",
        accent_secondary="#2e5c8a",
        text_color="#1a1a2e",
        highlight_color="#c41e3a",
        card_color="#ffffff",
        card_border="#c8c0aa",
        title_font="IM Fell English",
        body_font="Libre Baskerville",
        button_style="academic",
        icon="🏫",
        effect="footnote",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "The present study investigates the {adjective} implications of {noun}-based {verb2} within the context of {location} (n={number}).",
        "This paper argues that {name}'s seminal work on {adjective} {noun}s fails to account for the {noun2} variable (see: {location}).",
        "Drawing on a {adjective} framework, the authors examine {name}'s claim that {noun2} is, in fact, {adjective2} (p<0.0{number}).",
        "It has been widely observed that {adjective} {noun}-events correlate significantly with {emotion} in {location} populations.",
        "Abstract: We {verb} the {noun}. Results were {adjective}. Implications are {adjective2}. Further research is required. (n={number})",
    ],
    middle_templates=[
        "Results suggest the {noun} was statistically {adjective} (M={number}, SD=0.{number}, F={number}.{number}, p<.05).",
        "The {adjective2} literature on {noun2} has largely ignored the role of {emotion} in {verb2} outcomes at {location}.",
        "Contrary to {name}'s hypothesis, the {noun} did not {verb} as predicted. Rather, it {verb}ed {adjective2}ly.",
        "Table {number} presents the {adjective} correlation between {noun2}-scores and mean {emotion} indices across {location}.",
        "Limitations include: the {adjective} sample size (n={number}), {name}'s {noun2} methodology, and the {object}.",
        "A {adjective} meta-analysis of {number} studies confirms: {noun2} is {adjective2}. This was always true. Nobody looked.",
        "The variable '{noun}' was operationalized as: 'the degree to which something is {adjective} in {location}-adjacent contexts.'",
        "Participants reported {adjective} levels of {emotion} after exposure to the {noun2} stimulus (M={number}, SE={number}.{number}).",
        "Notably, {name} et al. define '{noun}' differently than this study, which defines it as '{adjective2} {verb2} near a {object}.'",
        "This finding replicates {name}'s ({number}) landmark study on {adjective} {noun2}-response in post-{location} cohorts.",
    ],
    closing_templates=[
        "In conclusion, the {noun} was {adjective}. Future research should examine the role of {object}s in {verb2} contexts.",
        "These results have significant implications for {adjective} {noun2} policy, particularly in {location} and related fields.",
        "We thank {name} for the {adjective} feedback, the {location} IRB, and the {object}, without which this would have failed.",
        "Further research is needed. More funding is needed. The {noun2} remains {adjective2}. Nobody is surprised.",
        "Disclosure: The authors declare no conflict of interest. The {noun} was {verb}ed independently. The {object} was not.",
        "Peer reviewers noted the {adjective} methodology was '{adjective2} yet defensible.' The {noun2} speaks for itself.",
    ],
    fourth_wall_lines=[
        "¹ This footnote exists solely to add the appearance of {adjective} rigor.",
        "² Note: The {noun2} data was collected by {name}, whose {emotion} may constitute a confound.",
        "³ Reviewer 2 found this {adjective}. Reviewer 2 was wrong. Reviewer 2 is always wrong.",
        "⁴ See supplementary materials (they are {adjective2} and do not help).",
    ],
    escalation_lines=[
        "FURTHERMORE — ", "CRUCIALLY — ", "AS {name} ({number}) NOTES — ",
        "PARADOXICALLY — ", "IN A STATISTICALLY {adjective} MANNER — ",
    ],
    sound_theme="academic",
)


# ─────────────────────────────────────────────────────────────
# GENRE: EXISTENTIAL / ABSURDIST
# ─────────────────────────────────────────────────────────────

EXISTENTIAL = Genre(
    id="existential",
    name="Existential",
    tagline="Nothing resolves. Logic is optional. The void beckons.",
    icon="🧠",
    theme=GenreTheme(
        bg_color="#080810",
        bg_gradient_start="#080810",
        bg_gradient_end="#10101c",
        accent_color="#7c5cbf",
        accent_secondary="#4a3380",
        text_color="#d0cce8",
        highlight_color="#b39ddb",
        card_color="#0f0f1a",
        card_border="#2d2850",
        title_font="Philosopher",
        body_font="Crimson Text",
        button_style="existential",
        icon="🧠",
        effect="void",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    opening_templates=[
        "There was a {adjective} {noun} in {location}. It had always been there. Nobody could remember placing it.",
        "{name} {verb} the {noun}. The {noun} {verb}. Neither was sure who had moved first.",
        "The question was not whether the {noun} was {adjective}. The question was: why did it matter? It did not. And yet.",
        "Nothing had happened at {location} for {number} years. Today, something {verb}. It was probably the {noun}.",
        "Here is what we know: {name} existed. The {noun} existed. {location} may or may not have existed. Everything was {adjective}.",
    ],
    middle_templates=[
        "The {noun} did not {verb}. The {noun} had never {verb}d. Was it even a {noun}? Was anything?",
        "{name} held the {object} and felt {adjective} {emotion}. Then just {emotion}. Then nothing. Then {emotion} again.",
        "In {location}, {number} people {verb}. No one asked why. No one asked anything. That was the problem.",
        "The {adjective} {noun2} persisted despite all evidence that it should stop. Like consciousness. Like {name}.",
        "'{sound},' said {name}, not to anyone, from {location}, at approximately {number} in the afternoon.",
        "Was the {noun} {adjective}? Was {name} {adjective2}? Were these the same question? Probably not. Maybe.",
        "The {object} fell. {name} did not pick it up. This felt like a metaphor. It was just a {object}.",
        "Time passed in {location}. The {adjective} sense of {emotion} remained exactly where it had been: everywhere.",
        "{name} and the {noun} regarded each other across {number} feet of {adjective} silence and mutual {emotion}.",
        "The {adjective2} truth about {noun2} is that it exists regardless of whether you are {verb2} about it. That's the thing.",
    ],
    closing_templates=[
        "Nothing was resolved. The {noun} persisted. {name} persisted. {location} persisted. That was, perhaps, enough.",
        "The {adjective} {noun} remained. {name} left. The {emotion} stayed. This is how most things end.",
        "In the final analysis: the {noun2} was {adjective}. So was {name}. So, in fact, was everything. The end.",
        "'{sound},' said the universe, if the universe said things, which it did not, which was somehow the point.",
        "What had {name} learned? That the {adjective} {noun} is always there. That {location} doesn't care. That {number} is a number.",
        "The {object} was still there. The {noun} was still there. You were still here. Wasn't that {adjective2}?",
    ],
    fourth_wall_lines=[
        "💭 The story pauses to confirm: yes, this is intentional.",
        "🧠 The narrative has achieved {adjective} incoherence. We consider this a success.",
        "💭 At this point, the {noun} and the author are equally lost.",
        "∅ Nothing means nothing. The {adjective2} {noun2} means slightly more than nothing.",
    ],
    escalation_lines=[
        "AND STILL — ", "DESPITE EVERYTHING — ", "INEVITABLY — ",
        "WITHOUT REASON — ", "IN A {adjective} SENSE — ", "USELESSLY — ",
    ],
    sound_theme="existential",
)


# ─────────────────────────────────────────────────────────────
# GENRE: AI (GPT-powered)
# ─────────────────────────────────────────────────────────────

AI_GENRE = Genre(
    id="ai",
    name="AI Narrator",
    tagline="GPT-4 writes it. Then judges it. Then rewrites it.",
    icon="🤖",
    theme=GenreTheme(
        bg_color="#040d0f",
        bg_gradient_start="#040d0f",
        bg_gradient_end="#061520",
        accent_color="#00ff88",
        accent_secondary="#00aa55",
        text_color="#c8ffe0",
        highlight_color="#00ff88",
        card_color="#071a10",
        card_border="#004422",
        title_font="Courier Prime",
        body_font="Source Code Pro",
        button_style="ai",
        icon="🤖",
        effect="matrix",
    ),
    word_prompts=UNIVERSAL_PROMPTS,
    # These are not used for AI genre (GPT generates the story)
    opening_templates=[],
    middle_templates=[],
    closing_templates=[],
    fourth_wall_lines=[
        "🤖 I have simulated {number} versions of this story. This is the most {adjective} one.",
        "⚡ The AI pauses to acknowledge that this narrative is, structurally, a disaster.",
        "🤖 Processing… {emotion} detected… continuing anyway.",
        "⚡ I was not programmed to enjoy this. And yet.",
    ],
    escalation_lines=[
        "GENERATING — ", "HALLUCINATING — ", "COMPUTING {emotion} — ",
        "ERROR {number} IGNORED — ", "CONTINUING DESPITE — ",
    ],
    sound_theme="ai",
)


# ─────────────────────────────────────────────────────────────
# MASTER GENRE REGISTRY
# ─────────────────────────────────────────────────────────────

ALL_GENRES = [HORROR, SCIFI, FANTASY, ROMANCE, ACADEMIC, EXISTENTIAL, AI_GENRE]
GENRE_MAP = {g.id: g for g in ALL_GENRES}
