## DACA-Flow Message Routing Case Study

This package implements a small, self-contained case study for **DACA-Flow** (Distributed Asynchronous Credit Assignment – Flow version) using decentralized message routing as the domain.

It instantiates the protocol and environment sketched in `../DACA-flow.md` within the broader context of `../setting.md` and `../principles.md`, focusing on a cooperative network of agents that route messages and relay credit backward along the same paths.

### Directory overview

- **`protocol.py`**: DACA(-Flow) **setting / protocol** for this case study.
  - Defines `Message`, `Hop`, `MessageFlow`, `MessageHop`, `CreditFlow`, `CreditHop`, and type aliases for IDs and `Timestamp`.
- **`network.py`**: Network topology and link delays.
  - `DirectedLink`, `Network`, and helpers like `corridor_topology()` (A→B→C→D with shortcuts).
- **`env.py`**: Message-routing **environment**.
  - `MessageRoutingEnv` implements forward and backward link queues, global time, and flow bookkeeping.
  - `NodeInbox` aggregates `MessageHop` and `CreditHop` arrivals at each node.
- **`agents.py`**: Node-local **agents** and observations.
  - `RoutingObservation`, `CreditObservation`, `NodeAgentConfig`, `NodeAgent`, and `build_node_agents(network)`.
- **`algorithms.py`**: DACA-Flow **solution algorithms**.
  - `DacaFlowConfig`, `DacaFlowState`, and `run_daca_flow_policy_iteration(env, source, target, config)`.
- **`experiments/`**: Experiment harnesses and baselines.
  - `daca_flow_experiments.py`: `_compute_total_credit_from_delay`, `run_single_episode(...)` using DACA-Flow-style agents.
  - `routing_baselines.py`: `run_random_routing_episode(...)`, `run_shortest_delay_routing_episode(...)`.
  - `compare_baselines.py`: `compare_daca_flow_vs_baselines(...)` to compare DACA-Flow against baselines.

### Prerequisites

- Requires **Python 3.10+** (no external dependencies beyond the standard library).

### Quickstart: running a simple DACA-Flow experiment

From the repo root:

```bash
python3 -m scripts.run_daca_flow_routing --episodes 100 --source A --target D
```

This will:

- Instantiate a `MessageRoutingEnv` with the corridor topology.
- Run 100 DACA-Flow-style episodes starting at node `A` and targeting node `D`.
- Print:
  - Number of episodes,
  - Number of messages successfully delivered,
  - Average delivery delay over delivered messages.

### Comparing against baselines

To compare DACA-Flow with random routing and a local shortest-delay heuristic:

```bash
python3 -m scripts.compare_routing_strategies --episodes 100 --source A --target D
```

This will run:

- `run_random_routing_episode` (no learning, random neighbor choice),
- `run_shortest_delay_routing_episode` (local greedy choice by link delay),
- `run_single_episode` using DACA-Flow-style agents,

and print a small table of mean delays:

- `random_mean_delay`
- `shortest_mean_delay`
- `daca_flow_mean_delay`

### Expected behaviour and performance

In the corridor topology:

- **Random routing** should exhibit high variance and relatively large mean delays, as paths explore detours arbitrarily.
- **Shortest-delay heuristic** should achieve near-optimal delay by always selecting the locally minimal link delay (it effectively assumes known link delays).
- **DACA-Flow agents** (with a more informative credit rule where `C_kept > 0` at intermediate nodes) are expected, over many episodes, to bias their routing policies toward lower-delay paths, reducing mean delay relative to random routing and ideally approaching the shortest-delay heuristic.

In the current minimal implementation:

- The environment is intentionally simple: one message at a time, fixed topology, and a toy credit rule.
- Agents use tabular structures over very small state and action spaces.
- This makes it easy to trace message flows, credit flows, and per-node rewards while you iterate on more realistic credit dynamics and learning rules.

### Relation to the broader project

- The **protocol and environment** here directly instantiate the DACA-Flow setting in `../DACA-flow.md`: a forward flow of messages and a backward flow of credit over the same non-branching paths.
- The **agents and algorithms** exemplify how local ORAC-style interfaces (observations, actions, and credit) can be used to realise decentralized, asynchronous credit assignment in a concrete domain.
- The **experiments and baselines** provide a first quantitative handle on how these flows of value impact performance, complementing the conceptual and theoretical framing in `../setting.md` and the principles articulated in `../principles.md`.

