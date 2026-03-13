from __future__ import annotations

import random
from typing import Dict, List, Tuple

from ..env import MessageRoutingEnv, NodeInbox
from ..network import Network
from ..protocol import CreditHop, MessageHop, NodeId


def _random_neighbor(network: Network, node_id: NodeId) -> NodeId | None:
    outgoing = network.outgoing(node_id)
    if not outgoing:
        return None
    return random.choice(outgoing).to_id


def run_random_routing_episode(
    env: MessageRoutingEnv,
    source: NodeId,
    target: NodeId,
    max_steps: int = 200,
) -> float:
    """Randomly route a single message until delivery or timeout.

    Returns:
      Delivery delay, or inf if not delivered.
    """
    env.reset()
    flow_id = env.inject_message(source=source, target=target)
    inboxes: Dict[NodeId, NodeInbox] = {}

    for _ in range(max_steps):
        routing_actions: Dict[NodeId, List[tuple[MessageHop, NodeId]]] = {}
        credit_actions: Dict[NodeId, List[tuple[CreditHop, float]]] = {}

        for node_id, inbox in inboxes.items():
            for msg_hop in inbox.message_hops:
                if node_id == target:
                    continue
                nxt = _random_neighbor(env.network, node_id)
                if nxt is not None:
                    routing_actions.setdefault(node_id, []).append((msg_hop, nxt))

        inboxes = env.step(routing_actions=routing_actions, credit_actions=credit_actions)

        flow = env._message_flows[flow_id]
        if flow.finish_time != 0:
            return float(flow.finish_time - flow.start_time)

    return float("inf")


def run_shortest_delay_routing_episode(
    env: MessageRoutingEnv,
    source: NodeId,
    target: NodeId,
    max_steps: int = 200,
) -> float:
    """Route a single message using a greedy local shortest-delay heuristic."""
    env.reset()
    flow_id = env.inject_message(source=source, target=target)
    inboxes: Dict[NodeId, NodeInbox] = {}

    for _ in range(max_steps):
        routing_actions: Dict[NodeId, List[tuple[MessageHop, NodeId]]] = {}
        credit_actions: Dict[NodeId, List[tuple[CreditHop, float]]] = {}

        for node_id, inbox in inboxes.items():
            for msg_hop in inbox.message_hops:
                if node_id == target:
                    continue
                outgoing = env.network.outgoing(node_id)
                if not outgoing:
                    continue
                best = min(outgoing, key=lambda link: link.delay)
                routing_actions.setdefault(node_id, []).append((msg_hop, best.to_id))

        inboxes = env.step(routing_actions=routing_actions, credit_actions=credit_actions)

        flow = env._message_flows[flow_id]
        if flow.finish_time != 0:
            return float(flow.finish_time - flow.start_time)

    return float("inf")


