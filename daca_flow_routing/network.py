from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .protocol import NodeId


@dataclass(frozen=True)
class DirectedLink:
    """A directed link with an associated transmission delay."""

    from_id: NodeId
    to_id: NodeId
    delay: int  # measured in discrete time steps


class Network:
    """Static directed network topology and link delays."""

    def __init__(self, links: Iterable[DirectedLink]):
        self._links: List[DirectedLink] = list(links)
        self._outgoing: Dict[NodeId, List[DirectedLink]] = {}
        self._incoming: Dict[NodeId, List[DirectedLink]] = {}

        for link in self._links:
            self._outgoing.setdefault(link.from_id, []).append(link)
            self._incoming.setdefault(link.to_id, []).append(link)

    @property
    def nodes(self) -> List[NodeId]:
        seen: Dict[NodeId, None] = {}
        for link in self._links:
            seen.setdefault(link.from_id, None)
            seen.setdefault(link.to_id, None)
        return list(seen.keys())

    def outgoing(self, node_id: NodeId) -> List[DirectedLink]:
        return list(self._outgoing.get(node_id, ()))

    def incoming(self, node_id: NodeId) -> List[DirectedLink]:
        return list(self._incoming.get(node_id, ()))

    def delay(self, from_id: NodeId, to_id: NodeId) -> int:
        for link in self._outgoing.get(from_id, ()):
            if link.to_id == to_id:
                return link.delay
        raise KeyError(f"No link from {from_id!r} to {to_id!r}")


def corridor_topology() -> Network:
    """A small corridor-like topology with shortcuts.

    Nodes: A -> B -> C -> D
    Shortcuts: A -> C, B -> D
    Delays are chosen so shortcuts are not always obviously optimal.
    """

    links = [
        DirectedLink("A", "B", delay=1),
        DirectedLink("B", "C", delay=1),
        DirectedLink("C", "D", delay=1),
        DirectedLink("A", "C", delay=2),
        DirectedLink("B", "D", delay=2),
    ]
    return Network(links)


