"""Player model representing game participants."""

from dataclasses import dataclass
from enum import Enum


class PlayerRole(Enum):
    """Represents the possible roles a player can have."""
    CHIEF = "chief"
    DETECTIVE = "detective"


@dataclass
class Player:
    """Represents a player in the game.
    
    Args:
        name: The player's display name
        role: Whether the player is a Chief or Detective
    """
    name: str
    role: PlayerRole
    
    def is_chief(self) -> bool:
        """Check if this player is a Chief.
        
        Returns:
            True if player role is CHIEF
        """
        return self.role == PlayerRole.CHIEF
    
    def is_detective(self) -> bool:
        """Check if this player is a Detective.
        
        Returns:
            True if player role is DETECTIVE
        """
        return self.role == PlayerRole.DETECTIVE
    
    def can_give_clues(self) -> bool:
        """Check if this player can give clues to their team.
        
        Returns:
            True if player can give clues
        """
        return self.is_chief()
    
    def can_make_guesses(self) -> bool:
        """Check if this player can make guesses.
        
        Returns:
            True if player can make guesses
        """
        return self.is_detective()
