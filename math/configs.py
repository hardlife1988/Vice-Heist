"""
Configs module for Vice-heist slot game.
Handles game configuration generation and management.
"""


def generate_configs(gamestate):
    """
    Generate game configurations based on gamestate.
    
    Args:
        gamestate: Current game state object
        
    Returns:
        dict: Generated configuration settings
    """
    configs = {
        "rtp": 96.5,
        "volatility": "HIGH",
        "base_game_rtp": 94.0,
        "feature_rtp": 2.5,
        "bet_levels": [0.10, 0.50, 1.00, 5.00, 10.00],
        "max_win": 10000,
    }
    return configs
