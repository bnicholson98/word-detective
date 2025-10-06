"""Clue model representing Chief's clues to their team."""

from dataclasses import dataclass
from .card import CardColor


@dataclass
class Clue:
    """Represents a clue given by a Chief to their Detective(s).
    
    Args:
        word: The one-word clue
        number: How many words the clue relates to
        team_color: Which team gave this clue
        guesses_remaining: How many guesses the team has left for this clue
    """
    word: str
    number: int
    team_color: CardColor
    guesses_remaining: int = 0
    
    def __post_init__(self):
        """Initialize guesses remaining based on clue number.
        
        Raises:
            ValueError: If number is less than 1, word is empty, or team color invalid
        """
        if self.guesses_remaining == 0:
            self.guesses_remaining = self.number + 1
        
        if self.number < 1:
            raise ValueError("Clue number must be at least 1")
        
        if not self.word or not self.word.strip():
            raise ValueError("Clue word cannot be empty")
        
        if self.team_color not in [CardColor.RED, CardColor.BLUE]:
            raise ValueError("Clue team color must be RED or BLUE")
    
    def use_guess(self) -> int:
        """Use one guess and return remaining guesses.
        
        Returns:
            Number of guesses remaining
        """
        if self.guesses_remaining > 0:
            self.guesses_remaining -= 1
        return self.guesses_remaining
    
    def has_guesses_left(self) -> bool:
        """Check if there are guesses remaining for this clue.
        
        Returns:
            True if guesses remain
        """
        return self.guesses_remaining > 0
    
    def max_guesses_allowed(self) -> int:
        """Get the maximum number of guesses allowed for this clue.
        
        Returns:
            Maximum guesses allowed (number + 1)
        """
        return self.number + 1
    
    def is_valid_word(self) -> bool:
        """Check if the clue word meets basic validity requirements.
        
        Returns:
            True if word is valid format
        """
        if not self.word or not self.word.strip():
            return False
        
        cleaned_word = self.word.strip()
        
        if len(cleaned_word) < 2:
            return False
        
        if not all(c.isalpha() or c in ['-', "'"] for c in cleaned_word):
            return False
        
        return True
