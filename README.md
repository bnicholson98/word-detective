# Word Detective Terminal Game

A terminal-based implementation of the classic word-guessing team game, featuring rich console interface and engaging gameplay mechanics.

## 🎯 Game Overview

Word Detective is a strategic word-guessing game where two teams compete to identify their secret words on a shared game board. Teams consist of a **Chief** (who gives clues) and **Detectives** (who make guesses).

## 🎮 Game Rules

### Setup
- **Game Board**: 5×5 grid containing 25 randomly selected word cards
- **Teams**: Red Team and Blue Team
- **Roles**: Each team has one Chief and one or more Detectives
- **Word Distribution**: 
  - Starting team: 9 target words
  - Second team: 8 target words
  - Neutral words: 7 words
  - Failure word: 1 word (instant loss if selected)

### Gameplay Flow

#### Chief's Turn
1. **Give Clue**: Provide a one-word clue and a number
   - The clue must relate to one or more of your team's words
   - Cannot use any word currently on the board
   - Cannot use rhyming words
   - Number indicates how many words the clue relates to
   - Example: "Ocean, 2" (hints at two ocean-related words)

#### Detective's Turn
1. **Make Guesses**: Select words from the board one by one
2. **Guess Limit**: Can make up to (clue number + 1) guesses
3. **Immediate Feedback**: Chief reveals each word's color after selection
4. **Turn Ends When**:
   - Maximum guesses reached
   - Neutral word selected
   - Opposing team's word selected
   - Failure word selected (immediate game loss)

### Winning Conditions
- **Victory**: First team to identify all their target words
- **Defeat**: Team that selects the failure word loses immediately

## 🛠️ Technical Features

### Built With
- **Python 3.8+**: Core game logic and data structures
- **Rich Library**: Beautiful terminal interface with colors and formatting
- **Dataclasses**: Clean, type-safe data modeling
- **Pytest**: Comprehensive unit testing suite

### Key Components
- **Game Engine**: Core logic for game state management and rule enforcement
- **Terminal Interface**: Rich console display with interactive word selection
- **Word Management**: Dynamic loading from word list with validation
- **Team System**: Role-based gameplay with turn management
- **Save/Load**: Game session persistence and recovery

## 🚀 Installation & Usage

### Prerequisites
```bash
pip install rich pytest
```

### Running the Game
```bash
python -m src.main
```

### Running Tests
```bash
pytest tests/ -v
```

## 📁 Project Structure

```
WordDetective/
├── src/                    # Main source code
│   ├── __init__.py
│   ├── main.py            # Game entry point
│   ├── models/            # Data models and structures
│   ├── game/              # Core game logic
│   ├── interface/         # Terminal UI components
│   └── utils/             # Utility functions
├── tests/                 # Unit tests
├── word_list.txt          # Game vocabulary
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Interface Features

- **Color-coded Teams**: Visual distinction between Red and Blue team words
- **Interactive Board**: Click-to-select word interface
- **Real-time Status**: Current team, remaining words, and game progress
- **Rich Formatting**: Beautiful terminal output with proper spacing and colors
- **Input Validation**: Comprehensive error checking and user guidance

## 🧪 Testing

Comprehensive test suite covering:
- Game logic and rule enforcement
- Word loading and board generation
- Team management and turn handling
- Win/lose condition validation
- Interface components and user interactions

## 📝 Development Notes

- Uses Python dataclasses for clean, type-safe data modeling
- Rich library provides cross-platform terminal enhancements
- Modular design allows easy extension and modification
- Full test coverage ensures reliable gameplay experience

## 🤝 Contributing

1. Follow existing code structure and naming conventions
2. Add unit tests for all new functionality
3. Use dataclasses for data modeling
4. Leverage Rich library for terminal interface enhancements
5. Clean __pycache__ folders before commits

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.