"""Main entry point for Word Detective game."""

import sys
from .game.game_controller import GameController
from .interface.game_interface import GameInterface


def main():
    """Main game entry point."""
    controller = GameController()
    interface = GameInterface(controller)
    
    while True:
        choice = interface.show_main_menu()
        
        if choice == 1:
            interface.controller.reset_game()
            if interface.setup_game():
                interface.run_game_loop()
                interface.input_handler.wait_for_enter()
        elif choice == 2:
            interface.show_rules()
        elif choice == 3:
            interface.display.show_message("\nThanks for playing Word Detective!", style="bold cyan")
            sys.exit(0)
        else:
            interface.display.show_error("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        sys.exit(1)
