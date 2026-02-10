The key components of AI agent architecture:
1. An LLM that determines program flow and termination:
  - The defining characteristic of an agent - The LLM decides what to do next and when to stop.
  - provides reasoning capabilities to understand context, make decisions, and recognize when 
  a task is complete, has failed or needs human intervention.

2. Short-term memory for maintaining execution context:
  - agent must track current state, including what it has just done, the results it has received,
  and its current position in the task.
  - Without this working memory, an agent would repeatedly attempt the same first step, unable
  to progress through multi-step processes.

3. Tools for taking action:
  - to interact with the real world
  - calling APIs, querying databases, sending emails, or updating spreadsheets.

4. Explicit success criteria and stopping conditions:
  - very helpful to have clear instructions about what constitutes success, acceptable failure
  modes, and specific scenarios that require escalation in production.

5. Human-in-the-loop capabilities:
  - mechanisms to request clarification, report progress, or escalate complex decisions.
  - increases reliability

6. Long-term Memory and state persistence:
  - remembering previous interactions, user preferences, or completed workflows, helps agents to
  learn patterns and provide increasingly personalized assistance over time.

7. Error Handling and recovery mechanisms:
  - robust mechanisms for handling API failures, timeouts, and unexpected responses.
  - includes retry logic, fallback approaches, and the ability to recognize when a different
  strategy is needed rather than repeatedly attempting failed actions.

## Basic HLD Agent Architecture:
![Agent_Arch](/KnowledgeBase/images/Agent_arch_HLD.png)

There can be variations on this tools usage and the architecture.
First, agent can call multiple tools. Example - customer service agent might query CRM 
to understand customer history, search KnowledgeBase for relevant solutions, and then update
the support ticket - all in a single run.
The agent orchestrates b/w these tools, using the output of one to inform its use to the next.

Second, agent themselves can be tools.

## How LLMs drive decision-making in AI agent architecture:
LLMs effectiveness depends entirely on **how it's configured and prompted**.
System prompt is what transforms a general-purpose language model into a specialized
decision-making engine.

The system prompt must explicitly define the agent's decision framework. This includes:
1. Tool awareness and usage patterns:
  - LLMs should precisely know what tools it has access to, what each tool does, and when
  to use them.
  - provide examples of situations where each tool is appropriate.
2. Stopping conditions and success criteria:
  - Explicitly mention for LLM to understand when it's job is done.
3. Escalation triggers and human handoff protocols:
  - Prompt should clearly define when to ask for human help versus when to proceed
  autonomously.
4. Decision-making methodology:
  - Rather than leaving the LLM to figure out its approach, effective prompts provide a
  structured thinking process.


