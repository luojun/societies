from __future__ import annotations

import math
from typing import Dict, List, Tuple

from ..agents import CreditObservation, RoutingObservation, build_node_agents
from ..env import MessageRoutingEnv, NodeInbox
from ..protocol import CreditHop, MessageHop, NodeId


def _compute_total_credit_from_delay(delay: int) -> float:
    """Map message delay to a total credit signal."""
    return math.exp(-0.1 * delay)


def run_single_episode(
    env: MessageRoutingEnv,
    source: NodeId,
    target: NodeId,
    max_steps: int = 200,
) -> Tuple[float, Dict[NodeId, float]]:
    """Run a single message routing + credit assignment episode."""
    agents = build_node_agents(env.network)
    env.reset()

    flow_id = env.inject_message(source=source, target=target)
    per_node_reward: Dict[NodeId, float] = {n: 0.0 for n in env.network.nodes}

    inboxes: Dict[NodeId, NodeInbox] = {}

    # Forward routing phase.
    for _ in range(max_steps):
        routing_actions: Dict[NodeId, List[tuple[MessageHop, NodeId]]] = {}
        credit_actions: Dict[NodeId, List[tuple[CreditHop, float]]] = {}

        for node_id, inbox in inboxes.items():
            agent = agents[node_id]
            for msg_hop in inbox.message_hops:
                obs = RoutingObservation(node_id=node_id, message_hop=msg_hop)
                next_node = agent.select_routing_action(obs)
                if next_node is not None:
                    routing_actions.setdefault(node_id, []).append((msg_hop, next_node))

        inboxes = env.step(routing_actions=routing_actions, credit_actions=credit_actions)

        flow = env._message_flows[flow_id]
        if flow.finish_time != 0:
            break

    flow = env._message_flows[flow_id]
    if flow.finish_time == 0:
        return float("inf"), per_node_reward

    delay = flow.finish_time - flow.start_time

    total_credit = _compute_total_credit_from_delay(delay)
    env.start_credit_flow(message_flow_id=flow_id, total_credit=total_credit)
    inboxes = {}

    # Backward credit phase.
    for _ in range(max_steps):
        routing_actions = {}
        credit_actions: Dict[NodeId, List[tuple[CreditHop, float]]] = {}

        for node_id, inbox in inboxes.items():
            agent = agents[node_id]
            for credit_hop in inbox.credit_hops:
                c_received = credit_hop.credit
                c_relayed = c_received
                reward = c_received - c_relayed
                per_node_reward[node_id] += reward

                obs = CreditObservation(node_id=node_id, credit_hop=credit_hop)
                agent.update_from_credit(
                    credit_obs=obs,
                    reward=reward,
                    target_id=flow.message.target_id,
                    next_best_value=0.0,
                )

                credit_actions.setdefault(node_id, []).append((credit_hop, c_relayed))

        inboxes = env.step(routing_actions=routing_actions, credit_actions=credit_actions)

        if all(cf.finish_time != 0 for cf in env._credit_flows.values()):
            break

    return float(delay), per_node_reward


