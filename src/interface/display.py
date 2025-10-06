"""Display components for the terminal interface using Rich."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from typing import List, Dict, Optional
from ..models.card import CardColor
from ..models.team import Team


class GameDisplay:
    """Handles all display rendering using Rich."""
    
    def __init__(self):
        """Initialize game display."""
        self.console = Console()
        self.color_map = {
            "red": "red",
            "blue": "blue",
            "neutral": "yellow",
            "failure": "black on white"
        }
    
    def clear_screen(self) -> None:
        """Clear the console screen."""
        self.console.clear()
    
    def show_title(self) -> None:
        """Display game title."""
        title = Text("WORD DETECTIVE", style="bold magenta", justify="center")
        subtitle = Text("A Strategic Word Guessing Game", style="dim", justify="center")
        
        panel = Panel(
            Align.center(Text.assemble(title, "\n", subtitle)),
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def show_board(self, board_data: List[List[Dict]], show_colors: bool = False) -> None:
        """Display the game board.
        
        Args:
            board_data: 5x5 grid of card data
            show_colors: Whether to show card colors (for Chiefs)
        """
        table = Table(show_header=False, box=None, padding=(0, 2))
        
        for _ in range(5):
            table.add_column(justify="center", width=15)
        
        for row_data in board_data:
            row_items = []
            for card_data in row_data:
                if card_data:
                    word = card_data["word"]
                    revealed = card_data["revealed"]
                    color = card_data.get("color")
                    
                    if revealed and color:
                        style = self.color_map.get(color, "white")
                        text = Text(word, style=f"bold {style}")
                    elif show_colors and color:
                        style = self.color_map.get(color, "white")
                        text = Text(word, style=style)
                    else:
                        text = Text(word, style="white")
                    
                    row_items.append(text)
                else:
                    row_items.append(Text(""))
            
            table.add_row(*row_items)
        
        self.console.print(Panel(table, title="Game Board", border_style="cyan"))
        self.console.print()
    
    def show_game_status(self, board_state: Dict) -> None:
        """Display current game status.
        
        Args:
            board_state: Current game state information
        """
        current_team = board_state["current_team"]
        turn_type = board_state["turn_type"]
        phase = board_state["phase"]
        red_remaining = board_state["red_words_remaining"]
        blue_remaining = board_state["blue_words_remaining"]
        current_clue = board_state.get("current_clue")
        
        team_color = "red" if current_team == "red" else "blue"
        status_text = Text()
        status_text.append(f"Current Team: ", style="white")
        status_text.append(current_team.upper(), style=f"bold {team_color}")
        status_text.append(f"\nPhase: {phase.replace('_', ' ').title()}", style="white")
        
        if current_clue:
            status_text.append(f"\nClue: ", style="white")
            status_text.append(f"{current_clue['word'].upper()} - {current_clue['number']}", style="bold yellow")
            status_text.append(f"\nGuesses Remaining: {current_clue['guesses_remaining']}", style="white")
        
        status_text.append(f"\n\nRed Team: ", style="bold red")
        status_text.append(f"{red_remaining} words left", style="white")
        status_text.append(f"\nBlue Team: ", style="bold blue")
        status_text.append(f"{blue_remaining} words left", style="white")
        
        self.console.print(Panel(status_text, title="Game Status", border_style="green"))
        self.console.print()
    
    def show_team_info(self, team_info: Dict) -> None:
        """Display team information.
        
        Args:
            team_info: Team details including players
        """
        red_team = team_info["red_team"]
        blue_team = team_info["blue_team"]
        
        table = Table(show_header=True, box=None)
        table.add_column("Red Team", style="red", justify="left")
        table.add_column("Blue Team", style="blue", justify="left")
        
        max_players = max(len(red_team["players"]), len(blue_team["players"]))
        
        for i in range(max_players):
            red_player = ""
            if i < len(red_team["players"]):
                p = red_team["players"][i]
                red_player = f"{p['name']} ({p['role'].title()})"
            
            blue_player = ""
            if i < len(blue_team["players"]):
                p = blue_team["players"][i]
                blue_player = f"{p['name']} ({p['role'].title()})"
            
            table.add_row(red_player, blue_player)
        
        self.console.print(Panel(table, title="Teams", border_style="cyan"))
        self.console.print()
    
    def show_message(self, message: str, style: str = "white") -> None:
        """Display a message.
        
        Args:
            message: Message to display
            style: Rich style to apply
        """
        self.console.print(message, style=style)
    
    def show_error(self, error: str) -> None:
        """Display an error message.
        
        Args:
            error: Error message to display
        """
        self.console.print(f"❌ {error}", style="bold red")
    
    def show_success(self, message: str) -> None:
        """Display a success message.
        
        Args:
            message: Success message to display
        """
        self.console.print(f"✅ {message}", style="bold green")
    
    def show_guess_result(self, result: Dict) -> None:
        """Display the result of a guess.
        
        Args:
            result: Guess result information
        """
        word = result["word"]
        color = result["color"]
        
        color_style = self.color_map.get(color, "white")
        
        panel_text = Text()
        panel_text.append(f"Word: ", style="white")
        panel_text.append(word.upper(), style=f"bold {color_style}")
        panel_text.append(f"\nColor: ", style="white")
        panel_text.append(color.upper(), style=f"bold {color_style}")
        
        if result.get("winner"):
            panel_text.append(f"\n\n🎉 ", style="white")
            panel_text.append("GAME OVER!", style="bold yellow")
            winner_color = result["winner"]
            panel_text.append(f"\nWinner: ", style="white")
            panel_text.append(winner_color.upper(), style=f"bold {winner_color}")
        elif result.get("continue_turn"):
            panel_text.append("\n\nCorrect! Continue guessing...", style="bold green")
        else:
            panel_text.append("\n\nTurn ends.", style="bold yellow")
        
        self.console.print(Panel(panel_text, title="Guess Result", border_style="yellow"))
        self.console.print()
    
    def show_winner(self, winner_color: str) -> None:
        """Display winner announcement.
        
        Args:
            winner_color: Color of winning team
        """
        winner_style = "red" if winner_color == "red" else "blue"
        
        title = Text("🎉 GAME OVER 🎉", style="bold yellow", justify="center")
        winner_text = Text(f"{winner_color.upper()} TEAM WINS!", style=f"bold {winner_style}", justify="center")
        
        panel = Panel(
            Align.center(Text.assemble(title, "\n\n", winner_text)),
            border_style=winner_style,
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def show_menu(self, options: List[str]) -> None:
        """Display a menu of options.
        
        Args:
            options: List of menu options
        """
        table = Table(show_header=False, box=None)
        table.add_column("Option", style="cyan")
        table.add_column("Description", style="white")
        
        for i, option in enumerate(options, 1):
            table.add_row(f"{i}.", option)
        
        self.console.print(Panel(table, title="Menu", border_style="cyan"))
        self.console.print()
    
    def show_key_card(self, key_card: List[Dict]) -> None:
        """Display the key card for Chiefs.
        
        Args:
            key_card: List of card information with colors
        """
        table = Table(show_header=False, box=None, padding=(0, 1))
        
        for _ in range(5):
            table.add_column(justify="center", width=15)
        
        for i in range(0, 25, 5):
            row_items = []
            for j in range(5):
                card_info = key_card[i + j]
                word = card_info["word"]
                color = card_info["color"]
                revealed = card_info["revealed"]
                
                style = self.color_map.get(color, "white")
                if revealed:
                    text = Text(f"[{word}]", style=f"bold {style} strike")
                else:
                    text = Text(word, style=style)
                
                row_items.append(text)
            
            table.add_row(*row_items)
        
        self.console.print(Panel(table, title="Key Card (Chiefs Only)", border_style="magenta"))
        self.console.print()
    
    def prompt_continue(self) -> None:
        """Prompt user to press enter to continue."""
        self.console.input("\n[dim]Press Enter to continue...[/dim]")
