from __future__ import annotations

import argparse

from daca_flow_routing import DacaFlowConfig, MessageRoutingEnv, corridor_topology
from daca_flow_routing.algorithms import run_daca_flow_policy_iteration


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DACA-Flow routing experiments.")
    parser.add_argument("--episodes", type=int, default=100, help="Number of episodes.")
    parser.add_argument("--source", type=str, default="A", help="Source node id.")
    parser.add_argument("--target", type=str, default="D", help="Target node id.")
    args = parser.parse_args()

    env = MessageRoutingEnv(network=corridor_topology())
    cfg = DacaFlowConfig(num_episodes=args.episodes)
    state, _ = run_daca_flow_policy_iteration(
        env, source=args.source, target=args.target, config=cfg
    )

    if state.num_delivered:
        avg_delay = state.total_delay / state.num_delivered
    else:
        avg_delay = float("inf")

    print(f"Episodes: {args.episodes}")
    print(f"Delivered: {state.num_delivered}")
    print(f"Average delay: {avg_delay}")


if __name__ == "__main__":
    main()

