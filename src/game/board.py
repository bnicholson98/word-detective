"""Game board management and generation."""

import random
from typing import List, Tuple
from dataclasses import dataclass
from ..models.card import Card, CardColor
from ..utils.word_loader import WordLoader


@dataclass
class BoardConfiguration:
    """Configuration for board generation.
    
    Args:
        starting_team_words: Number of words for starting team
        second_team_words: Number of words for second team  
        neutral_words: Number of neutral words
        failure_words: Number of failure words
    """
    starting_team_words: int = 9
    second_team_words: int = 8
    neutral_words: int = 7
    failure_words: int = 1


class GameBoard:
    """Manages the 5x5 game board with word cards."""
    
    def __init__(self, word_loader: WordLoader = None):
        """Initialize game board.
        
        Args:
            word_loader: Word loader instance for getting words
        """
        self.word_loader = word_loader or WordLoader()
        self.board: List[List[Card]] = [[None for _ in range(5)] for _ in range(5)]
        self.cards: List[Card] = []
        self._key_card: List[CardColor] = []
    
    def generate_board(self, starting_team: CardColor) -> None:
        """Generate a new game board with random words and assignments.
        
        Args:
            starting_team: Which team goes first (gets 9 words)
            
        Raises:
            ValueError: If starting team is not RED or BLUE
        """
        if starting_team not in [CardColor.RED, CardColor.BLUE]:
            raise ValueError("Starting team must be RED or BLUE")
        
        words = self.word_loader.get_game_words()
        config = BoardConfiguration()
        
        second_team = CardColor.BLUE if starting_team == CardColor.RED else CardColor.RED
        
        color_assignments = []
        color_assignments.extend([starting_team] * config.starting_team_words)
        color_assignments.extend([second_team] * config.second_team_words)
        color_assignments.extend([CardColor.NEUTRAL] * config.neutral_words)
        color_assignments.extend([CardColor.FAILURE] * config.failure_words)
        
        random.shuffle(color_assignments)
        
        self.cards = []
        self._key_card = color_assignments.copy()
        
        for i, (word, color) in enumerate(zip(words, color_assignments)):
            row, col = divmod(i, 5)
            card = Card(word=word, color=color, position=(row, col))
            self.cards.append(card)
            self.board[row][col] = card
    
    def get_card(self, row: int, col: int) -> Card:
        """Get card at board position.
        
        Args:
            row: Row index (0-4)
            col: Column index (0-4)
            
        Returns:
            Card at position
            
        Raises:
            ValueError: If position is out of bounds
        """
        if not (0 <= row < 5 and 0 <= col < 5):
            raise ValueError("Position must be within board bounds (0-4)")
        return self.board[row][col]
    
    def get_card_by_word(self, word: str) -> Card:
        """Get card by its word.
        
        Args:
            word: Word to search for
            
        Returns:
            Card with the word
            
        Raises:
            ValueError: If word not found on board
        """
        for card in self.cards:
            if card.word.lower() == word.lower():
                return card
        raise ValueError(f"Word '{word}' not found on board")
    
    def reveal_card(self, row: int, col: int) -> CardColor:
        """Reveal a card and return its color.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Color of revealed card
        """
        card = self.get_card(row, col)
        return card.reveal()
    
    def reveal_card_by_word(self, word: str) -> CardColor:
        """Reveal a card by its word.
        
        Args:
            word: Word on card to reveal
            
        Returns:
            Color of revealed card
        """
        card = self.get_card_by_word(word)
        return card.reveal()
    
    def get_all_words(self) -> List[str]:
        """Get all words on the board.
        
        Returns:
            List of all words
        """
        return [card.word for card in self.cards]
    
    def get_unrevealed_words(self) -> List[str]:
        """Get all unrevealed words.
        
        Returns:
            List of unrevealed words
        """
        return [card.word for card in self.cards if not card.revealed]
    
    def get_team_words(self, color: CardColor) -> List[str]:
        """Get all words belonging to a team.
        
        Args:
            color: Team color
            
        Returns:
            List of team's words
        """
        return [card.word for card in self.cards if card.color == color]
    
    def get_unrevealed_team_words(self, color: CardColor) -> List[str]:
        """Get unrevealed words for a team.
        
        Args:
            color: Team color
            
        Returns:
            List of unrevealed team words
        """
        return [card.word for card in self.cards 
                if card.color == color and not card.revealed]
    
    def count_team_words_remaining(self, color: CardColor) -> int:
        """Count remaining words for a team.
        
        Args:
            color: Team color
            
        Returns:
            Number of unrevealed team words
        """
        return len(self.get_unrevealed_team_words(color))
    
    def is_word_revealed(self, word: str) -> bool:
        """Check if a word has been revealed.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is revealed
        """
        try:
            card = self.get_card_by_word(word)
            return card.revealed
        except ValueError:
            return False
    
    def get_key_card(self) -> List[CardColor]:
        """Get the key card showing all color assignments.
        
        Returns:
            List of colors in board order
        """
        return self._key_card.copy()
    
    def is_board_complete(self) -> bool:
        """Check if board has been generated.
        
        Returns:
            True if board is ready
        """
        return len(self.cards) == 25 and all(card is not None for row in self.board for card in row)
