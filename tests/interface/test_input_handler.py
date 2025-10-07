"""Tests for the InputHandler class."""

import pytest
from unittest.mock import patch, MagicMock
from src.interface.input_handler import InputHandler


class TestInputHandler:
    """Test cases for InputHandler class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.handler = InputHandler()
    
    def test_handler_initialization(self):
        """Test handler initialization."""
        handler = InputHandler()
        assert handler.console is not None
    

    

    
    @patch('rich.prompt.Prompt.ask')
    def test_get_starting_team_red(self, mock_ask):
        """Test getting starting team red."""
        mock_ask.return_value = "red"
        
        team = self.handler.get_starting_team()
        assert team == "red"
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_starting_team_random(self, mock_ask):
        """Test getting random starting team."""
        mock_ask.return_value = "random"
        
        team = self.handler.get_starting_team()
        assert team is None
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_clue_valid(self, mock_ask):
        """Test getting valid clue."""
        mock_ask.side_effect = ["OCEAN", "2"]
        
        word, number = self.handler.get_clue()
        assert word == "OCEAN"
        assert number == 2
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_clue_invalid_number(self, mock_ask):
        """Test getting clue with invalid number."""
        mock_ask.side_effect = ["OCEAN", "0", "OCEAN", "2"]
        
        word, number = self.handler.get_clue()
        assert word == "OCEAN"
        assert number == 2
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_guess_valid(self, mock_ask):
        """Test getting valid guess."""
        mock_ask.return_value = "APPLE"
        available_words = ["APPLE", "BANANA", "CHERRY"]
        
        guess = self.handler.get_guess(available_words)
        assert guess == "APPLE"
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_guess_case_insensitive(self, mock_ask):
        """Test guess is case insensitive."""
        mock_ask.return_value = "apple"
        available_words = ["APPLE", "BANANA", "CHERRY"]
        
        guess = self.handler.get_guess(available_words)
        assert guess == "apple"
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_guess_invalid_then_valid(self, mock_ask):
        """Test getting guess with invalid then valid input."""
        mock_ask.side_effect = ["NOTHERE", "APPLE"]
        available_words = ["APPLE", "BANANA", "CHERRY"]
        
        guess = self.handler.get_guess(available_words)
        assert guess == "APPLE"
        assert mock_ask.call_count == 2
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_menu_choice_valid(self, mock_ask):
        """Test getting valid menu choice."""
        mock_ask.return_value = "2"
        
        choice = self.handler.get_menu_choice(3)
        assert choice == 2
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_menu_choice_out_of_range(self, mock_ask):
        """Test menu choice out of range."""
        mock_ask.side_effect = ["5", "2"]
        
        choice = self.handler.get_menu_choice(3)
        assert choice == 2
        assert mock_ask.call_count == 2
    
    @patch('rich.prompt.Confirm.ask')
    def test_confirm_action_yes(self, mock_ask):
        """Test confirming action."""
        mock_ask.return_value = True
        
        result = self.handler.confirm_action("Continue?")
        assert result is True
    
    @patch('rich.prompt.Confirm.ask')
    def test_confirm_action_no(self, mock_ask):
        """Test declining action."""
        mock_ask.return_value = False
        
        result = self.handler.confirm_action("Continue?")
        assert result is False
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_word_from_list(self, mock_ask):
        """Test getting word from list."""
        mock_ask.return_value = "2"
        words = ["APPLE", "BANANA", "CHERRY"]
        
        word = self.handler.get_word_from_list(words)
        assert word == "BANANA"
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_text_input(self, mock_ask):
        """Test getting text input."""
        mock_ask.return_value = "Test Input"
        
        text = self.handler.get_text_input("Enter text")
        assert text == "Test Input"
    
    @patch('rich.prompt.Prompt.ask')
    def test_get_text_input_with_default(self, mock_ask):
        """Test getting text input with default."""
        mock_ask.return_value = "Default"
        
        text = self.handler.get_text_input("Enter text", default="Default")
        assert text == "Default"
