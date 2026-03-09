"""
Program entry point.
"""

import argparse

from transactions import run_tx_flow

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        choices=["legacy", "p2sh-segwit", "both"],
        required=False,
        default="both"
    )
    parser.add_argument(
        "--stage",
        choices=["AtoB", "BtoC", "both"],
        required=False,
        default="both"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    if args.type in ["legacy", "both"]:
        print("="*20 +" Legacy Transactions " + "="*20)
        if args.stage in ["AtoB", "both"]:
            run_tx_flow("p2pkh", "AtoB")
        if args.stage in ["BtoC", "both"]:
            run_tx_flow("p2pkh", "BtoC")
        print()

    if args.type in ["p2sh-segwit", "both"]:
        print("="*20 + " P2SH-SegWit Transactions " + "="*20)
        if args.stage in ["AtoB", "both"]:
            run_tx_flow("p2sh-segwit", "AtoB")
        if args.stage in ["BtoC", "both"]:
            run_tx_flow("p2sh-segwit", "BtoC")

if __name__ == "__main__":
    main()
