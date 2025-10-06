"""Game state model representing the complete state of a game."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
from .card import Card, CardColor
from .team import Team
from .clue import Clue
from .player import Player


class GamePhase(Enum):
    """Represents the current phase of the game."""
    SETUP = "setup"
    CLUE_GIVING = "clue_giving"
    GUESSING = "guessing"
    GAME_OVER = "game_over"


class TurnType(Enum):
    """Represents whose turn it currently is."""
    CHIEF_CLUE = "chief_clue"
    DETECTIVE_GUESS = "detective_guess"


@dataclass
class GameState:
    """Represents the complete state of a Word Detective game.
    
    Attributes:
        board: 5x5 grid of Card objects
        red_team: The red team
        blue_team: The blue team
        current_team_color: Which team's turn it is
        current_clue: The active clue being worked on
        phase: Current phase of the game
        turn_type: What type of action is expected
        game_over: Whether the game has ended
        winner: The winning team (if game is over)
        starting_team_color: Which team started the game
    """
    board: List[List[Card]] = field(default_factory=lambda: [[None for _ in range(5)] for _ in range(5)])
    red_team: Optional[Team] = None
    blue_team: Optional[Team] = None
    current_team_color: CardColor = CardColor.RED
    current_clue: Optional[Clue] = None
    phase: GamePhase = GamePhase.SETUP
    turn_type: TurnType = TurnType.CHIEF_CLUE
    game_over: bool = False
    winner: Optional[Team] = None
    starting_team_color: CardColor = CardColor.RED
    
    def get_current_team(self) -> Team:
        """Get the team whose turn it currently is."""
        if self.current_team_color == CardColor.RED:
            return self.red_team
        return self.blue_team
    
    def get_opposing_team(self) -> Team:
        """Get the team that is not currently active."""
        if self.current_team_color == CardColor.RED:
            return self.blue_team
        return self.red_team
    
    def switch_teams(self) -> None:
        """Switch to the other team's turn."""
        self.current_team_color = (CardColor.BLUE if self.current_team_color == CardColor.RED 
                                 else CardColor.RED)
        self.turn_type = TurnType.CHIEF_CLUE
        self.current_clue = None
    
    def get_card_at_position(self, row: int, col: int) -> Card:
        """Get the card at the specified board position."""
        if not (0 <= row < 5 and 0 <= col < 5):
            raise ValueError("Position must be within 5x5 board bounds")
        return self.board[row][col]
    
    def get_all_cards(self) -> List[Card]:
        """Get all cards on the board as a flat list."""
        cards = []
        for row in self.board:
            for card in row:
                if card is not None:
                    cards.append(card)
        return cards
    
    def get_unrevealed_cards(self) -> List[Card]:
        """Get all cards that haven't been revealed yet."""
        return [card for card in self.get_all_cards() if not card.revealed]
    
    def get_team_cards(self, team_color: CardColor) -> List[Card]:
        """Get all cards belonging to the specified team."""
        return [card for card in self.get_all_cards() 
                if card.color == team_color]
    
    def get_unrevealed_team_cards(self, team_color: CardColor) -> List[Card]:
        """Get unrevealed cards belonging to the specified team."""
        return [card for card in self.get_team_cards(team_color) 
                if not card.revealed]
    
    def is_setup_complete(self) -> bool:
        """Check if game setup is complete and ready to play."""
        return (self.red_team is not None and 
                self.blue_team is not None and
                self.red_team.is_complete_team() and
                self.blue_team.is_complete_team() and
                any(any(card is not None for card in row) for row in self.board))
    
    def start_game(self) -> None:
        """Transition from setup to active gameplay."""
        if not self.is_setup_complete():
            raise ValueError("Cannot start game - setup incomplete")
        self.phase = GamePhase.CLUE_GIVING
        self.turn_type = TurnType.CHIEF_CLUE
    
    def end_game(self, winner: Team) -> None:
        """End the game with the specified winner."""
        self.game_over = True
        self.winner = winner
        self.phase = GamePhase.GAME_OVER
        self.current_clue = None
    
    def check_win_conditions(self) -> Optional[Team]:
        """Check if any team has won and return the winner."""
        if self.red_team and self.red_team.has_won():
            return self.red_team
        if self.blue_team and self.blue_team.has_won():
            return self.blue_team
        return None
