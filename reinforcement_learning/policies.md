# Policies: Mapping States to Actions
Agent interacts with env and observes the state and takes actions to receive rewards.
The decision making ability/logic of the agent in a particular state is encapsulated
in the agent's **policy** - its the agents strategy or behavioral brain.

Policy is a mapping of states to actions - defines agents way of behaving at a given time.

## 2 main types:
Deterministic and Stochastic

### Deterministic Policies
- Directly specifies the action the agent will take for each state.
- Agent is in state *s*, the policy π provides a single action *a*. written as:
						a=π(s)
- For every state *s*, in the set of all possible states *S*, the policy π outputs a specific action *a* from the set of available actions *A(s)*.
- Example: Given a state like (position X, clear path ahead), the action (move forward) is fixed.

### Stochastic Policies
- Defines a probability distribution over actions for each state.
- Instead of outputting a single action, it tells us the probability of taking each possible action *a* when in state *s*.
- We denote this as π(a∣s):
$$
π(a∣s) = P [ At​=a ∣ St​=s ]
$$

Here, $P[At=a∣St=s]$ represents the probability that the action *At*​ taken at time step t is a, given that the state St at time t is s. The sum of probabilities for all possible actions in a given state must equal 1:

$$
\sum_{a \in A(s)} \pi(a | s) = 1
$$
for all *s* $\in$ *S*
Particularly useful in:
- Exploration scenarios: agent often needs to try different actions to discover which ones yield the best rewards. Stochastic Policy naturally incorporates this exploration by allowing the agent to occasionally choose actions that aren't currently the best.
- Uncertainty: Sometimes the env itself has randomness, or the agent might not be able to perfectly distinguish b/w states (partially observable envs).
- Avoiding Deterministic Cycles: In certain cases deterministic policy might get stuck in a suboptimal loop, which stochastic policy can break out of.

## The Goal: Finding the Optimal Policy
Central Objective in RL: find an **Optimal Policy**, denoted by $\pi^*$.
Optimal Policy - one that maximizes the expected cumulative reward the agent receives over the long run, starting from any state.

How policies are represented depends on the complexity of the problem.
For simple envs with a small no. of discrete states and actions, a policy might be stored in a lookup table.
However, for problems with large or continuous state spaces (like controlling a robot based on sensor readings or playing video games from pixels), we often use function approximators, such as linear functions or neural networks, to represent the policy $\pi$.
These approximators take the state representation as input and output either the action (deterministic) or probabilities of actions (stochastic).