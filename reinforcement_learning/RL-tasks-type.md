The structure of the agent-environment interaction loop can differ - 2 categories:
Episodic tasks and Continuing tasks

## Episodic Tasks: Interactions with a Finish Line
RL problems that naturally break into subsequences or segments.
Example, a chess game, a maze run or a robot assembling some parts, each of these represents a self-contained unit of interaction. These units are called **episodes**.

- An episodic task is characterised by the existence of one or more **terminal states**.
- When agent reaches terminal state, the current episode ends.
- After the episode concludes, the environment is typically reset, and a new episode begins, often starting from a standard initial state or a distribution of possible starting states.
Example: a simple grid where an agent needs to navigate from a starting point 'S' to a goal 'G'.
![episodic-task-loop](reinforcement_learning/Episodic-task-loop.png)
The agents objective is typically to maximise the total reward accumulated over the course of a single episode. This sum of rewards within an episode is often called the **return**.
Since each episode has a finite length, the return is well-defined. We might evaluate the agent's performance by averaging the return over many episodes.

## Continuing Tasks: Interactions without an End
RL problems with interactions that do not have a natural endpoint.
Agent-Env interaction goes on continuously without breaking into identifiable episodes.
These are continuing tasks. There are no terminal states. The interaction sequence can in principle, continue forever.
![continuous-task-loop](reinforcement_learning/continuous-task-loop.png)
Now if the interaction never ends, how do we define the total accumulated reward ?
We cannot just sum all the rewards over an infinite sequence as it would lead to an infinite value, making it difficult to compare different policies.

Answer - **Discounting**
Instead of simply summing rewards, we calculate a *discounted return*, where rewards received further in the future are given less weight than immediate rewards. We use a discount factor, typically denoted by the greek letter gamma ($\gamma$), where $0 \le \gamma \lt 1$. The goal becomes maximizing the sum of discounted rewards:
$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ... = \sum_{k=0}^{\infty}\gamma^k R_{t+k+1}
$$
Here, $G_t$ is the discounted return starting from time step t, and $R_{t+k+1}$ is the reward received k+1 steps into the future.
By using discount factor $\gamma \lt 1$, we ensure that this sum remains finite even if the interaction continues forever (assuming rewards are bounded).
Intuitively: Immediate rewards might be more valuable than rewards far off in the future.


Very Important:
When approaching a new problem, one of the 1st questions to ask is: "Does the interaction have a natural endpoint ?"
This will guide how you frame the agent's objective and select appropriate learning techniques.