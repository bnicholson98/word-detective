"""Word loading utilities for the game."""

import random
from pathlib import Path
from typing import List, Set


class WordLoader:
    """Handles loading and managing words from the word list file."""
    
    def __init__(self, word_file_path: str = "word_list.txt"):
        """Initialize with path to word list file.
        
        Args:
            word_file_path: Path to the word list file
        """
        self.word_file_path = Path(word_file_path)
        self._word_cache: List[str] = []
    
    def load_words(self) -> List[str]:
        """Load words from the word list file.
        
        Returns:
            List of valid words from file
            
        Raises:
            FileNotFoundError: If word file doesn't exist
            ValueError: If insufficient valid words found
            IOError: If file cannot be read
        """
        if not self.word_file_path.exists():
            raise FileNotFoundError(f"Word list file not found: {self.word_file_path}")
        
        try:
            with open(self.word_file_path, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
                
            if len(words) < 25:
                raise ValueError(f"Word list must contain at least 25 words, found {len(words)}")
            
            self._word_cache = [word for word in words if self._is_valid_word(word)]
            
            if len(self._word_cache) < 25:
                raise ValueError(f"Not enough valid words in file, need at least 25, found {len(self._word_cache)}")
            
            return self._word_cache.copy()
            
        except IOError as e:
            raise IOError(f"Error reading word list file: {e}")
    
    def get_random_words(self, count: int) -> List[str]:
        """Get a random selection of words from the loaded word list.
        
        Args:
            count: Number of words to select
            
        Returns:
            List of randomly selected words
            
        Raises:
            ValueError: If count exceeds available words
        """
        if not self._word_cache:
            self.load_words()
        
        if count > len(self._word_cache):
            raise ValueError(f"Cannot select {count} words, only {len(self._word_cache)} available")
        
        return random.sample(self._word_cache, count)
    
    def get_game_words(self) -> List[str]:
        """Get exactly 25 random words for a game board.
        
        Returns:
            List of 25 random words
        """
        return self.get_random_words(25)
    
    def word_exists(self, word: str) -> bool:
        """Check if a word exists in the loaded word list.
        
        Args:
            word: Word to check for existence
            
        Returns:
            True if word exists in list
        """
        if not self._word_cache:
            self.load_words()
        return word.lower() in [w.lower() for w in self._word_cache]
    
    def get_word_count(self) -> int:
        """Get the total number of loaded words.
        
        Returns:
            Number of valid words loaded
        """
        if not self._word_cache:
            self.load_words()
        return len(self._word_cache)
    
    @staticmethod
    def _is_valid_word(word: str) -> bool:
        """Check if a word meets validity requirements.
        
        Args:
            word: Word to validate
            
        Returns:
            True if word meets requirements
        """
        if not word or not word.strip():
            return False
        
        cleaned_word = word.strip()
        
        if len(cleaned_word) < 2:
            return False
        
        if cleaned_word.isdigit():
            return False
        
        if not all(c.isalpha() or c in ['-', "'"] for c in cleaned_word):
            return False
        
        return True
    
    def validate_word_list_file(self) -> dict:
        """Validate the word list file and return statistics.
        
        Returns:
            Dict with validation results and statistics
        """
        if not self.word_file_path.exists():
            return {
                "valid": False,
                "error": f"File not found: {self.word_file_path}",
                "word_count": 0,
                "valid_words": 0
            }
        
        try:
            with open(self.word_file_path, 'r', encoding='utf-8') as file:
                all_lines = [line.strip() for line in file]
                
            valid_words = [word for word in all_lines if self._is_valid_word(word)]
            
            return {
                "valid": len(valid_words) >= 25,
                "word_count": len(all_lines),
                "valid_words": len(valid_words),
                "min_required": 25,
                "error": None if len(valid_words) >= 25 else "Not enough valid words"
            }
            
        except IOError as e:
            return {
                "valid": False,
                "error": f"Cannot read file: {e}",
                "word_count": 0,
                "valid_words": 0
            }
