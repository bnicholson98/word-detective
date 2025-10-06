"""Tests for the WordLoader utility."""

import pytest
import tempfile
import os
from pathlib import Path
from src.utils.word_loader import WordLoader


class TestWordLoader:
    """Test cases for WordLoader utility."""
    
    def test_word_loader_init(self):
        """Test WordLoader initialization."""
        loader = WordLoader("test_words.txt")
        assert loader.word_file_path == Path("test_words.txt")
        assert loader._word_cache == []
    
    def test_load_words_success(self):
        """Test successful word loading from file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"TestWord{chr(65+i)}" for i in range(30)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            loaded_words = loader.load_words()
            
            assert len(loaded_words) >= 25
            assert len(loaded_words) == 26  # Only A-Z generate valid words
            assert loader._word_cache == loaded_words
        finally:
            os.unlink(temp_path)
    
    def test_load_words_file_not_found(self):
        """Test loading words when file doesn't exist."""
        loader = WordLoader("nonexistent_file.txt")
        
        with pytest.raises(FileNotFoundError, match="Word list file not found"):
            loader.load_words()
    
    def test_load_words_insufficient_words(self):
        """Test loading words when file has too few words."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Word1\nWord2\nWord3")
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            with pytest.raises(ValueError, match="Word list must contain at least 25 words"):
                loader.load_words()
        finally:
            os.unlink(temp_path)
    
    def test_load_words_with_invalid_words(self):
        """Test loading words with some invalid entries."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            valid_words = [f"ValidWord{chr(65+i)}" for i in range(30)]
            invalid_words = ["", "   ", "X", "123", "Word@#$"]
            all_words = valid_words + invalid_words
            f.write('\n'.join(all_words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            loaded_words = loader.load_words()
            
            assert len(loaded_words) >= 25
            assert all(word in valid_words for word in loaded_words)
            assert not any(word in invalid_words for word in loaded_words if word)
        finally:
            os.unlink(temp_path)
    
    def test_get_random_words(self):
        """Test getting random selection of words."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"TestWord{chr(65+i%26)}{chr(65+(i//26)%26)}" for i in range(50)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            
            random_words_10 = loader.get_random_words(10)
            assert len(random_words_10) == 10
            assert len(set(random_words_10)) == 10
            
            random_words_25 = loader.get_random_words(25)
            assert len(random_words_25) == 25
            assert len(set(random_words_25)) == 25
            
        finally:
            os.unlink(temp_path)
    
    def test_get_random_words_too_many(self):
        """Test requesting more words than available."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"Word{chr(65+i)}" for i in range(30)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            
            with pytest.raises(ValueError, match="Cannot select .* words, only .* available"):
                loader.get_random_words(100)
        finally:
            os.unlink(temp_path)
    
    def test_get_game_words(self):
        """Test getting exactly 25 words for game."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"GameWord{chr(65+i%26)}{chr(65+(i//26)%26)}" for i in range(50)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            game_words = loader.get_game_words()
            
            assert len(game_words) == 25
            assert len(set(game_words)) == 25
        finally:
            os.unlink(temp_path)
    
    def test_word_exists(self):
        """Test checking if word exists in loaded list."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = ["Apple", "Banana", "Cherry", "Date", "Elderberry"] + [f"Word{chr(65+i)}" for i in range(25)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            
            assert loader.word_exists("Apple") is True
            assert loader.word_exists("apple") is True
            assert loader.word_exists("APPLE") is True
            assert loader.word_exists("Nonexistent") is False
        finally:
            os.unlink(temp_path)
    
    def test_get_word_count(self):
        """Test getting total word count."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"CountWord{chr(65+i%26)}{chr(65+(i//26)%26)}" for i in range(42)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            count = loader.get_word_count()
            assert count == 42
        finally:
            os.unlink(temp_path)
    
    def test_is_valid_word(self):
        """Test word validity checking."""
        assert WordLoader._is_valid_word("ValidWord") is True
        assert WordLoader._is_valid_word("Two-Words") is True
        assert WordLoader._is_valid_word("Don't") is True
        assert WordLoader._is_valid_word("AB") is True
        
        assert WordLoader._is_valid_word("") is False
        assert WordLoader._is_valid_word("   ") is False
        assert WordLoader._is_valid_word("A") is False
        assert WordLoader._is_valid_word("WordABC") is True
        assert WordLoader._is_valid_word("Word123") is False
        assert WordLoader._is_valid_word("Word@#$") is False
    
    def test_validate_word_list_file(self):
        """Test word list file validation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"ValidateWord{chr(65+i)}" for i in range(30)]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            validation = loader.validate_word_list_file()
            
            assert validation["valid"] is True
            assert validation["word_count"] == 30
            assert validation["valid_words"] == 26
            assert validation["min_required"] == 25
            assert validation["error"] is None
        finally:
            os.unlink(temp_path)
    
    def test_validate_word_list_file_not_found(self):
        """Test validation when file doesn't exist."""
        loader = WordLoader("nonexistent.txt")
        validation = loader.validate_word_list_file()
        
        assert validation["valid"] is False
        assert "File not found" in validation["error"]
        assert validation["word_count"] == 0
        assert validation["valid_words"] == 0
    
    def test_validate_word_list_insufficient_words(self):
        """Test validation with insufficient valid words."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = ["WordA", "WordB", "WordC", "", "Invalid123"]
            f.write('\n'.join(words))
            temp_path = f.name
        
        try:
            loader = WordLoader(temp_path)
            validation = loader.validate_word_list_file()
            
            assert validation["valid"] is False
            assert validation["word_count"] == 5
            assert validation["valid_words"] == 3
            assert "Not enough valid words" in validation["error"]
        finally:
            os.unlink(temp_path)
