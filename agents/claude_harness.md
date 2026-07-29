# Claude Code Harness Engineering

5 core components in claude code:
1. **Single-threaded Master Loop** - drives model through perception, reasoning, and tool execution cycles,
feeding results back into context until task reaches a terminal state.
Master Agent loop = Perception -> Action -> Observation
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


## How claude code follows the harness principles
1. The Master loop is stateless and generic, it runs identically whether the task is a one-liner fix or a multi-hour
refactor, because all task specific intelligence lives in the model.
By stateless we mean that the master loop itself does not remembers anything. Every iteration is identical, it is a
continuous loop of call model -> Execute tool -> Append result -> Repeat.
The loop never categorizes tasks into different states like debugging or coding etc. There are no internal variables
like current_task, phase, mode, plan, step_number etc.
Everything the model needs is in the conversation context.
The harness has zero task memory, the memory is the context maintained by the model through the harness.
Also it is quite generic/generalized as this same loop takes care of all tasks, no matter what it is.
It does not need any special loop for a specific task.
This is important, because suppose claude released a new model, which is amazing at debugging, then they will not have
to make any code change in the claude code to incorporate the new model.
It is the same loop. Now if the loop was not generic and if it tried to handle different tasks in separate deterministic
ways which are maybe predefined, then incorporating a new model which maybe wants to do things in a different way
would require alot of code change. So this generic flow enables the model to decide the workflow for the task at hand.

Also there is a state that is kept track of, just not inside the orchestration logic.
The state exists as conversation history.
e.g.: user -> assistant tool call -> tool output -> Assistant reasoning -> more tool output -> user .....
Every model invocation receives this history.
So the state lives in messages[] and not the master loop.
This distinction is important because the loop itself can be restarted or even replaced without needing to reconstruct
hidden execution state. If the conversation and any persisted context are available, the loop simply resumes by asking
the model what to do next.

2. The tool registry is the only extension point, adding new capabilities to claude code means registering one new tool,
with a name, description, and an input schema.

3. Context is actively managed at ~92% window usage, older conversation turns are summarized and persisted to disk, keeping
the model's working memory focused on the current task.

4. Permission governance runs as a pre-execution layer, every tool call passes through a rule evaluation before the harness
executes it, making safety a structural property rather than a model behaviour.

## Phase 1: Core Agent Loop
Single architectural primitive that everything else builds on.
Before tools, before permission, before multi-agent coordination,
