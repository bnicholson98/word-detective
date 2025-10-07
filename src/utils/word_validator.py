"""Word validation utilities for clues and game words."""

import re
from typing import List, Set


class WordValidator:
    """Handles validation of clues and words according to game rules."""
    
    def __init__(self):
        """Initialize the word validator."""
        self._simple_rhyme_patterns = self._build_rhyme_patterns()
    
    def is_valid_clue_word(self, clue: str, board_words: List[str]) -> tuple[bool, str]:
        """Validate a clue word according to game rules.
        
        Args:
            clue: The clue word to validate
            board_words: List of words currently on the board
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not clue or not clue.strip():
            return False, "Clue cannot be empty"
        
        cleaned_clue = clue.strip().lower()
        
        if not cleaned_clue.replace('-', '').replace("'", '').isalpha():
            return False, "Clue must contain only letters, hyphens, or apostrophes"
        
        if len(cleaned_clue) < 2:
            return False, "Clue must be at least 2 characters long"
        
        board_words_lower = [word.lower() for word in board_words]
        
        if cleaned_clue in board_words_lower:
            return False, "Clue cannot be a word that appears on the board"
        
        if self._contains_board_word(cleaned_clue, board_words_lower):
            return False, "Clue cannot contain a word that appears on the board"
        
        if self._is_rhyming_word(cleaned_clue, board_words_lower):
            return False, "Clue cannot rhyme with words on the board"
        
        return True, ""
    
    def is_valid_game_word(self, word: str) -> bool:
        """Check if a word is valid for use on the game board.
        
        Args:
            word: Word to validate
            
        Returns:
            True if word is valid for game board
        """
        if not word or not word.strip():
            return False
        
        cleaned_word = word.strip()
        
        if len(cleaned_word) < 2:
            return False
        
        if not all(c.isalpha() or c in ['-', "'"] for c in cleaned_word):
            return False
        
        return True
    
    def normalize_word(self, word: str) -> str:
        """Normalize a word for comparison purposes.
        
        Args:
            word: Word to normalize
            
        Returns:
            Normalized word (lowercase, trimmed)
        """
        return word.strip().lower()
    
    def _contains_board_word(self, clue: str, board_words: List[str]) -> bool:
        """Check if clue contains any board words as substrings.
        
        Args:
            clue: Clue word to check
            board_words: List of board words
            
        Returns:
            True if clue contains any board word
        """
        for board_word in board_words:
            if len(board_word) >= 3:
                if board_word in clue or clue in board_word:
                    return True
        return False
    
    def _is_rhyming_word(self, clue: str, board_words: List[str]) -> bool:
        """Check if clue rhymes with any board words using simple patterns.
        
        Args:
            clue: Clue word to check
            board_words: List of board words
            
        Returns:
            True if clue rhymes with any board word
        """
        for board_word in board_words:
            if self._words_rhyme(clue, board_word):
                return True
        return False
    
    def _words_rhyme(self, word1: str, word2: str) -> bool:
        """Simple rhyme detection based on common ending patterns.
        
        Args:
            word1: First word to compare
            word2: Second word to compare
            
        Returns:
            True if words rhyme
        """
        if len(word1) < 3 or len(word2) < 3:
            return False
        
        if word1 == word2:
            return True
        
        if word1[-3:] == word2[-3:] and len(word1) >= 4 and len(word2) >= 4:
            return True
        
        return False
    
    def _build_rhyme_patterns(self) -> Set[str]:
        """Build a set of common rhyming patterns.
        
        Returns:
            Set of common word ending patterns
        """
        return {
            'ing', 'tion', 'sion', 'ness', 'ment', 'able', 'ible',
            'ful', 'less', 'ous', 'ious', 'eous', 'ary', 'ery', 'ory',
            'ate', 'ite', 'ute', 'ent', 'ant', 'est', 'er', 'ed',
            'ly', 'ty', 'cy', 'sy', 'py', 'ky', 'dy', 'by', 'ry',
            'al', 'el', 'il', 'ol', 'ul', 'ar', 'or', 'ur', 'ir',
            'an', 'en', 'in', 'on', 'un', 'ck', 'nk', 'ng', 'nd',
            'st', 'nt', 'pt', 'ct', 'ft', 'lt', 'rt', 'xt'
        }
    
    def get_validation_rules(self) -> List[str]:
        """Get a list of validation rules for display to users.
        
        Returns:
            List of validation rule descriptions
        """
        return [
            "Clue must be a single word (letters, hyphens, apostrophes only)",
            "Clue must be at least 2 characters long",
            "Clue cannot be a word that appears on the board",
            "Clue cannot contain any board words",
            "Clue cannot rhyme with board words",
            "Clue must relate to your team's words"
        ]
