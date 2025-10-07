"""Game rules engine and validation."""

from typing import List, Tuple, Optional
from ..models.card import Card, CardColor
from ..models.clue import Clue
from ..models.team import Team
from ..models.game_state import GameState, TurnType
from ..utils.word_validator import WordValidator


class GameRules:
    """Enforces game rules and validates actions."""
    
    def __init__(self):
        """Initialize game rules engine."""
        self.word_validator = WordValidator()
    
    def validate_clue(self, clue_word: str, number: int, game_state: GameState) -> Tuple[bool, str]:
        """Validate a clue according to game rules.
        
        Args:
            clue_word: The clue word
            number: Number of words the clue relates to
            game_state: Current game state
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if number < 1:
            return False, "Clue number must be at least 1"
        
        if number > 25:
            return False, "Clue number cannot exceed 25"
        
        board_words = [card.word for card in game_state.get_all_cards()]
        return self.word_validator.is_valid_clue_word(clue_word, board_words)
    
    def can_give_clue(self, game_state: GameState) -> Tuple[bool, str]:
        """Check if current team can give a clue.
        
        Args:
            game_state: Current game state
            
        Returns:
            Tuple of (can_give_clue, reason_if_not)
        """
        if game_state.game_over:
            return False, "Game is over"
        
        if game_state.turn_type != TurnType.CHIEF_CLUE:
            return False, "Not clue-giving phase"
        
        current_team = game_state.get_current_team()
        if not current_team.has_chief():
            return False, "Team has no Chief"
        
        return True, ""
    
    def can_make_guess(self, game_state: GameState) -> Tuple[bool, str]:
        """Check if current team can make a guess.
        
        Args:
            game_state: Current game state
            
        Returns:
            Tuple of (can_guess, reason_if_not)
        """
        if game_state.game_over:
            return False, "Game is over"
        
        if game_state.turn_type != TurnType.DETECTIVE_GUESS:
            return False, "Not guessing phase"
        
        if not game_state.current_clue:
            return False, "No active clue"
        
        if not game_state.current_clue.has_guesses_left():
            return False, "No guesses remaining for current clue"
        
        current_team = game_state.get_current_team()
        if not current_team.has_detectives():
            return False, "Team has no Detectives"
        
        return True, ""
    
    def validate_guess(self, word: str, game_state: GameState) -> Tuple[bool, str]:
        """Validate a word guess.
        
        Args:
            word: Word being guessed
            game_state: Current game state
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not word or not word.strip():
            return False, "Guess cannot be empty"
        
        try:
            card = next(card for card in game_state.get_all_cards() 
                       if card.word.lower() == word.lower())
        except StopIteration:
            return False, f"Word '{word}' is not on the board"
        
        if card.revealed:
            return False, f"Word '{word}' has already been revealed"
        
        return True, ""
    
    def process_guess(self, word: str, game_state: GameState) -> Tuple[CardColor, bool, Optional[Team]]:
        """Process a guess and determine the outcome.
        
        Args:
            word: Word being guessed
            game_state: Current game state
            
        Returns:
            Tuple of (card_color, continue_turn, winner)
        """
        card = next(card for card in game_state.get_all_cards() 
                   if card.word.lower() == word.lower())
        
        revealed_color = card.reveal()
        game_state.current_clue.use_guess()
        
        current_team = game_state.get_current_team()
        current_team_color = game_state.current_team_color
        
        if revealed_color == CardColor.FAILURE:
            opposing_team = game_state.get_opposing_team()
            return revealed_color, False, opposing_team
        
        if revealed_color == CardColor.RED:
            game_state.red_team.word_found()
            if game_state.red_team.has_won():
                return revealed_color, False, game_state.red_team
        elif revealed_color == CardColor.BLUE:
            game_state.blue_team.word_found()
            if game_state.blue_team.has_won():
                return revealed_color, False, game_state.blue_team
        
        if revealed_color == current_team_color:
            if game_state.current_clue.has_guesses_left():
                return revealed_color, True, None
            else:
                return revealed_color, False, None
        
        return revealed_color, False, None
    
    def should_end_turn(self, revealed_color: CardColor, game_state: GameState) -> bool:
        """Determine if the turn should end after a guess.
        
        Args:
            revealed_color: Color of the revealed card
            game_state: Current game state
            
        Returns:
            True if turn should end
        """
        current_team_color = game_state.current_team_color
        
        if revealed_color == CardColor.FAILURE:
            return True
        
        if revealed_color != current_team_color:
            return True
        
        if not game_state.current_clue.has_guesses_left():
            return True
        
        return False
    
    def check_game_end_conditions(self, game_state: GameState) -> Optional[Team]:
        """Check if the game should end.
        
        Args:
            game_state: Current game state
            
        Returns:
            Winning team or None if game continues
        """
        if game_state.red_team.has_won():
            return game_state.red_team
        
        if game_state.blue_team.has_won():
            return game_state.blue_team
        
        failure_cards = [card for card in game_state.get_all_cards() 
                        if card.color == CardColor.FAILURE and card.revealed]
        
        if failure_cards:
            return game_state.get_opposing_team()
        
        return None
    
    def get_max_clue_number(self, team_color: CardColor, game_state: GameState) -> int:
        """Get maximum valid clue number for a team.
        
        Args:
            team_color: Color of the team
            game_state: Current game state
            
        Returns:
            Maximum clue number allowed
        """
        if team_color == CardColor.RED:
            return max(1, game_state.red_team.words_remaining)
        elif team_color == CardColor.BLUE:
            return max(1, game_state.blue_team.words_remaining)
        else:
            return 1
    
    def is_valid_team_setup(self, team: Team) -> Tuple[bool, str]:
        """Validate team setup.
        
        Args:
            team: Team to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not team.has_chief():
            return False, "Team must have a Chief"
        
        if not team.has_detectives():
            return False, "Team must have at least one Detective"
        
        return True, ""
    
    def can_start_game(self, game_state: GameState) -> Tuple[bool, str]:
        """Check if game can be started.
        
        Args:
            game_state: Current game state
            
        Returns:
            Tuple of (can_start, reason_if_not)
        """
        if not game_state.red_team or not game_state.blue_team:
            return False, "Both teams must be set up"
        
        red_valid, red_error = self.is_valid_team_setup(game_state.red_team)
        if not red_valid:
            return False, f"Red team: {red_error}"
        
        blue_valid, blue_error = self.is_valid_team_setup(game_state.blue_team)
        if not blue_valid:
            return False, f"Blue team: {blue_error}"
        

        
        return True, ""
