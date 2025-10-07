"""Main game interface coordinator."""

from typing import Optional
from .display import GameDisplay
from .input_handler import InputHandler
from ..game.game_controller import GameController
from ..models.card import CardColor


class GameInterface:
    """Coordinates game display and input handling."""
    
    def __init__(self, controller: GameController):
        """Initialize game interface.
        
        Args:
            controller: Game controller instance
        """
        self.controller = controller
        self.display = GameDisplay()
        self.input_handler = InputHandler()
    
    def setup_game(self) -> bool:
        """Run game setup flow.
        
        Returns:
            True if setup successful
        """
        self.display.clear_screen()
        self.display.show_title()
        
        red_players = [("Red Chief", "chief"), ("Red Detective", "detective")]
        blue_players = [("Blue Chief", "chief"), ("Blue Detective", "detective")]
        
        success, error = self.controller.setup_teams(red_players, blue_players)
        if not success:
            self.display.show_error(error)
            return False
        
        starting_team = self.input_handler.get_starting_team()
        success, error = self.controller.start_game(starting_team)
        if not success:
            self.display.show_error(error)
            return False
        
        self.display.show_success("Game setup complete!")
        self.input_handler.wait_for_enter()
        
        return True
    

    
    def run_game_loop(self) -> None:
        """Main game loop."""
        while not self.controller.game_state.game_over:
            self.display.clear_screen()
            self.display.show_title()
            
            board_state = self.controller.get_board_state()
            team_info = self.controller.get_team_info()
            
            current_team = board_state["current_team"]
            turn_type = board_state["turn_type"]
            
            self.display.show_game_status(board_state)
            self.display.show_team_info(team_info)
            
            if turn_type == "chief_clue":
                self._handle_chief_turn(current_team)
            else:
                self._handle_detective_turn(current_team)
            
            winner = self.controller.rules.check_game_end_conditions(self.controller.game_state)
            if winner:
                self.controller.game_state.end_game(winner)
        
        self._show_game_over()
    
    def _handle_chief_turn(self, team_color: str) -> None:
        """Handle Chief's turn.
        
        Args:
            team_color: Current team color
        """
        self.display.show_message(f"\n{team_color.upper()} CHIEF's Turn", style=f"bold {team_color}")
        
        self.display.show_message("\n⚠️  WARNING: The following key card shows ALL colors!", style="bold yellow")
        self.display.show_message("⚠️  Only the CHIEF should see this screen!", style="bold yellow")
        self.input_handler.wait_for_enter()
        
        self.display.clear_screen()
        self.display.show_title()
        
        key_card = self.controller.get_key_card()
        self.display.show_key_card(key_card)
        
        board_state = self.controller.get_board_state()
        self.display.show_board(board_state["board"], show_colors=False)
        
        while True:
            clue_word, number = self.input_handler.get_clue()
            
            success, error = self.controller.give_clue(clue_word, number)
            if success:
                self.display.clear_screen()
                self.display.show_title()
                self.display.show_success(f"Clue given: {clue_word.upper()} - {number}")
                self.input_handler.wait_for_enter()
                break
            else:
                self.display.show_error(error)
    
    def _handle_detective_turn(self, team_color: str) -> None:
        """Handle Detective's turn.
        
        Args:
            team_color: Current team color
        """
        self.display.show_message(f"\n{team_color.upper()} DETECTIVE's Turn", style=f"bold {team_color}")
        
        board_state = self.controller.get_board_state()
        self.display.show_board(board_state["board"], show_colors=False)
        
        current_clue = board_state.get("current_clue")
        if not current_clue or current_clue["guesses_remaining"] <= 0:
            self.controller.end_turn()
            return
        
        available_words = [
            card["word"] for row in board_state["board"] 
            for card in row if card and not card["revealed"]
        ]
        
        should_pass = self.input_handler.confirm_action("Make a guess?")
        if not should_pass:
            self.controller.end_turn()
            self.display.clear_screen()
            self.display.show_title()
            self.display.show_message("Turn passed.", style="yellow")
            self.input_handler.wait_for_enter()
            return
        
        guess = self.input_handler.get_guess(available_words)
        
        success, error, result = self.controller.make_guess(guess)
        if success:
            self.display.clear_screen()
            self.display.show_title()
            self.display.show_guess_result(result)
            self.input_handler.wait_for_enter()
            
            if result.get("winner"):
                return
        else:
            self.display.clear_screen()
            self.display.show_title()
            self.display.show_error(error)
            self.input_handler.wait_for_enter()
    
    def _show_game_over(self) -> None:
        """Display game over screen."""
        self.display.clear_screen()
        self.display.show_title()
        
        key_card = self.controller.get_key_card()
        self.display.show_message("\n🎯 FINAL BOARD - All Cards Revealed:", style="bold yellow")
        self.display.show_key_card(key_card)
        
        winner_color = self.controller.game_state.winner.color.value if self.controller.game_state.winner else None
        if winner_color:
            self.display.show_winner(winner_color)
        
        team_info = self.controller.get_team_info()
        self.display.show_team_info(team_info)
    
    def show_main_menu(self) -> int:
        """Show main menu and get selection.
        
        Returns:
            Selected menu option
        """
        self.display.clear_screen()
        self.display.show_title()
        
        options = [
            "Start New Game",
            "View Rules",
            "Exit"
        ]
        
        self.display.show_menu(options)
        return self.input_handler.get_menu_choice(len(options))
    
    def show_rules(self) -> None:
        """Display game rules."""
        self.display.clear_screen()
        self.display.show_title()
        
        rules_text = """
[bold cyan]OBJECTIVE:[/bold cyan]
Be the first team to identify all your team's secret words on the 5×5 game board.

[bold cyan]SETUP:[/bold cyan]
• Two teams (Red and Blue), each with a Chief and Detectives
• 25 word cards laid out in a 5×5 grid
• Starting team gets 9 words, second team gets 8 words
• 7 neutral words and 1 failure word

[bold cyan]GAMEPLAY:[/bold cyan]

[bold yellow]Chief's Turn:[/bold yellow]
• Give a one-word clue and a number
• The clue relates to one or more of your team's words
• Cannot use words on the board or rhyming words
• Example: "Ocean, 2" (hints at two ocean-related words)

[bold yellow]Detective's Turn:[/bold yellow]
• Guess words one by one
• Can make up to (clue number + 1) guesses
• Turn ends if you guess:
  - A neutral word
  - An opposing team's word
  - The failure word (immediate loss!)
• Continue if you guess your team's word correctly

[bold cyan]WINNING:[/bold cyan]
• Find all your team's words before the other team
• If a team guesses the failure word, they lose immediately

[bold red]Remember:[/bold red] Chiefs can see all colors, Detectives cannot!
        """
        
        self.display.console.print(rules_text)
        self.input_handler.wait_for_enter()
