"""
Books module for Vice-heist slot game.
Manages the Book symbol which acts as both wild and scatter.
"""


def create_books(gamestate, config, num_sim_args, batching_size, num_threads, compression, profiling):
    """
    Initialize and process book symbols for the slot game.
    
    The book symbol is special:
    - Acts as WILD (substitutes for other symbols)
    - Acts as SCATTER (triggers free spins when 3+ land)
    - Appears on all reels
    
    Args:
        gamestate: Current game state object
        config: Game configuration object
        num_sim_args: Number of simulation arguments
        batching_size: Size of batches for processing
        num_threads: Number of threads for parallel processing
        compression: Whether to compress output
        profiling: Whether to enable profiling
        
    Returns:
        dict: Book symbol configuration and state
    """
    books_config = {
        "symbol": "BOOK",
        "type": ["WILD", "SCATTER"],
        "scatter_trigger": 3,  # 3+ books trigger free spins
        "free_spins_awarded": 10,
        "appears_on_reels": [0, 1, 2, 3, 4],  # All 5 reels
        "substitution_value": "HIGH",  # Substitutes for any symbol
    }
    
    # Process with given parameters
    processed_books = {
        "config": books_config,
        "gamestate": gamestate,
        "batching_size": batching_size,
        "num_threads": num_threads,
        "compression": compression,
        "profiling": profiling,
    }
    
    return processed_books
