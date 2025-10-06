"""Tests for the GameController class."""

import pytest
import tempfile
import os
from src.game.game_controller import GameController
from src.models.card import CardColor
from src.models.player import PlayerRole
from src.utils.word_loader import WordLoader


class TestGameController:
    """Test cases for GameController class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            words = [f"TestWord{chr(65+i%26)}{chr(65+(i//26)%26)}" for i in range(50)]
            f.write('\n'.join(words))
            self.temp_word_file = f.name
        
        self.word_loader = WordLoader(self.temp_word_file)
        self.controller = GameController(self.word_loader)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_word_file)
    
    def test_controller_initialization(self):
        """Test controller initialization."""
        controller = GameController()
        assert controller.board is not None
        assert controller.rules is not None
        assert controller.game_state is not None
    
    def test_setup_teams_valid(self):
        """Test valid team setup."""
        red_players = [("Red Chief", "chief"), ("Red Detective", "detective")]
        blue_players = [("Blue Chief", "chief"), ("Blue Detective", "detective")]
        
        success, error = self.controller.setup_teams(red_players, blue_players)
        assert success is True
        assert error == ""
        assert self.controller.game_state.red_team is not None
        assert self.controller.game_state.blue_team is not None
    
    def test_setup_teams_invalid_role(self):
        """Test team setup with invalid role."""
        red_players = [("Red Chief", "invalid_role")]
        blue_players = [("Blue Chief", "chief"), ("Blue Detective", "detective")]
        
        success, error = self.controller.setup_teams(red_players, blue_players)
        assert success is False
        assert error != ""
    
    def test_setup_teams_no_chief(self):
        """Test team setup without Chief."""
        red_players = [("Red Detective", "detective")]
        blue_players = [("Blue Chief", "chief"), ("Blue Detective", "detective")]
        
        success, error = self.controller.setup_teams(red_players, blue_players)
        assert success is False
        assert "Red team" in error
        assert "Chief" in error
    
    def test_start_game_valid(self):
        """Test valid game start."""
        self.setup_valid_teams()
        
        success, error = self.controller.start_game("red")
        assert success is True
        assert error == ""
        assert self.controller.board.is_board_complete()
        assert self.controller.game_state.red_team.total_words == 9
        assert self.controller.game_state.blue_team.total_words == 8
    
    def test_start_game_without_teams(self):
        """Test game start without teams set up."""
        success, error = self.controller.start_game()
        assert success is False
        assert "Both teams must be set up" in error
    
    def test_start_game_random_team(self):
        """Test game start with random starting team."""
        self.setup_valid_teams()
        
        success, error = self.controller.start_game()
        assert success is True
        assert error == ""
    
    def test_start_game_invalid_starting_team(self):
        """Test game start with invalid starting team."""
        self.setup_valid_teams()
        
        success, error = self.controller.start_game("purple")
        assert success is False
        assert "must be 'red' or 'blue'" in error
    
    def test_give_clue_valid(self):
        """Test giving valid clue."""
        self.setup_and_start_game()
        
        success, error = self.controller.give_clue("OCEAN", 2)
        assert success is True
        assert error == ""
        assert self.controller.game_state.current_clue is not None
        assert self.controller.game_state.current_clue.word == "OCEAN"
        assert self.controller.game_state.current_clue.number == 2
    
    def test_give_clue_invalid_word(self):
        """Test giving clue with board word."""
        self.setup_and_start_game()
        
        board_word = self.controller.board.cards[0].word
        success, error = self.controller.give_clue(board_word, 1)
        assert success is False
        assert "appears on the board" in error
    
    def test_give_clue_too_high_number(self):
        """Test giving clue with number too high."""
        self.setup_and_start_game()
        
        success, error = self.controller.give_clue("OCEAN", 15)
        assert success is False
        assert "cannot exceed" in error
    
    def test_make_guess_valid_correct(self):
        """Test making valid guess for team word."""
        self.setup_and_start_game()
        self.controller.give_clue("OCEAN", 2)
        
        red_words = self.controller.board.get_team_words(CardColor.RED)
        target_word = red_words[0]
        
        success, error, result = self.controller.make_guess(target_word)
        assert success is True
        assert error == ""
        assert result["color"] == "red"
        assert result["continue_turn"] is True
    
    def test_make_guess_valid_wrong_team(self):
        """Test making guess for wrong team word."""
        self.setup_and_start_game()
        self.controller.give_clue("OCEAN", 2)
        
        blue_words = self.controller.board.get_team_words(CardColor.BLUE)
        target_word = blue_words[0]
        
        success, error, result = self.controller.make_guess(target_word)
        assert success is True
        assert error == ""
        assert result["color"] == "blue"
        assert result["continue_turn"] is False
    
    def test_make_guess_without_clue(self):
        """Test making guess without active clue."""
        self.setup_and_start_game()
        
        success, error, result = self.controller.make_guess("ANYTHING")
        assert success is False
        assert ("No active clue" in error or "Not guessing phase" in error)
    
    def test_make_guess_invalid_word(self):
        """Test making guess for word not on board."""
        self.setup_and_start_game()
        self.controller.give_clue("OCEAN", 2)
        
        success, error, result = self.controller.make_guess("NOTHERE")
        assert success is False
        assert "is not on the board" in error
    
    def test_end_turn(self):
        """Test ending turn switches teams."""
        self.setup_and_start_game()
        original_team = self.controller.game_state.current_team_color
        
        self.controller.end_turn()
        
        new_team = self.controller.game_state.current_team_color
        assert new_team != original_team
        assert self.controller.game_state.current_clue is None
    
    def test_get_board_state(self):
        """Test getting board state information."""
        self.setup_and_start_game()
        
        board_state = self.controller.get_board_state()
        
        assert "board" in board_state
        assert "current_team" in board_state
        assert "turn_type" in board_state
        assert "phase" in board_state
        assert "red_words_remaining" in board_state
        assert "blue_words_remaining" in board_state
        assert len(board_state["board"]) == 5
        assert len(board_state["board"][0]) == 5
    
    def test_get_key_card(self):
        """Test getting key card for Chiefs."""
        self.setup_and_start_game()
        
        key_card = self.controller.get_key_card()
        
        assert len(key_card) == 25
        for card_info in key_card:
            assert "word" in card_info
            assert "color" in card_info
            assert "revealed" in card_info
            assert "position" in card_info
    
    def test_get_team_info(self):
        """Test getting team information."""
        self.setup_and_start_game()
        
        team_info = self.controller.get_team_info()
        
        assert "red_team" in team_info
        assert "blue_team" in team_info
        assert len(team_info["red_team"]["players"]) == 2
        assert len(team_info["blue_team"]["players"]) == 2
        assert team_info["red_team"]["total_words"] == 9
        assert team_info["blue_team"]["total_words"] == 8
    
    def test_reset_game(self):
        """Test resetting game state."""
        self.setup_and_start_game()
        self.controller.give_clue("OCEAN", 2)
        
        self.controller.reset_game()
        
        assert not self.controller.game_state.game_over
        assert self.controller.game_state.current_clue is None
        assert self.controller.game_state.red_team is None
        assert self.controller.game_state.blue_team is None
    
    def test_full_game_flow(self):
        """Test complete game flow."""
        self.setup_and_start_game()
        
        self.controller.give_clue("NATURE", 2)
        assert self.controller.game_state.current_clue.word == "NATURE"
        
        red_words = self.controller.board.get_team_words(CardColor.RED)
        success, error, result = self.controller.make_guess(red_words[0])
        assert success is True
        assert result["color"] == "red"
        
        neutral_words = self.controller.board.get_team_words(CardColor.NEUTRAL)
        success, error, result = self.controller.make_guess(neutral_words[0])
        assert success is True
        assert result["color"] == "neutral"
        assert result["continue_turn"] is False
    
    def setup_valid_teams(self):
        """Helper to set up valid teams."""
        red_players = [("Red Chief", "chief"), ("Red Detective", "detective")]
        blue_players = [("Blue Chief", "chief"), ("Blue Detective", "detective")]
        self.controller.setup_teams(red_players, blue_players)
    
    def setup_and_start_game(self):
        """Helper to set up teams and start game."""
        self.setup_valid_teams()
        success, error = self.controller.start_game("red")
        if not success:
            raise Exception(f"Failed to start game: {error}")
