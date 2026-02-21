# Towards an RL Setting for Societies of Agents

## Agent Interface Refresh

Standard RL formalises the agent-environment boundary as the ORA loop: Observation and Reward in, then Action out. We propose extending it to **ORAC**, where **C** denotes a cumulable, socially legible quantity — credit, currency, score — that an agent emits as part of its interactions with other agents in the environment.

The move from ORA to ORAC is not merely additive. It delineates the agent's relation with its environment by explicating what flows between agent and environment partly but essentially in terms of *social valuation* — something that does not reduce to optimising a scalar reward signal in isolation.

### RL-Internal Motivations

Crucially, the proposal is compatible with the standard single-agent RL framework, especially with its founding intuitions expressed as the vintage "reward hypothesis" and the new-fangled "reward is enough" hypothesis.

- The **reward hypothesis** — that all goals can be cast as maximisation of cumulative scalar reward — holds *if the world is nice enough*. But the world is big and varied. A solipsistic agent may be able to learn to maximize its reward. But it cannot be responsible for its reward stream being consistent enough so that maiximization, and thus goal specification, makes sense.
- "**Reward is enough**" *if the society is wise enough* — that is, if the social fabric carries enough cultural memory of historical discoveries to make a stream of scalar signal informative, the architecturally solipsistic agent could acquire any cognitive capabilities.

In other words, the intellectually disciplined solipsism about single-agent RL is only methodologically sound under the background assumptions of a nice enough world and a wise enough society.

### Theoretical Computer Science Motivation

- Optimisation over combinatorial structures is generically NP-hard. Learning amortises the cost by substituting experience for exhaustive search.
- The wisdom of a society is precisely this amortisation at scale: a distributed, historically accumulated store of approximate solutions, heuristics, and norms — what C is meant to encode and transmit.

### Self-Critique

The separation of O from R was already an abstraction that obscures the evaluative character of perception. Is the further separation of C from R a corrective *Aufhebung* — or a compounding of the original sin?

Likewise, the O vs. A distinction presupposes a clean boundary between sensing and acting that embodied agents rarely exhibit. Adding C does not resolve this; it adds a third dimension of demand on the environment specification.

The honest answer: C puts enough demand on the environment that a whole society is needed to sustain it. The ORAC interface only makes sense in a multi-agent setting. This is a feature, not a bug — it forces sociality into the formulation from the start.

## Connections to Existing Research

### Robert Brandom: Deontic Scorekeeping

Brandom's *Making It Explicit* (1994) develops a model of discursive practice that is relevant to the ORAC proposal. In his framework:

- **Inferentialism** holds that the meaning of a concept is constituted not by what it refers to, but by its role in inference — what it commits you to and what it entitles you to. Translated to the agent setting: the "meaning" of C is not a fixed label but is constituted by the inferential and practical consequences it carries across agents.
- **Deontic scorekeeping** is Brandom's mechanism for normative pragmatics. Participants in a discursive practice keep track of each other's *commitments* (what you have bound yourself to) and *entitlements* (what you have earned the right to assert or do). Every speech act updates this score.
- The analogy to ORAC is: flow of C functions as a socially maintained ledger of commitments and entitlements among agents. When one agent assigns credit to another, it updates the deontic score — altering what the recipient is entitled to and what the assigner is committed to.
- **Singular reference** in Brandom's account arises from the social practice of tracking an object across different agents' perspectives. Similarly, a stable notion of "value" or "credit" in a society of agents requires that agents can track and reconcile C across distinct viewpoints — a non-trivial coordination problem which is already being taken up by recent research on A2A (agent-to-agent) coordinationl protocols, even though the credit flow part is yet to be researched on.

Key implication: If C is to function as social currency, its semantics must be *inferentially* constituted — maintained not by fiat but by the ongoing scorekeeping practices of the agents themselves. This is necessary because agents could "cheat". In this sense, unlike the reward signal, which is suppose to be non-negotiable and non-manipulable, the credit flow signal is negotiable and manipulable wherein the semantics is only constituted by the ongoing scorekeeping practices of the agents.

### Michael I. Jordan: Learning-Aware Mechanism Design

Jordan's programme at Berkeley directly addresses the gap between machine learning and microeconomics:

- **Learning-aware mechanism design** extends classical mechanism design (Hurwicz, Myerson) to settings where agents are learning rather than fully rational. The rules of the game must account for the fact that agents update their beliefs and strategies over time — precisely the condition in societies of learning agents.
- **Statistical contract theory** embeds statistical inference within principal-agent contracts. The canonical example: a regulatory agency (principal) and a drug company (agent) face information asymmetry; the contract must control statistical errors (Type I, Type II) while aligning incentives. In the ORAC setting, C-mediated contracts between agents face analogous challenges — how to design credit flows that are robust to estimation error and strategic misreporting.
- **Incentive-aware systems** — Jordan argues that machine learning systems deployed among multiple agents must be designed with incentive compatibility in mind. A recommender system in a two-sided market, for instance, must align the learning objective with the strategic interests of both sides. For ORAC, this means the dynamics of C must be incentive-compatible: agents should not gain by misrepresenting credit.

