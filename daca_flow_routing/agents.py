from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .protocol import CreditHop, MessageHop, NodeId
from .network import Network


@dataclass
class RoutingObservation:
    """Observation for routing decisions at a node."""

    node_id: NodeId
    message_hop: MessageHop


@dataclass
class CreditObservation:
    """Observation for credit-relay decisions at a node."""

    node_id: NodeId
    credit_hop: CreditHop


@dataclass
class NodeAgentConfig:
    """Configuration for a node-local agent."""

    epsilon: float = 0.1
    alpha: float = 0.1
    gamma: float = 0.9


@dataclass
class NodeAgent:
    """A simple tabular Q-learning agent for routing decisions."""

    node_id: NodeId
    outgoing_neighbors: List[NodeId]
    config: NodeAgentConfig = field(default_factory=NodeAgentConfig)

    q_values: Dict[Tuple[NodeId, NodeId], float] = field(default_factory=dict)

    def select_routing_action(self, obs: RoutingObservation) -> Optional[NodeId]:
        target = obs.message_hop.hop.to_id

        if obs.message_hop.hop.to_id == target:
            return None

        if not self.outgoing_neighbors:
            return None

        if random.random() < self.config.epsilon:
            return random.choice(self.outgoing_neighbors)

        best_a: Optional[NodeId] = None
        best_q = -math.inf
        for neighbor in self.outgoing_neighbors:
            q = self.q_values.get((target, neighbor), 0.0)
            if q > best_q:
                best_q = q
                best_a = neighbor
        return best_a if best_a is not None else random.choice(self.outgoing_neighbors)

    def update_from_credit(
        self,
        credit_obs: CreditObservation,
        reward: float,
        target_id: NodeId,
        next_best_value: float,
    ) -> None:
        from_id = credit_obs.credit_hop.hop.to_id
        if from_id != self.node_id:
            return

        action = self.node_id
        key = (target_id, action)
        q_old = self.q_values.get(key, 0.0)
        td_target = reward + self.config.gamma * next_best_value
        self.q_values[key] = q_old + self.config.alpha * (td_target - q_old)


def build_node_agents(network: Network, config: Optional[NodeAgentConfig] = None) -> Dict[NodeId, NodeAgent]:
    cfg = config or NodeAgentConfig()
    agents: Dict[NodeId, NodeAgent] = {}
    for node in network.nodes:
        outgoing_neighbors = [link.to_id for link in network.outgoing(node)]
        agents[node] = NodeAgent(node_id=node, outgoing_neighbors=outgoing_neighbors, config=cfg)
    return agents


