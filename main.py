#!/usr/bin/env python3
"""
The Shepherd King — entry point.

Usage:
  python main.py              # full campaign, all 7 levels
  python main.py --level 4   # start at a specific level
  python main.py --levels 2  # play only 2 levels
"""

import argparse
from src.game import Game


def main():
    parser = argparse.ArgumentParser(description="The Shepherd King — a game of David's life")
    parser.add_argument("--level",  type=int, default=1,    help="Starting level (1-7)")
    parser.add_argument("--levels", type=int, default=None, help="Number of levels to play")
    args = parser.parse_args()

    game = Game(start_level=args.level)
    game.run(max_levels=args.levels)


if __name__ == "__main__":
    main()
