"""Tests for the Clue model."""

import pytest
from src.models.clue import Clue
from src.models.card import CardColor


class TestClue:
    """Test cases for Clue dataclass."""
    
    def test_clue_creation_valid(self):
        """Test valid clue creation."""
        clue = Clue(word="OCEAN", number=2, team_color=CardColor.RED)
        
        assert clue.word == "OCEAN"
        assert clue.number == 2
        assert clue.team_color == CardColor.RED
        assert clue.guesses_remaining == 3
    
    def test_clue_creation_with_custom_guesses(self):
        """Test clue creation with custom guesses remaining."""
        clue = Clue(word="ANIMAL", number=3, team_color=CardColor.BLUE, guesses_remaining=5)
        
        assert clue.guesses_remaining == 5
        assert clue.max_guesses_allowed() == 4
    
    def test_clue_invalid_number(self):
        """Test clue creation with invalid number raises error."""
        with pytest.raises(ValueError, match="Clue number must be at least 1"):
            Clue(word="TEST", number=0, team_color=CardColor.RED)
        
        with pytest.raises(ValueError, match="Clue number must be at least 1"):
            Clue(word="TEST", number=-1, team_color=CardColor.BLUE)
    
    def test_clue_invalid_word(self):
        """Test clue creation with invalid word raises error."""
        with pytest.raises(ValueError, match="Clue word cannot be empty"):
            Clue(word="", number=1, team_color=CardColor.RED)
        
        with pytest.raises(ValueError, match="Clue word cannot be empty"):
            Clue(word="   ", number=1, team_color=CardColor.BLUE)
    
    def test_clue_invalid_team_color(self):
        """Test clue creation with invalid team color raises error."""
        with pytest.raises(ValueError, match="Clue team color must be RED or BLUE"):
            Clue(word="TEST", number=1, team_color=CardColor.NEUTRAL)
        
        with pytest.raises(ValueError, match="Clue team color must be RED or BLUE"):
            Clue(word="TEST", number=1, team_color=CardColor.FAILURE)
    
    def test_use_guess(self):
        """Test using guesses."""
        clue = Clue(word="SPACE", number=2, team_color=CardColor.RED)
        
        assert clue.guesses_remaining == 3
        
        remaining = clue.use_guess()
        assert remaining == 2
        assert clue.guesses_remaining == 2
        
        remaining = clue.use_guess()
        assert remaining == 1
        
        remaining = clue.use_guess()
        assert remaining == 0
        
        remaining = clue.use_guess()
        assert remaining == 0
    
    def test_has_guesses_left(self):
        """Test checking for remaining guesses."""
        clue = Clue(word="FOOD", number=1, team_color=CardColor.BLUE)
        
        assert clue.has_guesses_left() is True
        
        clue.use_guess()
        assert clue.has_guesses_left() is True
        
        clue.use_guess()
        assert clue.has_guesses_left() is False
        
        clue.use_guess()
        assert clue.has_guesses_left() is False
    
    def test_max_guesses_allowed(self):
        """Test maximum guesses calculation."""
        clue1 = Clue(word="ONE", number=1, team_color=CardColor.RED)
        clue2 = Clue(word="THREE", number=3, team_color=CardColor.BLUE)
        clue5 = Clue(word="FIVE", number=5, team_color=CardColor.RED)
        
        assert clue1.max_guesses_allowed() == 2
        assert clue2.max_guesses_allowed() == 4
        assert clue5.max_guesses_allowed() == 6
    
    def test_is_valid_word(self):
        """Test word validity checking."""
        valid_clue = Clue(word="NATURE", number=2, team_color=CardColor.RED)
        assert valid_clue.is_valid_word() is True
        
        single_char_clue = Clue(word="A", number=1, team_color=CardColor.BLUE)
        assert single_char_clue.is_valid_word() is False
        
        with_hyphen = Clue(word="CO-OP", number=1, team_color=CardColor.RED)
        assert with_hyphen.is_valid_word() is True
    
    def test_post_init_guesses_calculation(self):
        """Test that post_init correctly calculates guesses_remaining."""
        clue = Clue(word="CALCULATE", number=4, team_color=CardColor.BLUE)
        assert clue.guesses_remaining == 5
        
        clue_with_explicit = Clue(word="EXPLICIT", number=2, team_color=CardColor.RED, guesses_remaining=10)
        assert clue_with_explicit.guesses_remaining == 10
