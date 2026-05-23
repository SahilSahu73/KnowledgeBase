# Claude Code Harness Engineering

5 core components in claude code:
1. **Single-threaded Master Loop** - drives model through perception, reasoning, and tool execution cycles,
feeding results back into context until task reaches a terminal state.
2. A **typed tool dispatch registry mapping tool** names to handlers, bash, read, write, grep, glob, each
with a strict input schema that constraints what the model can express and the harness must execute.
3. A **Context Management Layer** combining on-demand skill injection, three-tier conversation compression,
and disk-persisted memory to maintain coherent reasoning across sessions that exceed the model's context window.
4. A rule-based **permission governance system** with three evaluation tiers, always deny, always allow, and user-gated
approval backed by a lifecycle event bus that lets external hooks observe and intercept every tool call.
5. A **multi-agent coordination layer** supporting subagent context isolation, async teammate delegation, FSM-governed
inter-agent protocols, and git worktree isolation for parallel task execution without file-level conflicts.


## What is Harness Engineering
Discipline of building the environment that surrounds an AI model, and not the model itself.
The model reasons and decides, the harness executes, constrains, and connects.
A well-designed harness gives the model precisely the tools it needs, nothing more, and governs
exactly what it is allowed to do with them.

4 core principles of harness engineering:
1. Model is the only source of decisions, the harness never branches on model output, it only executes
what the model has requested.
2. Tools are the only interface b/w the model and the world, every action from reading a file to spawning
a sub-agent, goes through a typed, schema-validated tool call.
3. Context is a managed resource, what the model sees at each turn is curated, compressed, and injected
deliberately, not accumulated blindly.
4. Permissions are declarative, not procedural, what is allowed, what is blocked and what requires approval
is defined in configuration, not scattered across conditional logic.
