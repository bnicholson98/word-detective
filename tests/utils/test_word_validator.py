"""Tests for the WordValidator utility."""

import pytest
from src.utils.word_validator import WordValidator


class TestWordValidator:
    """Test cases for WordValidator utility."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = WordValidator()
        self.board_words = ["APPLE", "BANANA", "CHERRY", "DOG", "ELEPHANT", "FIRE", "GUITAR"]
    
    def test_validator_initialization(self):
        """Test WordValidator initialization."""
        validator = WordValidator()
        assert validator._simple_rhyme_patterns is not None
        assert len(validator._simple_rhyme_patterns) > 0
    
    def test_is_valid_clue_word_valid_cases(self):
        """Test valid clue words."""
        valid, error = self.validator.is_valid_clue_word("OCEAN", self.board_words)
        assert valid is True
        assert error == ""
        
        valid, error = self.validator.is_valid_clue_word("MUSIC", self.board_words)
        assert valid is True
        assert error == ""
        
        valid, error = self.validator.is_valid_clue_word("Two-Words", self.board_words)
        assert valid is True
        assert error == ""
        
        valid, error = self.validator.is_valid_clue_word("Don't", self.board_words)
        assert valid is True
        assert error == ""
    
    def test_is_valid_clue_word_empty_clue(self):
        """Test empty or whitespace clue words."""
        valid, error = self.validator.is_valid_clue_word("", self.board_words)
        assert valid is False
        assert "cannot be empty" in error
        
        valid, error = self.validator.is_valid_clue_word("   ", self.board_words)
        assert valid is False
        assert "cannot be empty" in error
    
    def test_is_valid_clue_word_invalid_characters(self):
        """Test clue words with invalid characters."""
        valid, error = self.validator.is_valid_clue_word("WORD123", self.board_words)
        assert valid is False
        assert "letters, hyphens, or apostrophes" in error
        
        valid, error = self.validator.is_valid_clue_word("WORD@#$", self.board_words)
        assert valid is False
        assert "letters, hyphens, or apostrophes" in error
    
    def test_is_valid_clue_word_too_short(self):
        """Test clue words that are too short."""
        valid, error = self.validator.is_valid_clue_word("A", self.board_words)
        assert valid is False
        assert "at least 2 characters" in error
        
        valid, error = self.validator.is_valid_clue_word("X", self.board_words)
        assert valid is False
        assert "at least 2 characters" in error
    
    def test_is_valid_clue_word_board_word_exact(self):
        """Test clue words that exactly match board words."""
        valid, error = self.validator.is_valid_clue_word("APPLE", self.board_words)
        assert valid is False
        assert "appears on the board" in error
        
        valid, error = self.validator.is_valid_clue_word("apple", self.board_words)
        assert valid is False
        assert "appears on the board" in error
        
        valid, error = self.validator.is_valid_clue_word("DOG", self.board_words)
        assert valid is False
        assert "appears on the board" in error
    
    def test_is_valid_clue_word_contains_board_word(self):
        """Test clue words that contain board words."""
        valid, error = self.validator.is_valid_clue_word("FIREPLACE", self.board_words)
        assert valid is False
        assert "contain a word that appears" in error
        
        valid, error = self.validator.is_valid_clue_word("DOGHOUSE", self.board_words)
        assert valid is False
        assert "contain a word that appears" in error
    
    def test_is_valid_clue_word_rhyming(self):
        """Test clue words that rhyme with board words."""
        rhyming_board = ["FIRE", "CAT", "RUNNING"]
        
        valid, error = self.validator.is_valid_clue_word("TIRE", rhyming_board)
        assert valid is False
        assert "rhyme with" in error
        
        valid, error = self.validator.is_valid_clue_word("SINGING", rhyming_board)
        assert valid is False
        assert "rhyme with" in error
    
    def test_is_valid_game_word_valid(self):
        """Test valid game words."""
        assert self.validator.is_valid_game_word("HOUSE") is True
        assert self.validator.is_valid_game_word("Two-Word") is True
        assert self.validator.is_valid_game_word("Don't") is True
        assert self.validator.is_valid_game_word("COMPUTER") is True
    
    def test_is_valid_game_word_invalid(self):
        """Test invalid game words."""
        assert self.validator.is_valid_game_word("") is False
        assert self.validator.is_valid_game_word("   ") is False
        assert self.validator.is_valid_game_word("A") is False
        assert self.validator.is_valid_game_word("WORD123") is False
        assert self.validator.is_valid_game_word("WORD@#$") is False
    
    def test_normalize_word(self):
        """Test word normalization."""
        assert self.validator.normalize_word("APPLE") == "apple"
        assert self.validator.normalize_word("  Banana  ") == "banana"
        assert self.validator.normalize_word("Cherry") == "cherry"
        assert self.validator.normalize_word("TWO-WORD") == "two-word"
    
    def test_contains_board_word(self):
        """Test checking if clue contains board words."""
        board_words = ["fire", "cat", "dog"]
        
        assert self.validator._contains_board_word("fireplace", board_words) is True
        assert self.validator._contains_board_word("doghouse", board_words) is True
        assert self.validator._contains_board_word("caterpillar", board_words) is True
        assert self.validator._contains_board_word("music", board_words) is False
        assert self.validator._contains_board_word("ocean", board_words) is False
    
    def test_words_rhyme_simple_cases(self):
        """Test simple rhyming word detection."""
        assert self.validator._words_rhyme("fire", "tire") is True
        assert self.validator._words_rhyme("cat", "bat") is True
        assert self.validator._words_rhyme("running", "singing") is True
        assert self.validator._words_rhyme("house", "mouse") is True
        
        assert self.validator._words_rhyme("fire", "water") is False
        assert self.validator._words_rhyme("cat", "dog") is False
        assert self.validator._words_rhyme("apple", "orange") is False
    
    def test_words_rhyme_identical(self):
        """Test rhyming detection with identical words."""
        assert self.validator._words_rhyme("same", "same") is True
        assert self.validator._words_rhyme("word", "word") is True
    
    def test_words_rhyme_short_words(self):
        """Test rhyming detection with short words."""
        assert self.validator._words_rhyme("a", "b") is False
        assert self.validator._words_rhyme("to", "go") is False
        assert self.validator._words_rhyme("cat", "at") is False
    
    def test_build_rhyme_patterns(self):
        """Test rhyme pattern building."""
        patterns = self.validator._build_rhyme_patterns()
        
        assert 'ing' in patterns
        assert 'tion' in patterns
        assert 'ness' in patterns
        assert 'ment' in patterns
        assert len(patterns) > 20
    
    def test_get_validation_rules(self):
        """Test getting validation rules for display."""
        rules = self.validator.get_validation_rules()
        
        assert isinstance(rules, list)
        assert len(rules) > 0
        assert any("single word" in rule for rule in rules)
        assert any("board" in rule for rule in rules)
        assert any("rhyme" in rule for rule in rules)
    
    def test_edge_case_hyphenated_words(self):
        """Test edge cases with hyphenated words."""
        board_words = ["CO-OP", "TWENTY-ONE", "MOTHER-IN-LAW"]
        
        valid, error = self.validator.is_valid_clue_word("BUSINESS", board_words)
        assert valid is True
        
        valid, error = self.validator.is_valid_clue_word("CO-OP", board_words)
        assert valid is False
        assert "appears on the board" in error
    
    def test_edge_case_apostrophe_words(self):
        """Test edge cases with apostrophe words."""
        board_words = ["DON'T", "CAN'T", "WON'T"]
        
        valid, error = self.validator.is_valid_clue_word("SHOULDN'VE", board_words)
        assert valid is True
        
        valid, error = self.validator.is_valid_clue_word("DON'T", board_words)
        assert valid is False
        assert "appears on the board" in error
