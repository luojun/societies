from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Mapping, Optional, Tuple

from .network import Network, corridor_topology
from .protocol import (
    CreditFlow,
    CreditHop,
    FlowId,
    Hop,
    HopId,
    Message,
    MessageFlow,
    MessageHop,
    NodeId,
    Timestamp,
)


@dataclass
class NodeInbox:
    """Events that have just arrived at a node at the current time."""

    message_hops: List[MessageHop]
    credit_hops: List[CreditHop]


class MessageRoutingEnv:
    """Asynchronous message and credit routing environment for DACA-Flow."""

    def __init__(self, network: Optional[Network] = None):
        self.network = network or corridor_topology()
        self.time: Timestamp = 0

        # Queues keyed by (from_id, to_id).
        self._forward_queues: Dict[Tuple[NodeId, NodeId], Deque[MessageHop]] = defaultdict(deque)
        self._backward_queues: Dict[Tuple[NodeId, NodeId], Deque[CreditHop]] = defaultdict(deque)

        # Flow and hop registries.
        self._message_flows: Dict[FlowId, MessageFlow] = {}
        self._credit_flows: Dict[FlowId, CreditFlow] = {}
        self._message_hops: Dict[HopId, MessageHop] = {}

        # For each message flow, remember the sequence of forward hop_ids.
        self._flow_hop_history: Dict[FlowId, List[HopId]] = defaultdict(list)

        # Simple integer counters for ids.
        self._next_message_flow_id: int = 1
        self._next_credit_flow_id: int = 1
        self._next_hop_id: int = 1

    def reset(self) -> None:
        self.time = 0
        self._forward_queues.clear()
        self._backward_queues.clear()
        self._message_flows.clear()
        self._credit_flows.clear()
        self._message_hops.clear()
        self._flow_hop_history.clear()
        self._next_message_flow_id = 1
        self._next_credit_flow_id = 1
        self._next_hop_id = 1

    def inject_message(self, source: NodeId, target: NodeId, payload=None) -> FlowId:
        """Inject a new message request at the current time."""
        flow_id = self._alloc_message_flow_id()
        msg = Message(source_id=source, target_id=target, payload=payload)
        flow = MessageFlow(message_flow_id=flow_id, start_time=self.time, message=msg)
        self._message_flows[flow_id] = flow

        self._enqueue_initial_message_hop(flow)
        return flow_id

    def step(
        self,
        routing_actions: Mapping[NodeId, List[Tuple[MessageHop, NodeId]]],
        credit_actions: Mapping[NodeId, List[Tuple[CreditHop, float]]],
    ) -> Dict[NodeId, NodeInbox]:
        """Advance the simulation by one time step."""
        self._apply_routing_actions(routing_actions)
        self._apply_credit_actions(credit_actions)

        self.time += 1
        return self._collect_current_inboxes()

    def start_credit_flow(self, message_flow_id: FlowId, total_credit: float) -> FlowId:
        """Start a backward credit flow for a completed message flow."""
        if message_flow_id not in self._message_flows:
            raise KeyError(f"Unknown message flow {message_flow_id!r}")
        flow = self._message_flows[message_flow_id]
        if flow.finish_time == 0:
            raise ValueError("Cannot start credit flow before message is delivered.")

        credit_flow_id = self._alloc_credit_flow_id()
        credit_flow = CreditFlow(
            credit_flow_id=credit_flow_id,
            message_flow_id=message_flow_id,
            start_time=self.time,
        )
        self._credit_flows[credit_flow_id] = credit_flow

        last_hop_id = self._flow_hop_history[message_flow_id][-1]
        last_message_hop = self._message_hops[last_hop_id]
        last_hop = last_message_hop.hop
        hop = Hop(
            hop_id=self._alloc_hop_id(),
            from_id=last_hop.to_id,
            departure_time=self.time,
            to_id=last_hop.to_id,
            arrival_time=self.time,
        )
        credit_hop = CreditHop(
            hop=hop,
            credit_flow_id=credit_flow_id,
            message_hop_id=last_hop_id,
            credit=total_credit,
        )
        self._enqueue_credit_hop(credit_hop)
        return credit_flow_id

    # Internal helpers -------------------------------------------------

    def _alloc_message_flow_id(self) -> int:
        flow_id = self._next_message_flow_id
        self._next_message_flow_id += 1
        return flow_id

    def _alloc_credit_flow_id(self) -> int:
        flow_id = self._next_credit_flow_id
        self._next_credit_flow_id += 1
        return flow_id

    def _alloc_hop_id(self) -> int:
        hop_id = self._next_hop_id
        self._next_hop_id += 1
        return hop_id

    def _enqueue_initial_message_hop(self, flow: MessageFlow) -> None:
        hop = Hop(
            hop_id=self._alloc_hop_id(),
            from_id=flow.message.source_id,
            departure_time=self.time,
            to_id=flow.message.source_id,
            arrival_time=self.time,
        )
        msg_hop = MessageHop(hop=hop, message_flow_id=flow.message_flow_id)
        self._register_message_hop(msg_hop)
        self._enqueue_message_hop(msg_hop)

    def _enqueue_message_hop(self, msg_hop: MessageHop) -> None:
        key = (msg_hop.hop.from_id, msg_hop.hop.to_id)
        self._forward_queues[key].append(msg_hop)

    def _enqueue_credit_hop(self, credit_hop: CreditHop) -> None:
        key = (credit_hop.hop.from_id, credit_hop.hop.to_id)
        self._backward_queues[key].append(credit_hop)

    def _register_message_hop(self, msg_hop: MessageHop) -> None:
        self._message_hops[msg_hop.hop.hop_id] = msg_hop
        self._flow_hop_history[msg_hop.message_flow_id].append(msg_hop.hop.hop_id)

    def _apply_routing_actions(
        self,
        routing_actions: Mapping[NodeId, List[Tuple[MessageHop, NodeId]]],
    ) -> None:
        for node_id, actions in routing_actions.items():
            for msg_hop, to_node in actions:
                flow = self._message_flows[msg_hop.message_flow_id]
                if flow.message.target_id == node_id:
                    continue
                link_delay = self.network.delay(node_id, to_node)
                hop = Hop(
                    hop_id=self._alloc_hop_id(),
                    from_id=node_id,
                    departure_time=self.time,
                    to_id=to_node,
                    arrival_time=self.time + link_delay,
                )
                new_msg_hop = MessageHop(hop=hop, message_flow_id=msg_hop.message_flow_id)
                self._register_message_hop(new_msg_hop)
                self._enqueue_message_hop(new_msg_hop)

    def _apply_credit_actions(
        self,
        credit_actions: Mapping[NodeId, List[Tuple[CreditHop, float]]],
    ) -> None:
        for node_id, actions in credit_actions.items():
            for credit_hop, c_relayed in actions:
                message_hop = self._message_hops[credit_hop.message_hop_id]
                flow_id = message_hop.message_flow_id
                history = self._flow_hop_history[flow_id]

                idx = history.index(credit_hop.message_hop_id)
                if idx == 0:
                    flow = self._credit_flows[credit_hop.credit_flow_id]
                    flow.finish_time = self.time
                    continue

                prev_hop_id = history[idx - 1]
                prev_msg_hop = self._message_hops[prev_hop_id]
                prev_hop = prev_msg_hop.hop

                hop = Hop(
                    hop_id=self._alloc_hop_id(),
                    from_id=node_id,
                    departure_time=self.time,
                    to_id=prev_hop.from_id,
                    arrival_time=self.time,
                )
                new_credit_hop = CreditHop(
                    hop=hop,
                    credit_flow_id=credit_hop.credit_flow_id,
                    message_hop_id=prev_hop_id,
                    credit=c_relayed,
                )
                self._enqueue_credit_hop(new_credit_hop)

    def _collect_current_inboxes(self) -> Dict[NodeId, NodeInbox]:
        inboxes: Dict[NodeId, NodeInbox] = {}

        for key, queue in list(self._forward_queues.items()):
            remaining: Deque[MessageHop] = deque()
            while queue:
                msg_hop = queue.popleft()
                if msg_hop.hop.arrival_time == self.time:
                    node_id = msg_hop.hop.to_id
                    inbox = inboxes.setdefault(node_id, NodeInbox(message_hops=[], credit_hops=[]))
                    inbox.message_hops.append(msg_hop)

                    flow = self._message_flows[msg_hop.message_flow_id]
                    if node_id == flow.message.target_id and flow.finish_time == 0:
                        flow.finish_time = self.time
                else:
                    remaining.append(msg_hop)
            if remaining:
                self._forward_queues[key] = remaining
            else:
                del self._forward_queues[key]

        for key, queue in list(self._backward_queues.items()):
            remaining_c: Deque[CreditHop] = deque()
            while queue:
                credit_hop = queue.popleft()
                if credit_hop.hop.arrival_time == self.time:
                    node_id = credit_hop.hop.to_id
                    inbox = inboxes.setdefault(node_id, NodeInbox(message_hops=[], credit_hops=[]))
                    inbox.credit_hops.append(credit_hop)
                else:
                    remaining_c.append(credit_hop)
            if remaining_c:
                self._backward_queues[key] = remaining_c
            else:
                del self._backward_queues[key]

        return inboxes


