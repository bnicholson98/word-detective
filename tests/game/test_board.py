"""Tests for the GameBoard class."""

import pytest
from src.game.board import GameBoard, BoardConfiguration
from src.models.card import CardColor
from src.utils.word_loader import WordLoader
import tempfile
import os


class TestBoardConfiguration:
    """Test cases for BoardConfiguration dataclass."""
    
    def test_default_configuration(self):
        """Test default board configuration values."""
        config = BoardConfiguration()
        assert config.starting_team_words == 9
        assert config.second_team_words == 8
        assert config.neutral_words == 7
        assert config.failure_words == 1
    
    def test_custom_configuration(self):
        """Test custom board configuration."""
        config = BoardConfiguration(
            starting_team_words=10,
            second_team_words=7,
            neutral_words=6,
            failure_words=2
        )
        assert config.starting_team_words == 10
        assert config.second_team_words == 7
        assert config.neutral_words == 6
        assert config.failure_words == 2


class TestGameBoard:
    """Test cases for GameBoard class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"TestWord{chr(65+i%26)}{chr(65+(i//26)%26)}" for i in range(50)]
            f.write('\n'.join(words))
            self.temp_word_file = f.name
        
        self.word_loader = WordLoader(self.temp_word_file)
        self.board = GameBoard(self.word_loader)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_word_file)
    
    def test_board_initialization(self):
        """Test board initialization."""
        board = GameBoard()
        assert len(board.board) == 5
        assert all(len(row) == 5 for row in board.board)
        assert len(board.cards) == 0
        assert not board.is_board_complete()
    
    def test_generate_board_red_start(self):
        """Test board generation with red team starting."""
        self.board.generate_board(CardColor.RED)
        
        assert self.board.is_board_complete()
        assert len(self.board.cards) == 25
        assert len(self.board.get_key_card()) == 25
        
        red_count = sum(1 for card in self.board.cards if card.color == CardColor.RED)
        blue_count = sum(1 for card in self.board.cards if card.color == CardColor.BLUE)
        neutral_count = sum(1 for card in self.board.cards if card.color == CardColor.NEUTRAL)
        failure_count = sum(1 for card in self.board.cards if card.color == CardColor.FAILURE)
        
        assert red_count == 9
        assert blue_count == 8
        assert neutral_count == 7
        assert failure_count == 1
    
    def test_generate_board_blue_start(self):
        """Test board generation with blue team starting."""
        self.board.generate_board(CardColor.BLUE)
        
        assert self.board.is_board_complete()
        
        red_count = sum(1 for card in self.board.cards if card.color == CardColor.RED)
        blue_count = sum(1 for card in self.board.cards if card.color == CardColor.BLUE)
        
        assert blue_count == 9
        assert red_count == 8
    
    def test_generate_board_invalid_team(self):
        """Test board generation with invalid starting team."""
        with pytest.raises(ValueError, match="Starting team must be RED or BLUE"):
            self.board.generate_board(CardColor.NEUTRAL)
    
    def test_get_card_valid_position(self):
        """Test getting card at valid position."""
        self.board.generate_board(CardColor.RED)
        card = self.board.get_card(2, 3)
        assert card is not None
        assert card.position == (2, 3)
    
    def test_get_card_invalid_position(self):
        """Test getting card at invalid position."""
        with pytest.raises(ValueError, match="Position must be within board bounds"):
            self.board.get_card(-1, 0)
        
        with pytest.raises(ValueError, match="Position must be within board bounds"):
            self.board.get_card(5, 0)
    
    def test_get_card_by_word(self):
        """Test getting card by word."""
        self.board.generate_board(CardColor.RED)
        word = self.board.cards[0].word
        card = self.board.get_card_by_word(word)
        assert card.word == word
    
    def test_get_card_by_word_not_found(self):
        """Test getting card by non-existent word."""
        self.board.generate_board(CardColor.RED)
        with pytest.raises(ValueError, match="Word 'NONEXISTENT' not found on board"):
            self.board.get_card_by_word("NONEXISTENT")
    
    def test_reveal_card_by_position(self):
        """Test revealing card by position."""
        self.board.generate_board(CardColor.RED)
        card = self.board.get_card(1, 1)
        original_color = card.color
        
        assert not card.revealed
        revealed_color = self.board.reveal_card(1, 1)
        assert card.revealed
        assert revealed_color == original_color
    
    def test_reveal_card_by_word(self):
        """Test revealing card by word."""
        self.board.generate_board(CardColor.RED)
        word = self.board.cards[5].word
        original_color = self.board.cards[5].color
        
        revealed_color = self.board.reveal_card_by_word(word)
        assert self.board.cards[5].revealed
        assert revealed_color == original_color
    
    def test_get_all_words(self):
        """Test getting all words on board."""
        self.board.generate_board(CardColor.RED)
        words = self.board.get_all_words()
        assert len(words) == 25
        assert len(set(words)) == 25
    
    def test_get_unrevealed_words(self):
        """Test getting unrevealed words."""
        self.board.generate_board(CardColor.RED)
        
        initial_unrevealed = self.board.get_unrevealed_words()
        assert len(initial_unrevealed) == 25
        
        self.board.reveal_card(0, 0)
        after_reveal = self.board.get_unrevealed_words()
        assert len(after_reveal) == 24
    
    def test_get_team_words(self):
        """Test getting words for specific team."""
        self.board.generate_board(CardColor.RED)
        
        red_words = self.board.get_team_words(CardColor.RED)
        blue_words = self.board.get_team_words(CardColor.BLUE)
        neutral_words = self.board.get_team_words(CardColor.NEUTRAL)
        failure_words = self.board.get_team_words(CardColor.FAILURE)
        
        assert len(red_words) == 9
        assert len(blue_words) == 8
        assert len(neutral_words) == 7
        assert len(failure_words) == 1
    
    def test_get_unrevealed_team_words(self):
        """Test getting unrevealed words for team."""
        self.board.generate_board(CardColor.RED)
        
        red_words = self.board.get_team_words(CardColor.RED)
        first_red_word = red_words[0]
        
        initial_unrevealed = self.board.get_unrevealed_team_words(CardColor.RED)
        assert len(initial_unrevealed) == 9
        
        self.board.reveal_card_by_word(first_red_word)
        after_reveal = self.board.get_unrevealed_team_words(CardColor.RED)
        assert len(after_reveal) == 8
        assert first_red_word not in after_reveal
    
    def test_count_team_words_remaining(self):
        """Test counting remaining team words."""
        self.board.generate_board(CardColor.RED)
        
        assert self.board.count_team_words_remaining(CardColor.RED) == 9
        assert self.board.count_team_words_remaining(CardColor.BLUE) == 8
        
        red_word = self.board.get_team_words(CardColor.RED)[0]
        self.board.reveal_card_by_word(red_word)
        assert self.board.count_team_words_remaining(CardColor.RED) == 8
    
    def test_is_word_revealed(self):
        """Test checking if word is revealed."""
        self.board.generate_board(CardColor.RED)
        word = self.board.cards[0].word
        
        assert not self.board.is_word_revealed(word)
        self.board.reveal_card_by_word(word)
        assert self.board.is_word_revealed(word)
        
        assert not self.board.is_word_revealed("NONEXISTENT")
    
    def test_get_key_card(self):
        """Test getting key card."""
        self.board.generate_board(CardColor.RED)
        key_card = self.board.get_key_card()
        
        assert len(key_card) == 25
        assert sum(1 for color in key_card if color == CardColor.RED) == 9
        assert sum(1 for color in key_card if color == CardColor.BLUE) == 8
        assert sum(1 for color in key_card if color == CardColor.NEUTRAL) == 7
        assert sum(1 for color in key_card if color == CardColor.FAILURE) == 1
    
    def test_card_positions(self):
        """Test that cards have correct positions."""
        self.board.generate_board(CardColor.RED)
        
        for i, card in enumerate(self.board.cards):
            expected_row, expected_col = divmod(i, 5)
            assert card.position == (expected_row, expected_col)
            assert self.board.board[expected_row][expected_col] == card
