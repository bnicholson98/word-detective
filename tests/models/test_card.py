"""Tests for the Card model."""

import pytest
from src.models.card import Card, CardColor


class TestCard:
    """Test cases for Card dataclass."""
    
    def test_card_creation(self):
        """Test basic card creation."""
        card = Card(word="TEST", color=CardColor.RED)
        assert card.word == "TEST"
        assert card.color == CardColor.RED
        assert card.revealed is False
        assert card.position is None
    
    def test_card_with_position(self):
        """Test card creation with position."""
        card = Card(word="GAME", color=CardColor.BLUE, position=(2, 3))
        assert card.word == "GAME"
        assert card.color == CardColor.BLUE
        assert card.position == (2, 3)
        assert card.revealed is False
    
    def test_card_reveal(self):
        """Test card reveal functionality."""
        card = Card(word="SECRET", color=CardColor.FAILURE)
        assert card.revealed is False
        
        revealed_color = card.reveal()
        assert card.revealed is True
        assert revealed_color == CardColor.FAILURE
    
    def test_is_team_card(self):
        """Test team card identification."""
        red_card = Card(word="RED", color=CardColor.RED)
        blue_card = Card(word="BLUE", color=CardColor.BLUE)
        neutral_card = Card(word="NEUTRAL", color=CardColor.NEUTRAL)
        
        assert red_card.is_team_card(CardColor.RED) is True
        assert red_card.is_team_card(CardColor.BLUE) is False
        
        assert blue_card.is_team_card(CardColor.BLUE) is True
        assert blue_card.is_team_card(CardColor.RED) is False
        
        assert neutral_card.is_team_card(CardColor.RED) is False
        assert neutral_card.is_team_card(CardColor.BLUE) is False
    
    def test_is_safe_to_reveal(self):
        """Test safety check for card revelation."""
        red_card = Card(word="SAFE", color=CardColor.RED)
        blue_card = Card(word="ALSO_SAFE", color=CardColor.BLUE)
        neutral_card = Card(word="NEUTRAL", color=CardColor.NEUTRAL)
        failure_card = Card(word="DANGER", color=CardColor.FAILURE)
        
        assert red_card.is_safe_to_reveal() is True
        assert blue_card.is_safe_to_reveal() is True
        assert neutral_card.is_safe_to_reveal() is True
        assert failure_card.is_safe_to_reveal() is False
    
    def test_card_color_enum(self):
        """Test CardColor enum values."""
        assert CardColor.RED.value == "red"
        assert CardColor.BLUE.value == "blue"
        assert CardColor.NEUTRAL.value == "neutral"
        assert CardColor.FAILURE.value == "failure"
    
    def test_card_equality(self):
        """Test card equality comparison."""
        card1 = Card(word="SAME", color=CardColor.RED, revealed=False)
        card2 = Card(word="SAME", color=CardColor.RED, revealed=False)
        card3 = Card(word="DIFFERENT", color=CardColor.RED, revealed=False)
        
        assert card1 == card2
        assert card1 != card3
