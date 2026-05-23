Time is modelled in discrete steps: *t* = 0,1,2,3.....
At each time step *t*, the following sequence occurs:
1. Observation: agent observes current state of env. denote this state as $S_t \in S$, where S is the set of all possible states. St must contain all relevant information the agent needs to make a decision.
2. Action Selection: Based on observed state St, agent selects action $A_t \in A(S_t)$, where $A(S_t)$ is the set of actions available in state $S_t$. This selection is governed by the agent's current policy, $\pi$. The policy $\pi(a | s)$ defines the probability of taking action a when in state s. For deterministic policies, it directly maps a state to an action.
3. Environment Transition & Reward: Env receives the agents action At. Based on St and At, 2 things happen:
	1.  The env transitions to a new state $S_{t+1}$. This transition is determined by the env's dynamics, often modeled as a probability distribution $p(s'|s,a) = P(S_{t+1} = s' | S_t = s, A_t = a)$. In many practical scenarios, the agent does not know this transition function explicitly; it learns through interactions.
	2. The env provides a scalar reward signal, $R_{t+1} \in \mathbb{R}$, to the agent. Reward reflects the immediate consequence of taking action $A_t$ in state $S_t$. It's imp to remember the agents goal is not to maximize this immediate reward, but the cumulative reward over time (the return).
4. Next Step: Agent finds itself in state $S_{t+1}$, having received reward $R_{t+1}$. The cycle repeats for time step t + 1: observe $S_{t+1}$, select $A_{t+1}$, and so on.

This ongoing cycle generates a sequence of states, actions, and rewards, often called a trajectory or experience:
S0, A0, R1,  S1, A1, R2,  S2, A2, R3,....
This sequence represents the agents interaction history. This is used by RL to learn and improve the agent's policy $\pi$, aiming to select actions that maximize the expected cumulative future reward.