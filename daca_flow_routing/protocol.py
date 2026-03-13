from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Hashable


HopId = Hashable
FlowId = Hashable
NodeId = Hashable
Timestamp = int


@dataclass(frozen=True)
class Message:
    """A message request to be routed through the network."""

    source_id: NodeId
    target_id: NodeId
    payload: Any | None = None


@dataclass(frozen=True)
class Hop:
    """A single hop event along a directed link (forward or backward)."""

    hop_id: HopId
    from_id: NodeId
    departure_time: Timestamp
    to_id: NodeId
    arrival_time: Timestamp


@dataclass
class MessageFlow:
    """The end-to-end lifecycle of a single message."""

    message_flow_id: FlowId
    start_time: Timestamp
    message: Message
    finish_time: Timestamp = 0  # 0 means not yet delivered


@dataclass(frozen=True)
class MessageHop:
    """A hop together with its associated message flow."""

    hop: Hop
    message_flow_id: FlowId


@dataclass
class CreditFlow:
    """Backward credit flow associated with a message flow."""

    credit_flow_id: FlowId
    message_flow_id: FlowId
    start_time: Timestamp
    finish_time: Timestamp = 0  # 0 means not finished


@dataclass(frozen=True)
class CreditHop:
    """Backward credit hop that assigns credit to a specific forward hop."""

    hop: Hop
    credit_flow_id: FlowId
    message_hop_id: HopId
    credit: float


