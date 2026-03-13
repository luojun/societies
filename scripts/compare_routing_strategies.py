from __future__ import annotations

import argparse

from daca_flow_routing.experiments.compare_baselines import compare_daca_flow_vs_baselines


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare DACA-Flow routing to random and shortest-delay baselines."
    )
    parser.add_argument("--episodes", type=int, default=100, help="Number of episodes.")
    parser.add_argument("--source", type=str, default="A", help="Source node id.")
    parser.add_argument("--target", type=str, default="D", help="Target node id.")
    args = parser.parse_args()

    stats = compare_daca_flow_vs_baselines(
        source=args.source, target=args.target, num_episodes=args.episodes
    )

    print(f"Episodes: {args.episodes}")
    for name, value in stats.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()

