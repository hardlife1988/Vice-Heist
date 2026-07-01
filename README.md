# Vice Heist

A StakeEngine-compatible 5-reel, 3-row video slot game with provably fair math.

## Game Details

- **Type:** 5-Reel, 3-Row Video Slot
- **Paylines:** 20
- **Max Win:** 10,000x bet
- **Target RTP:** 96.0%
- **Features:** Free Games, Wilds, Scatters, Bonus Vault Pick Round
- **Bet Modes:** Base (1x), Bonus Buy (100x)

## Files

| File | Description |
|------|-------------|
| `index.html` | Game frontend |
| `game.js` | Frontend game logic |
| `style.css` | Game styling |
| `math/game_config.py` | Math SDK configuration |
| `math/gamestate.py` | Spin simulation logic |
| `math/run.py` | Math simulation runner |
| `math/reels/BR0.csv` | Base game reel strips |
| `math/reels/FR0.csv` | Free game reel strips |

## Math Configuration

- **Game ID:** vice_heist
- **Provider:** [Pending assignment]
- **Symbols:** Diamond, Gold Bar, Cash Stack, Heist Bag, Vault, A, K, Q, J, Wild, Scatter, Bonus Vault
- **Free Spins:** 3+ scatters trigger 10-20 free games
- **Bonus Round:** 3+ Bonus Vaults trigger pick-and-win bonus
- **Max Win:** 10,000x (1000x top symbol + 10x free game multiplier)

## Setup

### Math Generation (requires Python 3.12+ and Rust/Cargo)

```bash
cd math
python3 run.py

