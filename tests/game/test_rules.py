"""Tests for the GameRules class."""

import pytest
from src.game.rules import GameRules
from src.models.card import Card, CardColor
from src.models.clue import Clue
from src.models.team import Team
from src.models.player import Player, PlayerRole
from src.models.game_state import GameState, TurnType, GamePhase


class TestGameRules:
    """Test cases for GameRules class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.rules = GameRules()
        self.game_state = self.create_test_game_state()
    
    def create_test_game_state(self):
        """Create a test game state."""
        game_state = GameState()
        
        red_team = Team(color=CardColor.RED)
        red_team.add_player(Player("Red Chief", PlayerRole.CHIEF))
        red_team.add_player(Player("Red Detective", PlayerRole.DETECTIVE))
        red_team.set_word_count(9)
        
        blue_team = Team(color=CardColor.BLUE)
        blue_team.add_player(Player("Blue Chief", PlayerRole.CHIEF))
        blue_team.add_player(Player("Blue Detective", PlayerRole.DETECTIVE))
        blue_team.set_word_count(8)
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        
        words = ["APPLE", "BANANA", "CHERRY", "DOG", "ELEPHANT"]
        cards = []
        for i, word in enumerate(words):
            color = CardColor.RED if i < 2 else CardColor.BLUE if i < 4 else CardColor.NEUTRAL
            card = Card(word=word, color=color, position=(0, i))
            cards.append(card)
            game_state.board[0][i] = card
        
        # Fix the test data issue
        if len(words) > 2:
            words[1] = "REDWORD"  # Make sure we have different colored words
            game_state.board[0][1] = Card(word="REDWORD", color=CardColor.RED, position=(0, 1))
        if len(words) > 3:
            words[2] = "BLUEWORD"
            game_state.board[0][2] = Card(word="BLUEWORD", color=CardColor.BLUE, position=(0, 2))
        
        game_state.start_game()
        return game_state
    
    def test_validate_clue_valid(self):
        """Test valid clue validation."""
        valid, error = self.rules.validate_clue("OCEAN", 2, self.game_state)
        assert valid is True
        assert error == ""
    
    def test_validate_clue_invalid_number(self):
        """Test clue validation with invalid number."""
        valid, error = self.rules.validate_clue("OCEAN", 0, self.game_state)
        assert valid is False
        assert "must be at least 1" in error
        
        valid, error = self.rules.validate_clue("OCEAN", 26, self.game_state)
        assert valid is False
        assert "cannot exceed 25" in error
    
    def test_validate_clue_board_word(self):
        """Test clue validation with board word."""
        valid, error = self.rules.validate_clue("APPLE", 1, self.game_state)
        assert valid is False
        assert "appears on the board" in error
    
    def test_can_give_clue_valid(self):
        """Test valid clue giving conditions."""
        self.game_state.turn_type = TurnType.CHIEF_CLUE
        can_give, error = self.rules.can_give_clue(self.game_state)
        assert can_give is True
        assert error == ""
    
    def test_can_give_clue_game_over(self):
        """Test clue giving when game is over."""
        self.game_state.game_over = True
        can_give, error = self.rules.can_give_clue(self.game_state)
        assert can_give is False
        assert error == "Game is over"
    
    def test_can_give_clue_wrong_phase(self):
        """Test clue giving in wrong phase."""
        self.game_state.turn_type = TurnType.DETECTIVE_GUESS
        can_give, error = self.rules.can_give_clue(self.game_state)
        assert can_give is False
        assert error == "Not clue-giving phase"
    
    def test_can_make_guess_valid(self):
        """Test valid guess conditions."""
        clue = Clue("OCEAN", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.turn_type = TurnType.DETECTIVE_GUESS
        
        can_guess, error = self.rules.can_make_guess(self.game_state)
        assert can_guess is True
        assert error == ""
    
    def test_can_make_guess_no_clue(self):
        """Test guess when no active clue."""
        self.game_state.current_clue = None
        self.game_state.turn_type = TurnType.DETECTIVE_GUESS
        
        can_guess, error = self.rules.can_make_guess(self.game_state)
        assert can_guess is False
        assert error == "No active clue"
    
    def test_can_make_guess_no_guesses_left(self):
        """Test guess when no guesses remaining."""
        clue = Clue("OCEAN", 1, CardColor.RED)
        clue.use_guess()
        clue.use_guess()
        self.game_state.current_clue = clue
        self.game_state.turn_type = TurnType.DETECTIVE_GUESS
        
        can_guess, error = self.rules.can_make_guess(self.game_state)
        assert can_guess is False
        assert error == "No guesses remaining for current clue"
    
    def test_validate_guess_valid(self):
        """Test valid guess validation."""
        valid, error = self.rules.validate_guess("APPLE", self.game_state)
        assert valid is True
        assert error == ""
    
    def test_validate_guess_empty(self):
        """Test guess validation with empty word."""
        valid, error = self.rules.validate_guess("", self.game_state)
        assert valid is False
        assert error == "Guess cannot be empty"
    
    def test_validate_guess_not_on_board(self):
        """Test guess validation with word not on board."""
        valid, error = self.rules.validate_guess("NOTHERE", self.game_state)
        assert valid is False
        assert "is not on the board" in error
    
    def test_validate_guess_already_revealed(self):
        """Test guess validation with already revealed word."""
        card = self.game_state.board[0][0]
        card.reveal()
        
        valid, error = self.rules.validate_guess("APPLE", self.game_state)
        assert valid is False
        assert "already been revealed" in error
    
    def test_process_guess_correct_team_word(self):
        """Test processing guess for correct team word."""
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        color, continue_turn, winner = self.rules.process_guess("APPLE", self.game_state)
        
        assert color == CardColor.RED
        assert continue_turn is True
        assert winner is None
        assert self.game_state.red_team.words_remaining == 8
    
    def test_process_guess_wrong_team_word(self):
        """Test processing guess for wrong team word."""
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        color, continue_turn, winner = self.rules.process_guess("BLUEWORD", self.game_state)
        
        assert color == CardColor.BLUE
        assert continue_turn is False
        assert winner is None
    
    def test_process_guess_neutral_word(self):
        """Test processing guess for neutral word."""
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        color, continue_turn, winner = self.rules.process_guess("ELEPHANT", self.game_state)
        
        assert color == CardColor.NEUTRAL
        assert continue_turn is False
        assert winner is None
    
    def test_process_guess_failure_word(self):
        """Test processing guess for failure word."""
        failure_card = Card("FAILURE", CardColor.FAILURE, position=(0, 4))
        self.game_state.board[0][4] = failure_card
        
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        color, continue_turn, winner = self.rules.process_guess("FAILURE", self.game_state)
        
        assert color == CardColor.FAILURE
        assert continue_turn is False
        assert winner == self.game_state.blue_team
    
    def test_process_guess_winning_word(self):
        """Test processing guess that wins the game."""
        self.game_state.red_team.words_remaining = 1
        
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        color, continue_turn, winner = self.rules.process_guess("APPLE", self.game_state)
        
        assert color == CardColor.RED
        assert continue_turn is False
        assert winner == self.game_state.red_team
    
    def test_should_end_turn_failure(self):
        """Test turn ending on failure."""
        should_end = self.rules.should_end_turn(CardColor.FAILURE, self.game_state)
        assert should_end is True
    
    def test_should_end_turn_wrong_color(self):
        """Test turn ending on wrong color."""
        self.game_state.current_team_color = CardColor.RED
        should_end = self.rules.should_end_turn(CardColor.BLUE, self.game_state)
        assert should_end is True
    
    def test_should_end_turn_no_guesses_left(self):
        """Test turn ending when no guesses left."""
        clue = Clue("TEST", 1, CardColor.RED)
        clue.use_guess()
        clue.use_guess()
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        should_end = self.rules.should_end_turn(CardColor.RED, self.game_state)
        assert should_end is True
    
    def test_should_end_turn_continue(self):
        """Test turn continuing with correct color and guesses left."""
        clue = Clue("TEST", 2, CardColor.RED)
        self.game_state.current_clue = clue
        self.game_state.current_team_color = CardColor.RED
        
        should_end = self.rules.should_end_turn(CardColor.RED, self.game_state)
        assert should_end is False
    
    def test_check_game_end_red_wins(self):
        """Test game end check when red team wins."""
        self.game_state.red_team.words_remaining = 0
        winner = self.rules.check_game_end_conditions(self.game_state)
        assert winner == self.game_state.red_team
    
    def test_check_game_end_blue_wins(self):
        """Test game end check when blue team wins."""
        self.game_state.blue_team.words_remaining = 0
        winner = self.rules.check_game_end_conditions(self.game_state)
        assert winner == self.game_state.blue_team
    
    def test_check_game_end_failure_revealed(self):
        """Test game end check when failure card revealed."""
        failure_card = Card("FAILURE", CardColor.FAILURE, revealed=True)
        self.game_state.board[0][4] = failure_card
        self.game_state.current_team_color = CardColor.RED
        
        winner = self.rules.check_game_end_conditions(self.game_state)
        assert winner == self.game_state.blue_team
    
    def test_get_max_clue_number(self):
        """Test getting maximum clue number."""
        max_num = self.rules.get_max_clue_number(CardColor.RED, self.game_state)
        assert max_num == 9
        
        self.game_state.red_team.words_remaining = 3
        max_num = self.rules.get_max_clue_number(CardColor.RED, self.game_state)
        assert max_num == 3
        
        self.game_state.red_team.words_remaining = 0
        max_num = self.rules.get_max_clue_number(CardColor.RED, self.game_state)
        assert max_num == 1
    
    def test_is_valid_team_setup_complete(self):
        """Test valid complete team setup."""
        team = Team(color=CardColor.RED)
        team.add_player(Player("Chief", PlayerRole.CHIEF))
        team.add_player(Player("Detective", PlayerRole.DETECTIVE))
        
        valid, error = self.rules.is_valid_team_setup(team)
        assert valid is True
        assert error == ""
    
    def test_is_valid_team_setup_no_chief(self):
        """Test team setup without Chief."""
        team = Team(color=CardColor.RED)
        team.add_player(Player("Detective", PlayerRole.DETECTIVE))
        
        valid, error = self.rules.is_valid_team_setup(team)
        assert valid is False
        assert error == "Team must have a Chief"
    
    def test_is_valid_team_setup_no_detective(self):
        """Test team setup without Detective."""
        team = Team(color=CardColor.RED)
        team.add_player(Player("Chief", PlayerRole.CHIEF))
        
        valid, error = self.rules.is_valid_team_setup(team)
        assert valid is False
        assert error == "Team must have at least one Detective"
    
    def test_can_start_game_valid(self):
        """Test valid game start conditions."""
        can_start, error = self.rules.can_start_game(self.game_state)
        assert can_start is True
        assert error == ""
    
    def test_can_start_game_no_teams(self):
        """Test game start without teams."""
        game_state = GameState()
        can_start, error = self.rules.can_start_game(game_state)
        assert can_start is False
        assert error == "Both teams must be set up"
