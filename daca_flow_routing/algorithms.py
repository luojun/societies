from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .agents import NodeAgent, build_node_agents
from .env import MessageRoutingEnv
from .protocol import NodeId


@dataclass
class DacaFlowConfig:
    """Configuration for a minimal DACA-Flow policy iteration loop."""

    max_forward_steps: int = 200
    max_backward_steps: int = 200
    num_episodes: int = 100


@dataclass
class DacaFlowState:
    """Aggregated statistics from running DACA-Flow."""

    total_delay: float = 0.0
    num_delivered: int = 0


def run_daca_flow_policy_iteration(
    env: MessageRoutingEnv,
    source: NodeId,
    target: NodeId,
    config: DacaFlowConfig | None = None,
) -> Tuple[DacaFlowState, Dict[NodeId, NodeAgent]]:
    """Run a simple decentralized policy evaluation/improvement loop."""
    from .experiments.daca_flow_experiments import run_single_episode

    cfg = config or DacaFlowConfig()
    state = DacaFlowState()
    agents = build_node_agents(env.network)

    for _ in range(cfg.num_episodes):
        delay, _ = run_single_episode(env, source=source, target=target, max_steps=cfg.max_forward_steps)
        if delay < float("inf"):
            state.total_delay += delay
            state.num_delivered += 1

    return state, agents


