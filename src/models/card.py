"""Card model representing a word card on the game board."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CardColor(Enum):
    """Represents the possible colors/types of cards in the game."""
    RED = "red"
    BLUE = "blue"
    NEUTRAL = "neutral"
    FAILURE = "failure"


@dataclass
class Card:
    """Represents a single word card on the game board.
    
    Args:
        word: The word displayed on the card
        color: The card's team assignment or type
        revealed: Whether the card has been selected/revealed
        position: Optional grid position (row, col) for board placement
    """
    word: str
    color: CardColor
    revealed: bool = False
    position: Optional[tuple[int, int]] = None
    
    def reveal(self) -> CardColor:
        """Mark the card as revealed and return its color.
        
        Returns:
            The card's color after revealing
        """
        self.revealed = True
        return self.color
    
    def is_team_card(self, team_color: CardColor) -> bool:
        """Check if this card belongs to the specified team.
        
        Args:
            team_color: Color of the team to check against
            
        Returns:
            True if card belongs to the team
        """
        return self.color == team_color
    
    def is_safe_to_reveal(self) -> bool:
        """Check if revealing this card won't end the game in failure.
        
        Returns:
            True if card is not a failure card
        """
        return self.color != CardColor.FAILURE
