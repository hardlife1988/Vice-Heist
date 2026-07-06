"""
Vice Heist — RTP Simulation
Runs N provably fair spins and reports actual RTP, feature frequencies, and top wins.
Usage: python simulate.py [num_spins] [bet]
"""

import sys
import os
import json
import time
import secrets
import hashlib

sys.path.insert(0, os.path.dirname(__file__))

from game_config import GameConfig
from reel_engine import ReelEngine
from win_evaluator import WinEvaluator
from stake_engine import generate_server_seed

def run_simulation(num_spins=1_000_000, bet=1.0):
    config    = GameConfig()
    engine    = ReelEngine(config)
    evaluator = WinEvaluator(config)

    server_seed, _ = generate_server_seed()
    client_seed    = secrets.token_hex(16)

    total_wagered  = 0.0
    total_won      = 0.0
    free_spins_rem = 0
    in_free_spins  = False

    scatter_triggers = 0
    bonus_buys       = 0
    spin_types       = {"normal": 0, "free": 0}

    win_buckets = {          # x-bet multiplier buckets
        "0":     0,
        "0-1":   0,
        "1-5":   0,
        "5-10":  0,
        "10-50": 0,
        "50-100":0,
        "100-500":0,
        "500+":  0,
    }
    top_wins = []            # (win_amount, multiplier_x_bet)
    symbol_hit_counts = {}   # symbol -> total hits across paylines

    nonce = 0
    spins_done = 0
    start = time.time()

    print(f"Running {num_spins:,} spins  |  bet={bet}  |  paylines={config.paylines}")
    print("-" * 60)

    while spins_done < num_spins:
        is_free = in_free_spins and free_spins_rem > 0
        multiplier = config.free_spins_multiplier if is_free else 1.0

        cost = 0.0 if is_free else bet
        total_wagered += cost

        grid = engine.spin_reels(server_seed, client_seed, nonce)
        nonce += 1
        spins_done += 1

        result = evaluator.evaluate_spin(grid, bet, multiplier)
        win = min(result["total_win"], bet * config.max_win)
        total_won += win

        spin_types["free" if is_free else "normal"] += 1

        # Track free spin state
        if is_free:
            free_spins_rem -= 1
            if free_spins_rem <= 0:
                in_free_spins = False
        elif result["triggers_free_spins"]:
            scatter_triggers += 1
            free_spins_rem = config.free_spins_count
            in_free_spins  = True

        # Symbol hit counts
        for pw in result["payline_wins"]:
            sym = pw["symbol"]
            symbol_hit_counts[sym] = symbol_hit_counts.get(sym, 0) + 1

        # Win bucket
        x = win / bet if bet else 0
        if x == 0:         win_buckets["0"] += 1
        elif x < 1:        win_buckets["0-1"] += 1
        elif x < 5:        win_buckets["1-5"] += 1
        elif x < 10:       win_buckets["5-10"] += 1
        elif x < 50:       win_buckets["10-50"] += 1
        elif x < 100:      win_buckets["50-100"] += 1
        elif x < 500:      win_buckets["100-500"] += 1
        else:              win_buckets["500+"] += 1

        # Top wins
        if x >= 50:
            top_wins.append((win, x))

        # Progress
        if spins_done % 100_000 == 0:
            elapsed = time.time() - start
            pct = spins_done / num_spins * 100
            rtp_so_far = total_won / total_wagered * 100 if total_wagered else 0
            print(f"  {spins_done:>9,}  ({pct:5.1f}%)  RTP so far: {rtp_so_far:.3f}%  [{elapsed:.1f}s]")

    elapsed = time.time() - start

    # Final stats
    actual_rtp = total_won / total_wagered * 100 if total_wagered else 0
    target_rtp = config.rtp * 100

    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    print(f"  Total spins       : {spins_done:,}  ({spin_types['normal']:,} normal + {spin_types['free']:,} free)")
    print(f"  Total wagered     : {total_wagered:,.2f}")
    print(f"  Total won         : {total_won:,.2f}")
    print(f"  Actual RTP        : {actual_rtp:.4f}%")
    print(f"  Target RTP        : {target_rtp:.2f}%")
    rtp_diff = actual_rtp - target_rtp
    flag = "✅" if abs(rtp_diff) <= 1.0 else "❌ OUT OF TOLERANCE"
    print(f"  Variance          : {rtp_diff:+.4f}%  {flag}")
    print(f"  Free spin triggers: {scatter_triggers:,}  (1 in {spins_done//scatter_triggers if scatter_triggers else 'N/A'})")
    print(f"  Time              : {elapsed:.1f}s  ({spins_done/elapsed:,.0f} spins/sec)")

    print("\nWin distribution (% of all paid spins):")
    paid = spin_types["normal"] or 1
    for k, v in win_buckets.items():
        bar = "█" * int(v / paid * 400)
        print(f"  {k:>8}×  {v:>9,}  ({v/paid*100:6.3f}%)  {bar}")

    print("\nTop symbol hits (payline wins):")
    for sym, cnt in sorted(symbol_hit_counts.items(), key=lambda x: -x[1]):
        print(f"  {sym:<16} {cnt:>9,}")

    top_wins.sort(key=lambda x: -x[1])
    print(f"\nTop 10 individual wins:")
    for win_amt, x_bet in top_wins[:10]:
        print(f"  {win_amt:>12.4f}  ({x_bet:>8.1f}× bet)")

    report = {
        "num_spins": spins_done,
        "normal_spins": spin_types["normal"],
        "free_spins": spin_types["free"],
        "total_wagered": round(total_wagered, 4),
        "total_won": round(total_won, 4),
        "actual_rtp_pct": round(actual_rtp, 4),
        "target_rtp_pct": target_rtp,
        "rtp_variance_pct": round(rtp_diff, 4),
        "within_1pct_tolerance": abs(rtp_diff) <= 1.0,
        "scatter_triggers": scatter_triggers,
        "win_distribution": win_buckets,
        "symbol_hit_counts": symbol_hit_counts,
        "top_10_wins_x_bet": [round(x, 2) for _, x in top_wins[:10]],
        "elapsed_seconds": round(elapsed, 1),
        "spins_per_second": round(spins_done / elapsed),
    }
    out_path = os.path.join(os.path.dirname(__file__), "simulation_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved → {out_path}")
    return report


if __name__ == "__main__":
    n   = int(sys.argv[1])   if len(sys.argv) > 1 else 1_000_000
    bet = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    run_simulation(n, bet)
