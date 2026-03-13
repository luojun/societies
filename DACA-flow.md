# DACA-Flow - Distributed Asynchronous Credit Assignment - The Flow Version

## A Setting for Agent Coordination

We formulate a setting for coordinating the learning of a group of agents. We call this setting **Distributed Asynchronous Credit Assignment** or **DACA**, wherein

1. Each agent performs its function and learns to improve its function as a standalone computational unit—**distributed**;
2. Each agent controls the schedule of its own learning and its participation in credit assignment in a way that could be separated in time from when it took the relevant action—**asynchronous**;
3. The learning by each agent involves receiving from others and **assigning to others** as well as to oneself credit or blame associated with specific performance—**credit assignment**;
- The observation and action spaces of the agents may or may not be different and the agents could be AI and human—*heterogeneous*; and
- The agents are coordinated through a certain information-sharing protocol, likely under-specified for each agent, which could mix cooperation and competition as well as truthfulness and deception—*coordination*.

This setting is motivated by the observation that we are entering a new era of AI, in which

- Individual models are replaced by multiple assistants and agents as units in system analysis—*agents*;
- Workflow involving heterogeneous assistants and agents is becoming a focus of engineering *study—*workflow*;
- Per-action credit signal is typically unavailable from the environment immediately or directly but needs to be derived from an overall return feedback much later from elsewhere to the system as a whole—*return over reward*; and
- Humans are often the source of such feedback—*human feedback*.

## An Algorithm for Agent Coordination

We propose a first algorithm called **DACA-Flow**, which targets a highly limited version of the general DACA setting. DACA-Flow --

- Assumes the coordination of **a forward flow of actions** along a single, non-branching path and **a backward flow of credits** along the same path as the coordination protocol—*flow*, and
- Handles only cooperation but not competition of heterogeneous agents that do not share the same action space—*cooperative*.

## Case Study: Message Routing

We use denctralized message routing as a case study on the DACA Setting and the DACA-Flow algorithm.

### 1. Components

1. **Network:** a network of N nodes as a directed graph, possibly sparsely connected and possibly cyclical.
2. **Node:** each node has a unique ID, which also serves as its "address".
3. **Message:** each message is a tuple of `(Source, Target, Payload)`, where Source and Target are node IDs and Payload could be empty or dummy content for our exploratory purposes.
4. **Message Link:** a message could be passed from node A to node B if there exists a message link A=>B (read: "A forward to B"); each message link has its *specific communication delay*.
5. **Message Flow:** as a message is routed across the network, the path it takes (here assumed to be a non-branching sequence of message links) forms a **message flow** that goes *forward*.
6. **Credit Link:** wherever there is a message link A=>B, a corresponding credit link in the opposite direction is assumed: A<=B (read: "A backward from B"), which also has its *specific communciation delay* that may or may not be the same as that of the corresponding message link.
7. **Credit Flow:** credit signal for a message flow travels in the opposite direction of the message flow via the credit links.
8. **Agent:** each node has its corresponding agent that is responsible for
   a. *Routing*, i.e. when given a message, choosing the *message link* to send a message, and
   b. *Crediting*, i.e. when receiving a credit, deciding the credit for oneself and the credit to send further backwards along the *credit link*.
9. **Environment:**
   a. For the network as a whole, i.e. as a piece of decentralized collective agency, its environment dynamics is primarily the creation and completion of messages to be sent and received, as well as the evolution of the overall state of distributed message passing.
   b. For an individual agent responsible for a node, its environment is defined as what's on "the other side" of its *Agent Interface* under the *Flow Protocol*, both defined below.

### 2. Optimization Goal, Flow Protocol and Agent Interface

The components above together form a message routing domain. For such a domain we could adopt a certain performance metric, such as average and/or worse-case delay for message delivery. This turns the DACA setting into a decentralized and asychronous optimization problem.

#### **Flow Protocol**

Towards "solving" such an optimization problem in a decentralized and asynchronous fashion, i.e. for "DACA-Flow" to work, we need a protocol for using flow structures to support the coordination among the node-specific agents:

1. `MESSAGE`: `(SOURCE_ID, TARGET_ID, PAYLOAD)`
2. `HOP`: `(HOP_ID, FROM_ID, DEPARTURE_TIME, TO_ID, ARRIVAL_TIME)`, wherein
   - `HOP_ID` is the unique id for the specific *forward or backward* single-link hopping event from node `FROM_ID` at `DEPATURE_TIME` and arriving at node `TO_ID` at `ARRIVAL_TIME`, with a fowrard or backward link assumed to exist between node `FROM_ID` and node `TO_ID`.
