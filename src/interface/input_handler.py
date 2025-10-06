"""Input handling for the terminal interface."""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from typing import Tuple, Optional, List


class InputHandler:
    """Handles all user input processing."""
    
    def __init__(self):
        """Initialize input handler."""
        self.console = Console()
    
    def get_player_name(self, role: str, team: str) -> str:
        """Get player name from user.
        
        Args:
            role: Player role (Chief/Detective)
            team: Team color
            
        Returns:
            Player name
        """
        prompt_text = f"Enter {team} team {role} name"
        return Prompt.ask(prompt_text).strip()
    
    def get_team_size(self, team: str) -> int:
        """Get number of detectives for a team.
        
        Args:
            team: Team color
            
        Returns:
            Number of detectives
        """
        while True:
            try:
                size = Prompt.ask(f"How many detectives for {team} team", default="1")
                num = int(size)
                if num < 1:
                    self.console.print("Must have at least 1 detective", style="red")
                    continue
                if num > 10:
                    self.console.print("Maximum 10 detectives per team", style="red")
                    continue
                return num
            except ValueError:
                self.console.print("Please enter a valid number", style="red")
    
    def get_starting_team(self) -> Optional[str]:
        """Get which team should start.
        
        Returns:
            Team color or None for random
        """
        choice = Prompt.ask(
            "Which team starts",
            choices=["red", "blue", "random"],
            default="random"
        )
        return None if choice == "random" else choice
    
    def get_clue(self) -> Tuple[str, int]:
        """Get clue word and number from user.
        
        Returns:
            Tuple of (clue_word, number)
        """
        while True:
            clue_word = Prompt.ask("Enter your clue word").strip()
            if not clue_word:
                self.console.print("Clue cannot be empty", style="red")
                continue
            
            try:
                number = int(Prompt.ask("Enter the number"))
                if number < 1:
                    self.console.print("Number must be at least 1", style="red")
                    continue
                return clue_word, number
            except ValueError:
                self.console.print("Please enter a valid number", style="red")
    
    def get_guess(self, available_words: List[str]) -> str:
        """Get word guess from user.
        
        Args:
            available_words: List of unrevealed words
            
        Returns:
            Guessed word
        """
        while True:
            guess = Prompt.ask("Enter your guess").strip()
            if not guess:
                self.console.print("Guess cannot be empty", style="red")
                continue
            
            normalized_guess = guess.lower()
            normalized_available = [w.lower() for w in available_words]
            
            if normalized_guess not in normalized_available:
                self.console.print(f"'{guess}' is not available", style="red")
                continue
            
            return guess
    
    def get_menu_choice(self, num_options: int) -> int:
        """Get menu choice from user.
        
        Args:
            num_options: Number of menu options
            
        Returns:
            Selected option number
        """
        while True:
            try:
                choice = Prompt.ask("Select an option")
                num = int(choice)
                if 1 <= num <= num_options:
                    return num
                self.console.print(f"Please enter a number between 1 and {num_options}", style="red")
            except ValueError:
                self.console.print("Please enter a valid number", style="red")
    
    def confirm_action(self, prompt: str) -> bool:
        """Get confirmation from user.
        
        Args:
            prompt: Confirmation prompt
            
        Returns:
            True if confirmed
        """
        return Confirm.ask(prompt)
    
    def get_word_from_list(self, words: List[str], prompt: str = "Select a word") -> str:
        """Let user select a word from a list.
        
        Args:
            words: List of words to choose from
            prompt: Prompt message
            
        Returns:
            Selected word
        """
        self.console.print(f"\n[cyan]{prompt}:[/cyan]")
        for i, word in enumerate(words, 1):
            self.console.print(f"  {i}. {word}")
        
        while True:
            try:
                choice = Prompt.ask("Enter number")
                num = int(choice)
                if 1 <= num <= len(words):
                    return words[num - 1]
                self.console.print(f"Please enter a number between 1 and {len(words)}", style="red")
            except ValueError:
                self.console.print("Please enter a valid number", style="red")
    
    def get_text_input(self, prompt: str, default: str = None) -> str:
        """Get text input from user.
        
        Args:
            prompt: Input prompt
            default: Default value
            
        Returns:
            User input
        """
        if default:
            return Prompt.ask(prompt, default=default).strip()
        return Prompt.ask(prompt).strip()
    
    def wait_for_enter(self) -> None:
        """Wait for user to press enter."""
        self.console.input("\n[dim]Press Enter to continue...[/dim]")
