"""
UI Module for Vice-heist slot game.
Provides visualization and interaction layer.
"""

import json
from typing import List, Dict
from paytable import Symbol, Paytable
from reel_engine import ReelEngine
from win_evaluator import WinEvaluator
from gamestate import GameState


class GameUI:
    """User interface for Vice-heist game."""
    
    def __init__(self, config, gamestate):
        """
        Initialize game UI.
        
        Args:
            config: Game configuration
            gamestate: Game state tracker
        """
        self.config = config
        self.gamestate = gamestate
        self.reel_engine = ReelEngine(config)
        self.win_evaluator = WinEvaluator(config)
    
    def display_welcome(self):
        """Display welcome screen."""
        print("\n" + "="*60)
        print("  🎰 VICE-HEIST - 5x3 SLOT GAME 🎰")
        print("="*60 + "\n")
        print(f"  Welcome to {self.config.name}!")
        print(f"  Reels: {self.config.reels}x{self.config.rows}")
        print(f"  Paylines: {self.config.paylines}")
        print(f"  RTP: {self.config.rtp*100:.1f}%")
        print(f"  Max Win: {self.config.max_win}x")
        print(f"  Volatility: {self.config.volatility}\n")
    
    def display_reels(self, reel_grid: List[List[Symbol]]):
        """Display reel result."""
        print("\n  ┌─────────────────────────────┐")
        for row in reel_grid:
            row_display = "  │ "
            for symbol in row:
                row_display += self._symbol_to_display(symbol) + " "
            row_display += "│"
            print(row_display)
        print("  └─────────────────────────────┘\n")
    
    def display_bet_options(self):
        """Display available bet amounts."""
        print("\n  Available Bet Amounts:")
        for i, bet in enumerate(self.config.bet_levels, 1):
            print(f"    {i}. ${bet:.2f}")
    
    def display_spin_result(self, result: Dict):
        """Display spin result with win info."""
        print("\n" + "="*60)
        print("  SPIN RESULT")
        print("="*60)
        
        print(f"\n  Total Win: ${result['total_win']:.2f}")
        print(f"  Scatter Count: {result['scatter_count']}")
        
        if result['wins']:
            print(f"\n  Winning Lines:")
            for win in result['wins']:
                print(f"    Line {win['payline']}: ${win['win']:.2f}")
        
        if result['triggers_free_spins']:
            print(f"\n  🎉 FREE SPINS TRIGGERED! 🎉")
            print(f"  You will receive {self.config.free_spins_count} free spins!")
        
        if result['total_win'] == 0:
            print(f"\n  No wins this spin.")
        
        print("\n" + "-"*60)
    
    def display_game_stats(self):
        """Display current game statistics."""
        print("\n  GAME STATISTICS:")
        print(f"    Total Spins: {self.gamestate.total_spins}")
        print(f"    Total Wagered: ${self.gamestate.total_wagered:.2f}")
        print(f"    Total Won: ${self.gamestate.total_won:.2f}")
        print(f"    Current Balance: ${self.gamestate.current_balance:.2f}")
        
        if self.gamestate.total_spins > 0:
            rtp_actual = self.gamestate.total_won / self.gamestate.total_wagered * 100 if self.gamestate.total_wagered > 0 else 0
            print(f"    Actual RTP: {rtp_actual:.1f}%")
    
    def display_free_spins_info(self):
        """Display free spins information."""
        if self.gamestate.in_free_spins:
            print(f"\n  🎁 FREE SPINS MODE 🎁")
            print(f"    Remaining: {self.gamestate.free_spins_remaining}")
            print(f"    All wins are 2x multiplied!")
    
    @staticmethod
    def _symbol_to_display(symbol: Symbol) -> str:
        """Convert symbol to display character."""
        symbol_display = {
            Symbol.WILD: "🔹",        # Diamond for wild
            Symbol.SCATTER: "📖",      # Book for scatter
            Symbol.BOOK: "📘",         # Book
            Symbol.GOLD_BAR: "🏆",     # Trophy for gold
            Symbol.DIAMOND: "💎",      # Diamond
            Symbol.RUBY: "❤️ ",        # Red heart for ruby
            Symbol.EMERALD: "💚",      # Green heart for emerald
            Symbol.CLUB: "🍀",         # Club
            Symbol.SPADE: "♠️ ",        # Spade
            Symbol.HEART: "♥️ ",        # Heart
        }
        return symbol_display.get(symbol, "❓")
    
    def display_exit(self):
        """Display exit/summary screen."""
        print("\n" + "="*60)
        print("  GAME OVER - THANKS FOR PLAYING!")
        print("="*60 + "\n")
        self.display_game_stats()
        print("\n" + "="*60 + "\n")


class GameSimulator:
    """Simulate game rounds for testing and demonstration."""
    
    def __init__(self, config, gamestate):
        self.config = config
        self.gamestate = gamestate
        self.ui = GameUI(config, gamestate)
        self.reel_engine = ReelEngine(config)
        self.win_evaluator = WinEvaluator(config)
    
    def run_demo(self, num_spins: int = 10, bet_amount: float = 1.0):
        """
        Run demonstration game.
        
        Args:
            num_spins: Number of spins to simulate
            bet_amount: Bet per spin
        """
        self.ui.display_welcome()
        
        for spin_num in range(1, num_spins + 1):
            print(f"\n🎯 SPIN {spin_num}/{num_spins}")
            
            # Start spin
            self.gamestate.start_spin(bet_amount)
            
            # Spin reels
            reel_grid = self.reel_engine.spin_reels()
            self.ui.display_reels(reel_grid)
            
            # Evaluate wins
            multiplier = 2.0 if self.gamestate.in_free_spins else 1.0
            result = self.win_evaluator.evaluate_spin(reel_grid, bet_amount, multiplier)
            
            # End spin
            self.gamestate.end_spin(result['total_win'])
            
            # Display result
            self.ui.display_spin_result(result)
            
            # Handle features
            if result['triggers_free_spins']:
                self.gamestate.trigger_free_spins(self.config.free_spins_count)
            elif self.gamestate.in_free_spins:
                self.gamestate.use_free_spin()
            
            self.ui.display_free_spins_info()
        
        self.ui.display_exit()


def create_game_session(config) -> GameUI:
    """
    Create a new game session.
    
    Args:
        config: Game configuration
        
    Returns:
        GameUI: Game interface
    """
    gamestate = GameState(config)
    return GameUI(config, gamestate)
