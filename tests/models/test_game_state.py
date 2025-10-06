"""Tests for the GameState model."""

import pytest
from src.models.game_state import GameState, GamePhase, TurnType
from src.models.team import Team
from src.models.player import Player, PlayerRole
from src.models.card import Card, CardColor
from src.models.clue import Clue


class TestGameState:
    """Test cases for GameState dataclass."""
    
    def test_game_state_creation(self):
        """Test basic game state creation."""
        game_state = GameState()
        
        assert len(game_state.board) == 5
        assert all(len(row) == 5 for row in game_state.board)
        assert game_state.red_team is None
        assert game_state.blue_team is None
        assert game_state.current_team_color == CardColor.RED
        assert game_state.current_clue is None
        assert game_state.phase == GamePhase.SETUP
        assert game_state.turn_type == TurnType.CHIEF_CLUE
        assert game_state.game_over is False
        assert game_state.winner is None
    
    def test_setup_teams(self):
        """Test setting up teams in game state."""
        game_state = GameState()
        
        red_team = Team(color=CardColor.RED)
        blue_team = Team(color=CardColor.BLUE)
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        
        assert game_state.red_team == red_team
        assert game_state.blue_team == blue_team
    
    def test_get_current_team(self):
        """Test getting current team."""
        game_state = GameState()
        red_team = Team(color=CardColor.RED)
        blue_team = Team(color=CardColor.BLUE)
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        
        game_state.current_team_color = CardColor.RED
        assert game_state.get_current_team() == red_team
        
        game_state.current_team_color = CardColor.BLUE
        assert game_state.get_current_team() == blue_team
    
    def test_get_opposing_team(self):
        """Test getting opposing team."""
        game_state = GameState()
        red_team = Team(color=CardColor.RED)
        blue_team = Team(color=CardColor.BLUE)
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        
        game_state.current_team_color = CardColor.RED
        assert game_state.get_opposing_team() == blue_team
        
        game_state.current_team_color = CardColor.BLUE
        assert game_state.get_opposing_team() == red_team
    
    def test_switch_teams(self):
        """Test switching between teams."""
        game_state = GameState()
        game_state.current_team_color = CardColor.RED
        game_state.turn_type = TurnType.DETECTIVE_GUESS
        game_state.current_clue = Clue(word="TEST", number=1, team_color=CardColor.RED)
        
        game_state.switch_teams()
        
        assert game_state.current_team_color == CardColor.BLUE
        assert game_state.turn_type == TurnType.CHIEF_CLUE
        assert game_state.current_clue is None
        
        game_state.switch_teams()
        assert game_state.current_team_color == CardColor.RED
    
    def test_board_position_access(self):
        """Test accessing board positions."""
        game_state = GameState()
        card = Card(word="TEST", color=CardColor.RED)
        game_state.board[2][3] = card
        
        retrieved_card = game_state.get_card_at_position(2, 3)
        assert retrieved_card == card
    
    def test_board_position_bounds_checking(self):
        """Test board position bounds checking."""
        game_state = GameState()
        
        with pytest.raises(ValueError, match="Position must be within 5x5 board bounds"):
            game_state.get_card_at_position(-1, 0)
        
        with pytest.raises(ValueError, match="Position must be within 5x5 board bounds"):
            game_state.get_card_at_position(0, 5)
        
        with pytest.raises(ValueError, match="Position must be within 5x5 board bounds"):
            game_state.get_card_at_position(5, 0)
    
    def test_get_all_cards(self):
        """Test getting all cards from board."""
        game_state = GameState()
        
        cards = []
        for i in range(5):
            for j in range(5):
                card = Card(word=f"CARD_{i}_{j}", color=CardColor.RED)
                game_state.board[i][j] = card
                cards.append(card)
        
        all_cards = game_state.get_all_cards()
        assert len(all_cards) == 25
        assert all(card in cards for card in all_cards)
    
    def test_get_unrevealed_cards(self):
        """Test getting unrevealed cards."""
        game_state = GameState()
        
        revealed_card = Card(word="REVEALED", color=CardColor.RED, revealed=True)
        unrevealed_card1 = Card(word="HIDDEN1", color=CardColor.BLUE)
        unrevealed_card2 = Card(word="HIDDEN2", color=CardColor.NEUTRAL)
        
        game_state.board[0][0] = revealed_card
        game_state.board[0][1] = unrevealed_card1
        game_state.board[0][2] = unrevealed_card2
        
        unrevealed = game_state.get_unrevealed_cards()
        assert len(unrevealed) == 2
        assert unrevealed_card1 in unrevealed
        assert unrevealed_card2 in unrevealed
        assert revealed_card not in unrevealed
    
    def test_get_team_cards(self):
        """Test getting cards for specific team."""
        game_state = GameState()
        
        red_card1 = Card(word="RED1", color=CardColor.RED)
        red_card2 = Card(word="RED2", color=CardColor.RED)
        blue_card = Card(word="BLUE1", color=CardColor.BLUE)
        neutral_card = Card(word="NEUTRAL", color=CardColor.NEUTRAL)
        
        game_state.board[0][0] = red_card1
        game_state.board[0][1] = red_card2
        game_state.board[0][2] = blue_card
        game_state.board[0][3] = neutral_card
        
        red_cards = game_state.get_team_cards(CardColor.RED)
        blue_cards = game_state.get_team_cards(CardColor.BLUE)
        
        assert len(red_cards) == 2
        assert red_card1 in red_cards
        assert red_card2 in red_cards
        
        assert len(blue_cards) == 1
        assert blue_card in blue_cards
    
    def test_is_setup_complete(self):
        """Test checking if setup is complete."""
        game_state = GameState()
        assert game_state.is_setup_complete() is False
        
        red_team = Team(color=CardColor.RED)
        red_team.add_player(Player(name="Red Chief", role=PlayerRole.CHIEF))
        red_team.add_player(Player(name="Red Detective", role=PlayerRole.DETECTIVE))
        
        blue_team = Team(color=CardColor.BLUE)
        blue_team.add_player(Player(name="Blue Chief", role=PlayerRole.CHIEF))
        blue_team.add_player(Player(name="Blue Detective", role=PlayerRole.DETECTIVE))
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        assert game_state.is_setup_complete() is False
        
        game_state.board[0][0] = Card(word="TEST", color=CardColor.RED)
        assert game_state.is_setup_complete() is True
    
    def test_start_game(self):
        """Test starting the game."""
        game_state = GameState()
        
        with pytest.raises(ValueError, match="Cannot start game - setup incomplete"):
            game_state.start_game()
        
        red_team = Team(color=CardColor.RED)
        red_team.add_player(Player(name="Red Chief", role=PlayerRole.CHIEF))
        red_team.add_player(Player(name="Red Detective", role=PlayerRole.DETECTIVE))
        
        blue_team = Team(color=CardColor.BLUE)
        blue_team.add_player(Player(name="Blue Chief", role=PlayerRole.CHIEF))
        blue_team.add_player(Player(name="Blue Detective", role=PlayerRole.DETECTIVE))
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        game_state.board[0][0] = Card(word="TEST", color=CardColor.RED)
        
        game_state.start_game()
        assert game_state.phase == GamePhase.CLUE_GIVING
        assert game_state.turn_type == TurnType.CHIEF_CLUE
    
    def test_end_game(self):
        """Test ending the game."""
        game_state = GameState()
        red_team = Team(color=CardColor.RED)
        
        assert game_state.game_over is False
        assert game_state.winner is None
        
        game_state.end_game(red_team)
        
        assert game_state.game_over is True
        assert game_state.winner == red_team
        assert game_state.phase == GamePhase.GAME_OVER
        assert game_state.current_clue is None
    
    def test_check_win_conditions(self):
        """Test checking win conditions."""
        game_state = GameState()
        
        red_team = Team(color=CardColor.RED)
        blue_team = Team(color=CardColor.BLUE)
        
        red_team.set_word_count(2)
        blue_team.set_word_count(3)
        
        game_state.red_team = red_team
        game_state.blue_team = blue_team
        
        assert game_state.check_win_conditions() is None
        
        red_team.word_found()
        red_team.word_found()
        
        winner = game_state.check_win_conditions()
        assert winner == red_team
        
        blue_team.word_found()
        blue_team.word_found()
        blue_team.word_found()
        
        winner = game_state.check_win_conditions()
        assert winner == red_team
