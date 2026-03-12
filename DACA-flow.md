# DACA-Flow - Distributed Asynchronous Credit Assignment - The Flow Version

## A Setting for Agent Coordination

We formulate a new setting for coordinating the learning of a group of agents. We call this setting **Distributed Asynchronous Credit Assignment** or **DACA**, wherein

- Each agent performs its function and learns to improve its function as a standalone computational unit (distributed);
- Each agent controls the schedule of its own learning and backward credit assignment (see next point) in a way that could be separated in time from when it took the relevant action (asynchronous);
- The learning by each agent involves receiving from others and **assigning to others** as well as to oneself credit or blame associated with specific performance (credit assignment);
- The observation and action spaces of the agents may or may not be different and the agents could be AI and human (heterogeneous); and
- The agents are coordinated through a certain information-sharing protocol, likely under-specified for each agent, which could mix cooperation and competition as well as truthfulness and deception (coordination).

This new setting is motivated by the observation that we are entering a new era of AI, in which

- Individual models are replaced by multiple assistants and agents as units in system analysis (agents);
- Workflow involving heterogeneous assistants and agents is becoming a focus of engineering study (workflow);
- Per-action credit signal is typically unavailable from the environment immediately or directly but needs to be derived from an overall return feedback much later from elsewhere to the system as a whole (return over reward); and
- Humans are often the source of such feedback (human feedback).

## An Algorithm for Agent Coordination

For this setting, we propose a first algorithm called **DACA-Flow**, which  

- Assumes the coordination of a forward single-path, i.e. non-branching, flow of actions and **a backward flow of credits** as the coordination protocol (flow), and
- Handles only cooperation but not competition of heterogeneous agents (cooperative).

## Case Study: Message Routing

We can use denctralized message routing as a case study on the DACA Setting.

### 1. Components

1. **Network:** a network of N nodes as a directed graph, possibly sparsely connected and possibly cyclical.
2. **Node:** each node has a unique ID, which also serves as its "address".
3. **Message:** each message is a tuple of `(Source, Target, Payload)`, where Source and Target are node IDs and Payload could be empty or dummy for our exploratory purposes.
4. **Message Link:** a message could be passed from node A to node B if there exists a message link A=>B (read: "A forward to B"); each message link has its *specific communication delay*.
5. **Message Flow:** as a message is routed across the network, the path it takes (here assumed to be a non-branching sequence of message links) forms a **message flow** that goes *forward*.
6. **Credit Link:** wherever there is a message link A=>B, a corresponding credit link in the opposite direction is assumed: A<=B (read: "A backward from B"), which has its own specific communciation delay that may or may not be the same as that of the corresponding message link.
7. **Credit Flow:** credit signal for a message flow travels in the opposite direction of the message flow via the credit links corresponding to the message links.
8. **Agent:** each node has its corresponding agent that is responsible for
   a. *Routing*, i.e. when given a message, choose the *message link* to send a message, and
   b. *Crediting*, i.e. when receiving a credit, decide the credit for oneself and the credit to send further backwards along the *credit link*.
9. **Environment:**
   a. For the network as a whole, i.e. as a piece of decentralized collective agency, its environment dynamics is the origin over time of the many messages to be sent and received.
   b. For an individual agent responsible for a node, its environment is defined as what's on "the other side" of its "Agent Interface" under the "Flow Protocol", both defined below.

### 2. Optimization Goal, Flow Protocol and Agent Interface

The components above together form a message routing domain. For such a domain we could adopt a certain performance metric, such as average or worse-case delay for message delivery. This turns the DACA setting into a decentralized and asychronous optimization setup.

#### **Flow Protocol**

Towards "solving" such an optimization problem in a decentralized and asynchronous fashion, i.e. for "DACA-Flow", we need a protocol for using flow structures to support the coordination among the node-specific agents:

