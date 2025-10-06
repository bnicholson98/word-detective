"""Tests for the Player model."""

import pytest
from src.models.player import Player, PlayerRole


class TestPlayer:
    """Test cases for Player dataclass."""
    
    def test_player_creation(self):
        """Test basic player creation."""
        player = Player(name="Alice", role=PlayerRole.CHIEF)
        assert player.name == "Alice"
        assert player.role == PlayerRole.CHIEF
    
    def test_chief_player_methods(self):
        """Test methods for Chief players."""
        chief = Player(name="Chief Alice", role=PlayerRole.CHIEF)
        
        assert chief.is_chief() is True
        assert chief.is_detective() is False
        assert chief.can_give_clues() is True
        assert chief.can_make_guesses() is False
    
    def test_detective_player_methods(self):
        """Test methods for Detective players."""
        detective = Player(name="Detective Bob", role=PlayerRole.DETECTIVE)
        
        assert detective.is_chief() is False
        assert detective.is_detective() is True
        assert detective.can_give_clues() is False
        assert detective.can_make_guesses() is True
    
    def test_player_role_enum(self):
        """Test PlayerRole enum values."""
        assert PlayerRole.CHIEF.value == "chief"
        assert PlayerRole.DETECTIVE.value == "detective"
    
    def test_player_equality(self):
        """Test player equality comparison."""
        player1 = Player(name="Same", role=PlayerRole.CHIEF)
        player2 = Player(name="Same", role=PlayerRole.CHIEF)
        player3 = Player(name="Different", role=PlayerRole.CHIEF)
        player4 = Player(name="Same", role=PlayerRole.DETECTIVE)
        
        assert player1 == player2
        assert player1 != player3
        assert player1 != player4
