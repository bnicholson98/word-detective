"""Test that all modules can be imported correctly."""

import pytest


class TestImports:
    """Test cases for module imports."""
    
    def test_model_imports(self):
        """Test that all model classes can be imported."""
        from src.models.card import Card, CardColor
        from src.models.player import Player, PlayerRole
        from src.models.team import Team
        from src.models.clue import Clue
        from src.models.game_state import GameState, GamePhase, TurnType
        
        assert Card is not None
        assert CardColor is not None
        assert Player is not None
        assert PlayerRole is not None
        assert Team is not None
        assert Clue is not None
        assert GameState is not None
        assert GamePhase is not None
        assert TurnType is not None
    
    def test_utility_imports(self):
        """Test that all utility classes can be imported."""
        from src.utils.word_loader import WordLoader
        from src.utils.word_validator import WordValidator
        
        assert WordLoader is not None
        assert WordValidator is not None
    
    def test_package_imports(self):
        """Test that packages can be imported."""
        import src
        import src.models
        import src.utils
        
        assert src is not None
        assert src.models is not None
        assert src.utils is not None
    
    def test_full_integration(self):
        """Test that classes can be instantiated together."""
        from src.models.card import Card, CardColor
        from src.models.player import Player, PlayerRole
        from src.models.team import Team
        from src.models.clue import Clue
        from src.models.game_state import GameState
        from src.utils.word_loader import WordLoader
        from src.utils.word_validator import WordValidator
        
        card = Card(word="TEST", color=CardColor.RED)
        player = Player(name="TestPlayer", role=PlayerRole.CHIEF)
        team = Team(color=CardColor.BLUE)
        clue = Clue(word="HINT", number=2, team_color=CardColor.RED)
        game_state = GameState()
        loader = WordLoader("word_list.txt")
        validator = WordValidator()
        
        assert card.word == "TEST"
        assert player.name == "TestPlayer"
        assert team.color == CardColor.BLUE
        assert clue.word == "HINT"
        assert game_state.phase.value == "setup"
        assert loader is not None
        assert validator is not None
