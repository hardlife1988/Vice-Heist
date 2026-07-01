"""
GameConfig class for Vice-heist slot game.
Defines game configuration structure and parameters.
"""


class GameConfig:
    """
    Game configuration class for Vice-heist.
    """
    
    def __init__(self):
        self.name = "Vice-heist"
        self.reels = 5
        self.rows = 3
        self.paylines = 10
        self.max_bet = 10.00
        self.min_bet = 0.10
        self.rtp = 0.965
        self.volatility = "HIGH"
        self.max_win = 10000
        self.free_spins_trigger = 3  # Book scatter
        self.free_spins_count = 10
        self.bonus_vault_available = True
        
    def to_dict(self):
        return {
            "name": self.name,
            "reels": self.reels,
            "rows": self.rows,
            "paylines": self.paylines,
            "max_bet": self.max_bet,
            "min_bet": self.min_bet,
            "rtp": self.rtp,
            "volatility": self.volatility,
            "max_win": self.max_win,
            "free_spins_trigger": self.free_spins_trigger,
            "free_spins_count": self.free_spins_count,
            "bonus_vault_available": self.bonus_vault_available,
        }