1. `MESSAGE`: `(SOURCE_ID, TARGET_ID, PAYLOAD)`
2. `MESSAGE_HOP`: `(MESSAGE_HOP_ID, FROM_ID, TO_ID, DEPARTURE_TIME, ARRIVAL_TIME)`, wherein
   - `MESSAGE_HOP_ID` is the unique id for the specific one-link "forward hopping" event from node `FROM_ID` at `DEPATURE_TIME` and arriving at node `TO_ID` at `ARRIVAL_TIME`, and
   - It is assumed that a message link exists between node `FROM_ID` and node `TO_ID`.
3. `CREDIT_HOP`: `(CREDIT_HOP_ID, FROM_ID, TO_ID, DEPARTURE_TIME, ARRIVAL_TIME, CREDIT)`, wherein
   - `CREDIT` is a scalar value in universal (i.e. system-wide consistent) unit, such as a second of real-time delay, and
   - The rest is similar to `MESSAGE_HOP` except that this is for the "backward hopping".
4. `FLOW`: `(FLOW_ID, MESSAGE, START_TIME, FINISH_TIME, MESSAGE_HOP, CREDIT_HOP)`, wherein
   - `FLOW_ID` is a globally unique identifier over the entire network and its history,
   - `(MESSAGE)` is the tuple defined above,
   - `START_TIME` is when the message request "showed up" originally in the network, i.e. when the node `SOURCE_ID` first received the request (from the "environment" such as when a human user clicking on a web link),
   - `FINISH_TIME` is when the message is finally delivered to the `TARGET_ID` node, where `0` could be taken to mean not arrived yet, and
   - `MESSAGE_HOP` and `CREDIT_HOP` may be `null` and could contain redundant information (the detailed situation here is left as an exercise but is also explained further below).
5. NB: for simplicity, we assume that both the forward flow and the backward flow use the same `FLOW` protocol structure, which again means redundancy but so be it.

#### **Agent Interface**

Additionally, we need appropriate agent interface specification:

1. Observation: a `FLOW` specification data object, wherein
   - `FLOW_ID` is always already assigned along with the `MESSAGE`, `START_TIME`, and `FINISH_TIME` (as 0 until the message arrives) by the environment,
   - `MESSAGE_HOP` is `null` when the flow first "appears" in the network,
   - `CREDIT_HOP` is `null` unless `FINISH_TIME` is (set by the environment to be) non-0 (i.e. message delivered), and
   - When `CREDIT_HOP` is not `null`, `MESSAGE_HOP` must represent the corresponding forward hop.
2. Action: a `TO_ID`
   - This action is used by the node to trigger the actual forward message delivery and to compose the forward `MESSAGE_HOP` data object through filling in the `TO-ID`: `(MESSAGE_HOP_ID, FROM_ID, TO_ID, DEPARTURE_TIME, ARRIVAL_TIME)`, and
   - The "action space" here for the agent associated with a particular node could be viewed as the set of IDs of the nodes to which it has a message link.
3. Credit: a scalar value `C`
   - This scalar is used by the node to trigger the actual credit delivery and to compose the backward `CREDIT_HOP` data object through filling in the `CREDIT`: `(CREDIT_HOP_ID, FROM_ID, TO_ID, DEPARTURE_TIME, ARRIVAL_TIME, CREDIT)`, and
   - This credit value should correspond to the overall credit that is due for the whole upstream of the messaging flow (i.e. downstream of backward credit assignment flow).
4. Reward: a scalar value `R` that the agent decided to assign itself according to the **spirit** of soemthing like `R = C_received - C_backpropagated`.


#### 3. DACA-Flow Algorithm

TODO: get Cursor to generate something ...

## Research Tasks

1. Present the DACA-Flow algorithm for policy evaluation and policy improvement,
2. Prove the convergence of the algorithm under idealized conditions,
3. Demonstrate its effectiveness in a simple multi-agent simulation,
4.Demonstarte its effectiveness in a more realistic communication network routing case,
5. Potentially demonstrate its usefulness in solving other important distributed and asychronous optimization challenges, and 
6. Potentially demonstrate that it or simple variants of it could adapt to environment nonstationarity.
