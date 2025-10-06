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
    
    Attributes:
        name: The player's display name
        role: Whether the player is a Chief or Detective
    """
    name: str
    role: PlayerRole
    
    def is_chief(self) -> bool:
        """Check if this player is a Chief."""
        return self.role == PlayerRole.CHIEF
    
    def is_detective(self) -> bool:
        """Check if this player is a Detective."""
        return self.role == PlayerRole.DETECTIVE
    
    def can_give_clues(self) -> bool:
        """Check if this player can give clues to their team."""
        return self.is_chief()
    
    def can_make_guesses(self) -> bool:
        """Check if this player can make guesses."""
        return self.is_detective()
