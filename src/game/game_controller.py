"""Main game controller managing game flow and state."""

import random
from typing import List, Tuple, Optional
from ..models.card import CardColor
from ..models.clue import Clue
from ..models.team import Team
from ..models.player import Player, PlayerRole
from ..models.game_state import GameState, GamePhase, TurnType
from .board import GameBoard
from .rules import GameRules
from ..utils.word_loader import WordLoader


class GameController:
    """Controls game flow and manages state transitions."""
    
    def __init__(self, word_loader: WordLoader = None):
        """Initialize game controller.
        
        Args:
            word_loader: Word loader for board generation
        """
        self.word_loader = word_loader or WordLoader()
        self.board = GameBoard(self.word_loader)
        self.rules = GameRules()
        self.game_state = GameState()
    
    def setup_teams(self, red_players: list, blue_players: list) -> Tuple[bool, str]:
        """Set up teams with players.
        
        Args:
            red_players: List of (name, role) tuples for red team
            blue_players: List of (name, role) tuples for blue team
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            red_team = Team(color=CardColor.RED)
            for name, role in red_players:
                player = Player(name=name, role=PlayerRole(role))
                red_team.add_player(player)
            
            blue_team = Team(color=CardColor.BLUE)
            for name, role in blue_players:
                player = Player(name=name, role=PlayerRole(role))
                blue_team.add_player(player)
            
            red_valid, red_error = self.rules.is_valid_team_setup(red_team)
            if not red_valid:
                return False, f"Red team: {red_error}"
            
            blue_valid, blue_error = self.rules.is_valid_team_setup(blue_team)
            if not blue_valid:
                return False, f"Blue team: {blue_error}"
            
            self.game_state.red_team = red_team
            self.game_state.blue_team = blue_team
            
            return True, ""
            
        except Exception as e:
            return False, str(e)
    
    def start_game(self, starting_team: str = None) -> Tuple[bool, str]:
        """Start a new game.
        
        Args:
            starting_team: "red" or "blue", random if None
            
        Returns:
            Tuple of (success, error_message)
        """
        can_start, error = self.rules.can_start_game(self.game_state)
        if not can_start:
            return False, error
        
        if starting_team:
            if starting_team.lower() == "red":
                start_color = CardColor.RED
            elif starting_team.lower() == "blue":
                start_color = CardColor.BLUE
            else:
                return False, "Starting team must be 'red' or 'blue'"
        else:
            start_color = random.choice([CardColor.RED, CardColor.BLUE])
        
        try:
            self.board.generate_board(start_color)
            
            for card in self.board.cards:
                row, col = card.position
                self.game_state.board[row][col] = card
            
            self.game_state.starting_team_color = start_color
            self.game_state.current_team_color = start_color
            
            starting_words = 9
            second_words = 8
            
            if start_color == CardColor.RED:
                self.game_state.red_team.set_word_count(starting_words)
                self.game_state.blue_team.set_word_count(second_words)
            else:
                self.game_state.blue_team.set_word_count(starting_words)
                self.game_state.red_team.set_word_count(second_words)
            
            self.game_state.start_game()
            
            return True, ""
            
        except Exception as e:
            return False, str(e)
    
    def give_clue(self, clue_word: str, number: int) -> Tuple[bool, str]:
        """Give a clue to the team.
        
        Args:
            clue_word: The clue word
            number: Number of words the clue relates to
            
        Returns:
            Tuple of (success, error_message)
        """
        can_give, error = self.rules.can_give_clue(self.game_state)
        if not can_give:
            return False, error
        
        valid_clue, clue_error = self.rules.validate_clue(
            clue_word, number, self.game_state
        )
        if not valid_clue:
            return False, clue_error
        
        max_number = self.rules.get_max_clue_number(
            self.game_state.current_team_color, self.game_state
        )
        if number > max_number:
            return False, f"Clue number cannot exceed {max_number} (remaining team words)"
        
        clue = Clue(
            word=clue_word,
            number=number,
            team_color=self.game_state.current_team_color
        )
        
        self.game_state.current_clue = clue
        self.game_state.turn_type = TurnType.DETECTIVE_GUESS
        self.game_state.phase = GamePhase.GUESSING
        
        return True, ""
    
    def make_guess(self, word: str) -> Tuple[bool, str, dict]:
        """Make a guess for a word.
        
        Args:
            word: Word being guessed
            
        Returns:
            Tuple of (success, error_message, result_info)
        """
        can_guess, error = self.rules.can_make_guess(self.game_state)
        if not can_guess:
            return False, error, {}
        
        valid_guess, guess_error = self.rules.validate_guess(word, self.game_state)
        if not valid_guess:
            return False, guess_error, {}
        
        revealed_color, continue_turn, winner = self.rules.process_guess(
            word, self.game_state
        )
        
        result_info = {
            "word": word,
            "color": revealed_color.value,
            "continue_turn": continue_turn,
            "winner": winner.color.value if winner else None,
            "guesses_remaining": self.game_state.current_clue.guesses_remaining
        }
        
        if winner:
            self.game_state.end_game(winner)
            return True, "", result_info
        
        should_end = self.rules.should_end_turn(revealed_color, self.game_state)
        if should_end or not continue_turn:
            self.end_turn()
        
        return True, "", result_info
    
    def end_turn(self) -> None:
        """End current turn and switch to other team."""
        self.game_state.switch_teams()
        self.game_state.phase = GamePhase.CLUE_GIVING
    
    def get_board_state(self) -> dict:
        """Get current board state for display.
        
        Returns:
            Dict with board information
        """
        board_data = []
        for row in range(5):
            row_data = []
            for col in range(5):
                card = self.game_state.get_card_at_position(row, col)
                if card:
                    card_data = {
                        "word": card.word,
                        "revealed": card.revealed,
                        "color": card.color.value if card.revealed else None,
                        "position": (row, col)
                    }
                    row_data.append(card_data)
                else:
                    row_data.append(None)
            board_data.append(row_data)
        
        return {
            "board": board_data,
            "current_team": self.game_state.current_team_color.value,
            "turn_type": self.game_state.turn_type.value,
            "phase": self.game_state.phase.value,
            "current_clue": {
                "word": self.game_state.current_clue.word,
                "number": self.game_state.current_clue.number,
                "guesses_remaining": self.game_state.current_clue.guesses_remaining
            } if self.game_state.current_clue else None,
            "red_words_remaining": self.game_state.red_team.words_remaining,
            "blue_words_remaining": self.game_state.blue_team.words_remaining,
            "game_over": self.game_state.game_over,
            "winner": self.game_state.winner.color.value if self.game_state.winner else None
        }
    
    def get_key_card(self) -> List[dict]:
        """Get the key card for Chiefs (shows all colors).
        
        Returns:
            List of card info with colors revealed
        """
        key_data = []
        for card in self.board.cards:
            row, col = card.position
            card_info = {
                "word": card.word,
                "color": card.color.value,
                "revealed": card.revealed,
                "position": (row, col)
            }
            key_data.append(card_info)
        
        return key_data
    
    def get_team_info(self) -> dict:
        """Get team information.
        
        Returns:
            Dict with team details
        """
        red_team = self.game_state.red_team
        blue_team = self.game_state.blue_team
        
        return {
            "red_team": {
                "players": [{"name": p.name, "role": p.role.value} for p in red_team.players],
                "words_remaining": red_team.words_remaining,
                "total_words": red_team.total_words
            },
            "blue_team": {
                "players": [{"name": p.name, "role": p.role.value} for p in blue_team.players],
                "words_remaining": blue_team.words_remaining,
                "total_words": blue_team.total_words
            }
        }
    
    def reset_game(self) -> None:
        """Reset game to initial state."""
        self.game_state = GameState()
        self.board = GameBoard(self.word_loader)
        self.rules = GameRules()
