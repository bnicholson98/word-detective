"""Tests for the GameInterface class."""

import pytest
from unittest.mock import patch, MagicMock
from src.interface.game_interface import GameInterface
from src.game.game_controller import GameController


class TestGameInterface:
    """Test cases for GameInterface class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.controller = MagicMock(spec=GameController)
        self.interface = GameInterface(self.controller)
    
    def test_interface_initialization(self):
        """Test interface initialization."""
        controller = MagicMock(spec=GameController)
        interface = GameInterface(controller)
        
        assert interface.controller is controller
        assert interface.display is not None
        assert interface.input_handler is not None
    
    @patch('src.interface.game_interface.InputHandler')
    @patch('src.interface.game_interface.GameDisplay')
    def test_setup_game_success(self, mock_display_class, mock_input_class):
        """Test successful game setup."""
        mock_input = MagicMock()
        mock_input.get_starting_team.return_value = "red"
        mock_input_class.return_value = mock_input
        
        mock_display = MagicMock()
        mock_display_class.return_value = mock_display
        
        self.interface.input_handler = mock_input
        self.interface.display = mock_display
        
        self.controller.setup_teams.return_value = (True, "")
        self.controller.start_game.return_value = (True, "")
        
        result = self.interface.setup_game()
        assert result is True
    
    @patch('src.interface.game_interface.InputHandler')
    @patch('src.interface.game_interface.GameDisplay')
    def test_setup_game_team_setup_failure(self, mock_display_class, mock_input_class):
        """Test game setup with team setup failure."""
        mock_input = MagicMock()
        mock_input_class.return_value = mock_input
        
        mock_display = MagicMock()
        mock_display_class.return_value = mock_display
        
        self.interface.input_handler = mock_input
        self.interface.display = mock_display
        
        self.controller.setup_teams.return_value = (False, "Setup error")
        
        result = self.interface.setup_game()
        assert result is False
    
    def test_show_main_menu(self):
        """Test showing main menu."""
        self.interface.input_handler.get_menu_choice = MagicMock(return_value=1)
        
        choice = self.interface.show_main_menu()
        assert choice == 1
    
    @patch('src.interface.input_handler.InputHandler.wait_for_enter')
    def test_show_rules(self, mock_wait):
        """Test showing game rules."""
        mock_wait.return_value = None
        try:
            self.interface.show_rules()
        except Exception as e:
            pytest.fail(f"show_rules raised exception: {e}")
    

    
    def test_handle_chief_turn(self):
        """Test handling chief turn."""
        key_card = []
        for i in range(25):
            key_card.append({
                "word": f"WORD{i}",
                "color": "red",
                "revealed": False,
                "position": (i // 5, i % 5)
            })
        
        self.controller.get_key_card.return_value = key_card
        self.controller.get_board_state.return_value = {
            "board": [[{"word": "TEST", "revealed": False} for _ in range(5)] for _ in range(5)]
        }
        self.controller.give_clue.return_value = (True, "")
        
        self.interface.input_handler.get_clue = MagicMock(return_value=("NATURE", 2))
        self.interface.input_handler.wait_for_enter = MagicMock()
        
        try:
            self.interface._handle_chief_turn("red")
        except Exception as e:
            pytest.fail(f"_handle_chief_turn raised exception: {e}")
    
    def test_handle_detective_turn_pass(self):
        """Test handling detective turn with pass."""
        self.controller.get_board_state.return_value = {
            "board": [[{"word": "TEST", "revealed": False} for _ in range(5)] for _ in range(5)],
            "current_clue": {"guesses_remaining": 1}
        }
        
        self.interface.input_handler.confirm_action = MagicMock(return_value=False)
        self.interface.input_handler.wait_for_enter = MagicMock()
        
        try:
            self.interface._handle_detective_turn("blue")
        except Exception as e:
            pytest.fail(f"_handle_detective_turn with pass raised exception: {e}")
    
    def test_handle_detective_turn_guess(self):
        """Test handling detective turn with guess."""
        self.controller.get_board_state.return_value = {
            "board": [[{"word": "TEST", "revealed": False} for _ in range(5)] for _ in range(5)],
            "current_clue": {"guesses_remaining": 2}
        }
        self.controller.make_guess.return_value = (True, "", {
            "word": "TEST",
            "color": "red",
            "continue_turn": True,
            "winner": None
        })
        
        self.interface.input_handler.confirm_action = MagicMock(return_value=True)
        self.interface.input_handler.get_guess = MagicMock(return_value="TEST")
        self.interface.input_handler.wait_for_enter = MagicMock()
        
        try:
            self.interface._handle_detective_turn("red")
        except Exception as e:
            pytest.fail(f"_handle_detective_turn with guess raised exception: {e}")
    
    def test_show_game_over(self):
        """Test showing game over screen."""
        self.controller.get_board_state.return_value = {
            "board": [[None for _ in range(5)] for _ in range(5)],
            "winner": "red"
        }
        self.controller.get_team_info.return_value = {
            "red_team": {"players": [], "words_remaining": 0, "total_words": 9},
            "blue_team": {"players": [], "words_remaining": 5, "total_words": 8}
        }
        
        try:
            self.interface._show_game_over()
        except Exception as e:
            pytest.fail(f"_show_game_over raised exception: {e}")
