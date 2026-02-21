# DACA-Flow - Distributed Asynchronous Credit Assignment - The Flow Version

We formulate a new setting for coordinating the learning of a group of agents, wherein

- Each agent performs its function and learns to improve its function as a standalone computational unit (distributed);
- Each agent controls the schedule of its own learning which could be decoupled in time from its action taking (asynchronous);
- The learning by each agent involves receiving from others and assigning to others as well as to oneself credit or blame associated with specific performance (credit assignment);
- The observation and action spaces of the agents may or may not be different and the agents could be AI and human (heterogeneous); and
- The agents are coordinated through a certain information-sharing protocol, likely under-specified for each agent, which could mix cooperation and competition as well as truthfulness and deception (coordination).

This new setting is motivated by the observation that we are entering a new era of AI, in which
- Individual models are replaced by multiple assistants and agents as units in system analysis (agents);
- Workflow involving heterogeneous assistants and agents is becoming a focus of engineering study (workflow);
- Per-action credit signal is typically unavailable from the environment immediately or directly but needs to be derived from an overall return feedback much later from elsewhere to the system as a whole (return over reward) -- the situation here seems very interesting -- what are we relaxing here?:
    - ``scalar reward'' vs. ``discrete preference''? 
    - do we even need to construct step-specific reward? can we simply do with global return for entire flows?
    - how important is ``individual responsibility''? only through ``individual context'', e.g. $credit_{team} = f(ctx_{xiangyu})$ vs. $credit_{team} = g(ctx_{jun})$, but not through ``individual reward'' $credit_{xiangyu} = f(ctx_{xiangyu})$ vs. $credit_{jun} = g(ctx_{jun})$?
    - etc.; and
- Humans are often the source of such feedback (human feedback).

We call this setting ``Distributed Asynchronous Credit Assignment'' or ``DACA''. For this setting, we propose a first algorithm called ``DACA Flow'', which  
- Assumes the coordination of a forward single-path, i.e. non-branching, flow of performance and a backward flow of credit as the coordination protocol (flow), and
- Handles only cooperation but not competition of heterogeneous agents (cooperative).

We
- Present the DACA-Flow algorithm for policy evaluation and improvement,
- Prove the convergence of the algorithm under idealized conditions, and
- Demonstrate its effectiveness in a simple multi-agent simulation and a more realistic communication network routing case.
