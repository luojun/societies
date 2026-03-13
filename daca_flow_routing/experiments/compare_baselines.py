from __future__ import annotations

from typing import Dict, List

from ..algorithms import DacaFlowConfig, run_daca_flow_policy_iteration
from ..env import MessageRoutingEnv
from ..network import corridor_topology
from ..protocol import NodeId
from .daca_flow_experiments import run_single_episode
from .routing_baselines import (
    run_random_routing_episode,
    run_shortest_delay_routing_episode,
)


def compare_daca_flow_vs_baselines(
    source: NodeId = "A",
    target: NodeId = "D",
    num_episodes: int = 100,
) -> Dict[str, float]:
    """Run random, shortest-delay, and DACA-Flow strategies and compare delays."""
    env = MessageRoutingEnv(network=corridor_topology())

    random_delays: List[float] = []
    shortest_delays: List[float] = []
    daca_delays: List[float] = []

    for _ in range(num_episodes):
        random_delays.append(
            run_random_routing_episode(env, source=source, target=target)
        )
        shortest_delays.append(
            run_shortest_delay_routing_episode(env, source=source, target=target)
        )
        delay, _ = run_single_episode(env, source=source, target=target)
        daca_delays.append(delay)

    def _finite_mean(xs: List[float]) -> float:
        finite = [x for x in xs if x < float("inf")]
        return sum(finite) / len(finite) if finite else float("inf")

    return {
        "random_mean_delay": _finite_mean(random_delays),
        "shortest_mean_delay": _finite_mean(shortest_delays),
        "daca_flow_mean_delay": _finite_mean(daca_delays),
    }


