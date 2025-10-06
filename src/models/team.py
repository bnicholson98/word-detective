"""Team model representing game teams."""

from dataclasses import dataclass, field
from typing import List
from .card import CardColor
from .player import Player, PlayerRole


@dataclass
class Team:
    """Represents a team in the game.
    
    Args:
        color: The team's color (RED or BLUE)
        players: List of players on this team
        words_remaining: Number of team words still to be found
        total_words: Total number of words assigned to this team
    """
    color: CardColor
    players: List[Player] = field(default_factory=list)
    words_remaining: int = 0
    total_words: int = 0
    
    def __post_init__(self):
        """Validate team color is RED or BLUE.
        
        Raises:
            ValueError: If color is not RED or BLUE
        """
        if self.color not in [CardColor.RED, CardColor.BLUE]:
            raise ValueError("Team color must be RED or BLUE")
    
    def add_player(self, player: Player) -> None:
        """Add a player to this team.
        
        Args:
            player: Player to add to the team
        """
        self.players.append(player)
    
    def get_chief(self) -> Player:
        """Get the Chief player from this team.
        
        Returns:
            The Chief player
            
        Raises:
            ValueError: If no Chief found on team
        """
        for player in self.players:
            if player.is_chief():
                return player
        raise ValueError("No Chief found on this team")
    
    def get_detectives(self) -> List[Player]:
        """Get all Detective players from this team.
        
        Returns:
            List of Detective players
        """
        return [player for player in self.players if player.is_detective()]
    
    def has_chief(self) -> bool:
        """Check if this team has a Chief.
        
        Returns:
            True if team has a Chief player
        """
        return any(player.is_chief() for player in self.players)
    
    def has_detectives(self) -> bool:
        """Check if this team has any Detectives.
        
        Returns:
            True if team has Detective players
        """
        return any(player.is_detective() for player in self.players)
    
    def is_complete_team(self) -> bool:
        """Check if team has both a Chief and at least one Detective.
        
        Returns:
            True if team is complete
        """
        return self.has_chief() and self.has_detectives()
    
    def word_found(self) -> None:
        """Mark that one of this team's words has been found."""
        if self.words_remaining > 0:
            self.words_remaining -= 1
    
    def has_won(self) -> bool:
        """Check if this team has found all their words.
        
        Returns:
            True if team has won
        """
        return self.words_remaining == 0
    
    def set_word_count(self, total_words: int) -> None:
        """Set the total number of words for this team.
        
        Args:
            total_words: Total number of words assigned to team
        """
        self.total_words = total_words
        self.words_remaining = total_words
