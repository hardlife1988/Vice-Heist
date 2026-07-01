"""
GameState class for Vice-heist slot game.
Manages the current state of the game during simulation.
"""


class GameState:
    """
    Tracks the state of the game during play.
    """
    
    def __init__(self, config=None):
        self.config = config
        self.current_spin = 0
        self.total_spins = 0
        self.current_balance = 0.0
        self.total_wagered = 0.0
        self.total_won = 0.0
        self.in_free_spins = False
        self.free_spins_remaining = 0
        self.in_bonus_vault = False
        self.last_reel_result = None
        self.last_win = 0.0
        self.history = []
        
    def start_spin(self, bet_amount):
        """
        Start a new spin.
        
        Args:
            bet_amount: Amount wagered on this spin
        """
        self.current_spin += 1
        self.total_spins += 1
        self.total_wagered += bet_amount
        self.current_balance -= bet_amount
        
    def end_spin(self, win_amount):
        """
        End the current spin with a win amount.
        
        Args:
            win_amount: Amount won on this spin
        """
        self.last_win = win_amount
        self.total_won += win_amount
        self.current_balance += win_amount
        
    def trigger_free_spins(self, count=10):
        """
        Trigger free spins feature.
        
        Args:
            count: Number of free spins to award
        """
        self.in_free_spins = True
        self.free_spins_remaining = count
        
    def use_free_spin(self):
        """
        Use one free spin.
        """
        if self.free_spins_remaining > 0:
            self.free_spins_remaining -= 1
            if self.free_spins_remaining == 0:
                self.in_free_spins = False