Key implication: The "mechanism" through which C flows is not merely a technical protocol but a designed institution — one that must be learning-aware, robust to information asymmetry, and incentive-compatible. Jordan's framework provides the mathematical tools for this design.

## Connections to the [Principles](principles.md)

The ORAC setting operationalises several principles:

| Principle | ORAC Operationalisation |
|---|---|
| **Credit assignment as social dynamics** | C is the formal vehicle for inter-agent credit flow — not a scalar reward but a socially maintained quantity |
| **Sustained competition and cooperation** | C-dynamics encode both: cooperation as mutually beneficial credit exchange, competition as tension in credit allocation |
| **Governance through value flow** | Governance emerges from the structure of C-flow rather than from external safety constraints imposed from above |
| **No moat between digital and biological agency** | ORAC makes no substrate distinction — the interface is defined functionally, not materially |
| **Sharing the big world** | The social constraint on C (deontic scorekeeping, checks and balances) formalises the shared nature of the world |

## Setting

A formal specification of the ORAC setting would include:

1. **Agents**: A set of agents $\mathcal{A} = \{a_1, \ldots, a_n\}$, each with its own observation space, action space, and credit register.
2. **Environment**: A shared environment $\mathcal{E}$ that produces observations and mediates the consequences of actions, but does not unilaterally assign credit.
3. **Credit channel (C)**: Each agent $a_i$ at each timestep emits a credit signal $c_i^t$ directed at other agents and receives credit signals from them. The credit is *cumulable* — it accumulates over time and can be aggregated.
4. **Balance constraint**: The total credit in circulation is subject to conservation or accounting constraints — socially maintained balance sheets that enforce checks and balances. This is necessary if C is to function as currency rather than noise.
5. **Theory of Mind (ToM)**: Adding C necessitates that agents model each other's credit-assignment strategies — a minimal form of recursive social modelling.
6. **[DACA-flow](DACA-flow.md)**: Decentralised, Asynchronous Credit Assignment as a flow identity — the conservation law that governs how C circulates and transforms across the social graph.

### Relation to Game Theory

ORAC can be seen as an update to game theory in which:

- Payoffs are not exogenous but are endogenously generated through agents' credit-assignment practices.
- The "game" is not a one-shot or repeated static interaction but a continuously evolving social process with learning agents.
- Equilibrium concepts must be replaced or supplemented by dynamical notions — flows, credit cycles, negotiations, belief updates, and construction of belief structures — reflecting the non-stationary nature of societies.

---

## Questions

Before the ORAC setting can be made rigorous, a number of questions need to be addressed:

### Foundations

1. What is the precise formal relationship between R (reward) and C (credit)? Is R a special case of C (self-assigned credit), or are they genuinely orthogonal channels?
2. Should C be a scalar, a vector, or a structured object (e.g., a commitment-entitlement pair, à la Brandom)?
3. Is the balance constraint on C a hard conservation law (like energy) or a soft norm (like accounting standards) that can be violated at a cost?
4. How do we handle the bootstrapping problem — agents need a working C-system to coordinate, but the C-system requires coordinated agents?

### Dynamics

5. Under what conditions do [DACA-flows](DACA-flow.md) converge to stable credit distributions? When do they exhibit cycles, inflation, or collapse?
6. How does the timescale of credit assignment interact with the timescale of learning? If C is too slow, agents cannot learn from it; if too fast, it becomes noise.
7. What is the right analogue of "equilibrium" in a society of learning agents exchanging C? Is it a fixed point, a limit cycle, or something else?

### Design

8. How should C-mechanisms be designed to be incentive-compatible in the sense of Jordan's learning-aware mechanism design?
9. Can statistical contract theory be extended to multi-party contracts where credit flows through a network rather than between a single principal and agent?
10. What is the minimal ToM requirement? Must agents model each other's C-strategies, or is it sufficient that C be designed so that a simpler heuristic suffices?

### Relation to Existing Frameworks

11. How does ORAC relate to existing multi-agent RL formalisms (Dec-POMDPs, Markov games, mean-field games)? Is it a strict generalisation, or does it carve a different slice?
12. Can Brandom's deontic scorekeeping be formalised mathematically in a way that connects to ORAC, or is the analogy primarily conceptual?
13. How does ORAC relate to token economies, attention economies, and blockchain-based incentive mechanisms — practical systems that already implement forms of C?

### Empirical

14. What is the simplest non-trivial system that can be analysed in terms of ORAC and that yields insight not available from standard MARL?
15. Can [DACA-flow](DACA-flow.md) be demonstrated in a concrete multi-agent environment — and does it produce qualitatively different social dynamics from reward-only settings?
