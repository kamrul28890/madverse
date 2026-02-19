# 🎭 MadVerse

**A Genre-Based, Randomized Mad Libs Game with AI-Powered Story Generation**

MadVerse is an interactive storytelling application that combines the classic Mad Libs gameplay with modern AI integration and beautiful GUI design. Generate hilarious, genre-specific stories by providing words, then watch as the AI assembles them into chaotic narratives with callbacks, escalations, and fourth-wall breaks.

---

## ✨ Features

- **Multiple Genres**: Fantasy, Science Fiction, Horror, Romance, Academic, Existential, and more
- **AI-Powered Story Generation**: Dynamic story assembly with humor amplification techniques
- **Interactive Gameplay**: Real-time word input with visual feedback
- **Sophisticated Humor Engine**: 
  - Callbacks and story callbacks for recurring jokes
  - Escalation mechanics for tension building
  - Fourth-wall breaks for meta humor
  - Mismatches and unexpected twists
- **Beautiful UI**: Genre-specific theming with custom colors, gradients, and effects
- **Sound Design**: Contextual audio feedback and genre-based background music
- **Statistics Tracking**: Track your most hilarious creations
- **Audio Feedback**: Click sounds, typing effects, and completion notifications

---

## 🎮 Gameplay Style

1. **Genre Selection**: Choose your preferred storytelling genre from the available options
2. **Word Input**: Provide words for specific prompts (nouns, adjectives, verbs, etc.)
3. **Story Generation**: Watch as MadVerse generates a unique, hilarious story
4. **Story Reveal**: Enjoy the finished story with highlighted key phrases and sound effects
5. **Stats Tracking**: View your story statistics and gameplay history

Each playthrough generates a completely randomized narrative, ensuring infinite replayability and unexpected humor combinations.

---

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB recommended
- **Internet**: Required for AI story generation via Azure OpenAI API

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/kamrul28890/madverse.git
cd madverse
```

### Step 2: Create a Virtual Environment
```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
Create or update `keys.py` with your Azure OpenAI credentials:
```python
azure_openai_key = "YOUR_AZURE_OPENAI_KEY"
azure_openai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
azure_openai_region = "YOUR_AZURE_REGION"
azure_openai_api_version = "2024-08-01-preview"

azure_key = "YOUR_AZURE_KEY"
azure_endpoint = "YOUR_AZURE_ENDPOINT"
azure_region = "YOUR_AZURE_REGION"
```

**Note**: `keys.py` is gitignored for security. Never commit sensitive credentials to version control.

---

## ▶️ Running the Application

### Quick Start
```bash
python main.py
```

The application will launch a PyQt6-based GUI window with the main menu.

### From Virtual Environment
```bash
# Make sure your virtual environment is activated
source .venv/bin/activate  # macOS/Linux
python main.py
```

---

## 📁 Project Structure

```
madverse/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── keys.py                    # API credentials (gitignored)
├── audio/
│   ├── sounds.py             # Sound management and playback
│   └── __init__.py
├── data/
│   ├── genres.py             # Genre definitions and themes
│   ├── stats.py              # Statistics tracking
│   ├── stats.json            # Persisted statistics
│   └── __init__.py
├── engine/
│   ├── story_engine.py       # Story generation logic
│   ├── ai_engine.py          # Azure OpenAI integration
│   ├── ai_worker.py          # Background AI processing
│   └── __init__.py
├── ui/
│   ├── main_window.py        # Main application window
│   ├── genre_select.py       # Genre selection screen
│   ├── word_input.py         # Word input interface
│   ├── loading_screen.py     # Loading animation
│   ├── story_reveal.py       # Story display and animation
│   ├── stats_screen.py       # Statistics viewer
│   ├── background.py         # UI background effects
│   ├── theme.py              # Theme and styling
│   └── __init__.py
└── sounds/                    # Audio files
    ├── *.wav files           # Genre themes, effects, UI sounds
```

---

## 🎨 Genres Available

- **Fantasy**: Epic quests, dragons, and magical adventures
- **Science Fiction**: Space exploration, futuristic tech, alien encounters
- **Horror**: Suspenseful and spine-tingling narratives
- **Romance**: Love stories with dramatic twists
- **Academic**: Scholarly mishaps and intellectual chaos
- **Existential**: Philosophical musings and reality-bending tales
- **Fourth Wall**: Meta-narrative experiences

Each genre features:
- Unique color schemes and visual themes
- Genre-appropriate background music
- Specialized sentence templates
- Contextual word prompts

---

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | ≥6.4.0 | GUI framework |
| PyQt6-Qt6 | ≥6.4.0 | Qt runtime |
| azure-openai | Latest | AI story generation |

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🎬 How It Works

### Story Generation Pipeline

1. **User Input**: Collect words based on genre-specific prompts
2. **AI Processing**: Send word data to Azure OpenAI for story generation
3. **Story Assembly**: Engine randomizes templates and injects humor techniques
4. **Visual Rendering**: Display story with animations and visual emphasis
5. **Audio Playback**: Play complementary sound effects and background music

### Humor Amplification Techniques

- **Callbacks**: Words reappear at unexpected moments for comedic effect
- **Escalation**: Story intensity gradually increases for dramatic payoff
- **Fourth-Wall Breaks**: Meta-commentary that acknowledges the game itself
- **Mismatches**: Unexpected word combinations create absurdist humor

---

## 📊 Statistics

MadVerse tracks:
- Total stories generated
- Most-used words
- Average words per story
- Genre popularity
- Playtime statistics

View stats in-game from the Statistics screen.

---

## 🎵 Audio Features

Immersive soundscapes for each genre:
- Thematic background music during gameplay
- Interactive sound effects for user actions
- Story reveal audio cues
- Ambient effects for atmosphere

All audio files are included in the `sounds/` directory.

---

## ⚙️ Configuration

### Adjusting Difficulty
Modify `keys.py` and `engine/ai_engine.py` to adjust:
- AI model used
- Response creativity level
- Story length parameters

### Customizing Themes
Edit `data/genres.py` to:
- Add new genres
- Modify color schemes
- Change sentence templates
- Add custom word prompts

---

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Ensure all dependencies are installed
pip install --upgrade -r requirements.txt

# Verify Python version
python --version  # Should be 3.8+
```

### API Connection Issues
- Verify `keys.py` contains valid Azure credentials
- Check internet connectivity
- Ensure API keys have sufficient quota

### Sound Playback Problems
- Verify audio files exist in `sounds/` directory
- Check system volume settings
- Ensure PyQt6-Multimedia is properly installed

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Kamruzzaman Kamrul**

- GitHub: [@kamrul28890](https://github.com/kamrul28890)
- Project: [MadVerse](https://github.com/kamrul28890/madverse)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new genres
- Improve story templates
- Enhance UI/UX

---

## 📞 Support

For issues, feature requests, or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/kamrul28890/madverse/issues)
3. Create a new issue with detailed information

---

## 🎯 Roadmap

- [ ] Multiplayer story battles
- [ ] Custom genre builder
- [ ] Mobile app version
- [ ] Story sharing and leaderboards
- [ ] Advanced AI customization options
- [ ] Offline story mode with pre-written templates

---

## ✅ Quick Checklist

Before first run:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `keys.py` configured with API credentials
- [ ] Sound files present in `sounds/` directory

---

**Enjoy generating chaotic, hilarious stories! 🎭✨**