3. `MESSAGE_FLOW`: `(MESSAGE_FLOW_ID, START_TIME, FINISH_TIME, MESSAGE)`, wherein
   - `MESSAGE_FLOW_ID` is a globally unique identifier over the entire network and its history,
   - `START_TIME` is when the message request "showed up" originally in the network, i.e. when the node `SOURCE_ID` first received the request (from the "environment" such as when a human user clicking on a web link),
   - `FINISH_TIME` is when the message is finally delivered to the `TARGET_ID` node, where `0` could be taken to mean not arrived yet, and
   - `MESSAGE` is the tuple defined above.
4. `MESSAGE_HOP`: `(HOP, MESSAGE_FLOW)`, wherein
   - `HOP` is a tuple defined above, with its `TO_ID` being the main concern of *forward action decision*, and
   - `MESSAGE_FLOW` is a tuple defined above.
5. `CREDIT_FLOW`: `(CREDIT_FLOW_ID, START_TIME, FINISH_TIME, MESSAGE_FLOW_ID)`, wherein
   - `CREDIT_FLOW_ID` is a globally unique identifier over the entire network and its history, and may or may not reuse the id of the corresponding message flow,
   - `START_TIME` is when the request for credit assignment flow first "showed up" originally in the network, presumably upon the success (or failure) of the delivery of the associated message, and
   - `FINISH_TIME` is when the credit assignment flow finally finishes, presumably at the `SOURCE_ID` of the original message, where `0` could be taken to mean not finished yet, and
   - `MESSAGE_FLOW_ID` is ID of the corresponding forward message flow, which may be redundant.
6. `CREDIT_HOP`: `(HOP, CREDIT_FLOW, MESSAGE_HOP_ID, CREDIT)`, wherein
   - `HOP` is a tuple defined above, with its `TO_ID` set to the `FROM_ID` of the original forward message `HOP`,
   - Which entails necessary **per-node book-keeping** that retains the original forward `HOP_ID` and its association with the forward message via `MESSAGE_FLOW_ID`, such that
   - The original forward message's `HOP_ID` could be retrieved and sent backward as `MESSAGE_HOP_ID` of the current `CREDIT_HOP` data object to support "backward chaining", and
   - `CREDIT` is a scalar value in universal (i.e. system-wide consistent) unit, such as a second of real-time that measures delay, and it is this `CREDIT` field of the backward `CREDIT_HOP` that is the primary cocnern of *backward credit assignment*.

#### **Agent Interface**

Additionally, we need appropriate agent interface specification:

1. Message Observation: a `MESSAGE_HOP` data object
2. Message Action: a `TO_ID`, if observation is a `MESSAGE_HOP` and the current node is not `TARGET_ID`.
   - This action triggers a forward message delivery and sets the `TO_ID` field of the `MESSAGE_HOP` data object accordingly.
   - The "action space" here for the agent associated with a node is the set of IDs of the nodes to which it has a message link.
3. Credit Observatin: a `CREDIT_HOP` data object with a `CREDIT` field as `C_received`.
3. Credit Action: a scalar value `C` as `C_relayed`, if observation is a `CREDIT_HOP` and the current node is not `SOURCE_ID`.
   - This scalar is used by the node to trigger the actual credit delivery and to compose the backward `CREDIT_HOP` data object through filling in the `CREDIT` field of the `CREDIT_HOP` object.
   - This credit value should correspond to the overall credit that is due for the whole upstream of the messaging flow (i.e. downstream of backward credit assignment flow).
4. Reward: a scalar value `R` that the agent decided to assign itself according to the **spirit** of soemthing like `R = C_kept = C_received - C_relayed`,
   - Which is expected to locally respect the global credit assignment constraint.

#### **Environment Implementation**

Environment fill in the fields
Node manage queues
Noise
Error handling
Simulation loop
Time measurement and representation
Environment determines the delay

### 3. DACA-Flow Algorithm

TODO: get Cursor to generate something ...

## Research Tasks

1. Present the DACA-Flow algorithm for policy evaluation and policy improvement,
2. Prove the convergence of the algorithm under idealized conditions,
3. Demonstrate its effectiveness in a simple multi-agent simulation,
4.Demonstarte its effectiveness in a more realistic communication network routing case,
5. Potentially demonstrate its usefulness in solving other important distributed and asychronous optimization challenges, and 
6. Potentially demonstrate that it or simple variants of it could adapt to environment nonstationarity.
