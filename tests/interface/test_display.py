"""Tests for the GameDisplay class."""

import pytest
from io import StringIO
from unittest.mock import patch
from src.interface.display import GameDisplay


class TestGameDisplay:
    """Test cases for GameDisplay class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.display = GameDisplay()
    
    def test_display_initialization(self):
        """Test display initialization."""
        display = GameDisplay()
        assert display.console is not None
        assert len(display.color_map) == 4
        assert "red" in display.color_map
        assert "blue" in display.color_map
        assert "neutral" in display.color_map
        assert "failure" in display.color_map
    
    def test_color_map(self):
        """Test color mappings."""
        assert self.display.color_map["red"] == "red"
        assert self.display.color_map["blue"] == "blue"
        assert self.display.color_map["neutral"] == "yellow"
        assert self.display.color_map["failure"] == "black on white"
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_title(self, mock_stdout):
        """Test title display."""
        self.display.show_title()
        output = mock_stdout.getvalue()
        assert "WORD DETECTIVE" in output or output != ""
    
    def test_show_board_basic(self):
        """Test basic board display."""
        board_data = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append({
                    "word": f"WORD{i}{j}",
                    "revealed": False,
                    "color": None
                })
            board_data.append(row)
        
        try:
            self.display.show_board(board_data, show_colors=False)
        except Exception as e:
            pytest.fail(f"show_board raised exception: {e}")
    
    def test_show_board_with_colors(self):
        """Test board display with colors shown."""
        board_data = []
        colors = ["red", "blue", "neutral", "failure", "red"]
        
        for i in range(5):
            row = []
            for j in range(5):
                row.append({
                    "word": f"WORD{i}{j}",
                    "revealed": False,
                    "color": colors[j]
                })
            board_data.append(row)
        
        try:
            self.display.show_board(board_data, show_colors=True)
        except Exception as e:
            pytest.fail(f"show_board with colors raised exception: {e}")
    
    def test_show_board_revealed_cards(self):
        """Test board display with revealed cards."""
        board_data = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append({
                    "word": f"WORD{i}{j}",
                    "revealed": i == 0,
                    "color": "red" if i == 0 else None
                })
            board_data.append(row)
        
        try:
            self.display.show_board(board_data, show_colors=False)
        except Exception as e:
            pytest.fail(f"show_board with revealed cards raised exception: {e}")
    
    def test_show_game_status(self):
        """Test game status display."""
        board_state = {
            "current_team": "red",
            "turn_type": "chief_clue",
            "phase": "clue_giving",
            "red_words_remaining": 9,
            "blue_words_remaining": 8,
            "current_clue": None
        }
        
        try:
            self.display.show_game_status(board_state)
        except Exception as e:
            pytest.fail(f"show_game_status raised exception: {e}")
    
    def test_show_game_status_with_clue(self):
        """Test game status display with active clue."""
        board_state = {
            "current_team": "blue",
            "turn_type": "detective_guess",
            "phase": "guessing",
            "red_words_remaining": 7,
            "blue_words_remaining": 6,
            "current_clue": {
                "word": "OCEAN",
                "number": 2,
                "guesses_remaining": 3
            }
        }
        
        try:
            self.display.show_game_status(board_state)
        except Exception as e:
            pytest.fail(f"show_game_status with clue raised exception: {e}")
    
    def test_show_team_info(self):
        """Test team info display."""
        team_info = {
            "red_team": {
                "players": [
                    {"name": "Red Chief", "role": "chief"},
                    {"name": "Red Detective", "role": "detective"}
                ],
                "words_remaining": 9,
                "total_words": 9
            },
            "blue_team": {
                "players": [
                    {"name": "Blue Chief", "role": "chief"},
                    {"name": "Blue Detective", "role": "detective"}
                ],
                "words_remaining": 8,
                "total_words": 8
            }
        }
        
        try:
            self.display.show_team_info(team_info)
        except Exception as e:
            pytest.fail(f"show_team_info raised exception: {e}")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_message(self, mock_stdout):
        """Test message display."""
        self.display.show_message("Test message")
        output = mock_stdout.getvalue()
        assert "Test message" in output or output != ""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_error(self, mock_stdout):
        """Test error message display."""
        self.display.show_error("Test error")
        output = mock_stdout.getvalue()
        assert output != ""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_success(self, mock_stdout):
        """Test success message display."""
        self.display.show_success("Test success")
        output = mock_stdout.getvalue()
        assert output != ""
    
    def test_show_guess_result(self):
        """Test guess result display."""
        result = {
            "word": "APPLE",
            "color": "red",
            "continue_turn": True,
            "winner": None
        }
        
        try:
            self.display.show_guess_result(result)
        except Exception as e:
            pytest.fail(f"show_guess_result raised exception: {e}")
    
    def test_show_guess_result_with_winner(self):
        """Test guess result display with winner."""
        result = {
            "word": "FINAL",
            "color": "blue",
            "continue_turn": False,
            "winner": "blue"
        }
        
        try:
            self.display.show_guess_result(result)
        except Exception as e:
            pytest.fail(f"show_guess_result with winner raised exception: {e}")
    
    def test_show_winner(self):
        """Test winner display."""
        try:
            self.display.show_winner("red")
            self.display.show_winner("blue")
        except Exception as e:
            pytest.fail(f"show_winner raised exception: {e}")
    
    def test_show_menu(self):
        """Test menu display."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        try:
            self.display.show_menu(options)
        except Exception as e:
            pytest.fail(f"show_menu raised exception: {e}")
    
    def test_show_key_card(self):
        """Test key card display."""
        key_card = []
        colors = ["red", "red", "blue", "blue", "neutral"]
        
        for i in range(25):
            key_card.append({
                "word": f"WORD{i}",
                "color": colors[i % 5],
                "revealed": i < 5,
                "position": (i // 5, i % 5)
            })
        
        try:
            self.display.show_key_card(key_card)
        except Exception as e:
            pytest.fail(f"show_key_card raised exception: {e}")
