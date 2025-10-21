# OpenAI Agent SDK — Overview & Quickstart

This repo uses the official ChatKit starter for hosted Agent Builder workflows. You can also build agents programmatically using the OpenAI Agents SDK (TypeScript or Python). This page summarizes what it is, when to use it, and how to start.

## What is the Agents SDK

- Agents: LLMs with instructions and function tools.
- Handoffs: delegate to other agents for specific tasks.
- Guardrails: validate inputs/outputs; stop early on failure.
- Sessions: manage conversation history automatically.
- Tracing: inspect runs, tools, handoffs while developing.

References:
- TypeScript docs: https://openai.github.io/openai-agents-js/
- Python docs: https://openai.github.io/openai-agents-python/
- JS repo: https://github.com/openai/openai-agents-js
- Python repo: https://github.com/openai/openai-agents-python

## When to use it vs ChatKit

| Option | Pros | Cons | Prefer when |
| ------ | ---- | ---- | ----------- |
| ChatKit + Agent Builder | Fastest path, hosted UI, minimal code | Limited to published workflows | You need a UI quickly and can model logic in Agent Builder |
| Agents SDK | Full code control, multi‑agent orchestration, tools/guardrails | You own the orchestration; more code | You need custom behaviors, multi‑agent flows, or tight backend integration |

Both can coexist: keep ChatKit for UI while evolving backend logic in Agents SDK.

## TypeScript Quickstart (bun)

1) Install

```bash
bun add @openai/agents zod
```

2) Set your key (or use `.env.local`)

```bash
export OPENAI_API_KEY=sk-...
```

3) Minimal agent

```ts
import { Agent, run } from "@openai/agents";

const agent = new Agent({
  name: "Assistant",
  instructions: "You are a helpful assistant.",
});

const result = await run(agent, "Write a haiku about recursion in programming.");
console.log(result.finalOutput);
```

Notes:
- For browser voice agents, see `@openai/agents-realtime` and ephemeral client secrets.
- You can set keys in code: `setDefaultOpenAIKey("sk-...")`.

## Python Quickstart

1) Install

```bash
pip install openai-agents
```

2) Set your key

```bash
export OPENAI_API_KEY=sk-...
```

3) Minimal multi‑agent with handoff

```py
from agents import Agent, run

math = Agent(
    name="Math Tutor",
    instructions="Help with math problems. Explain reasoning with examples.",
)

history = Agent(
    name="History Tutor",
    instructions="Assist with historical queries; explain events and context.",
)

triage = Agent(
    name="Triage",
    instructions="Route to the right specialist based on the user question.",
    handoffs=[math, history],
)

result = run(triage, "When did sharks first appear?")
print(result.final_output)
```

## Tools, Guardrails, and Tracing

- Tools: define function tools; SDK handles call/loop updates.
- Guardrails: validate inputs/outputs; fail fast on invalid data.
- Tracing: export traces to inspect actions and handoffs.

See:
- JS Quickstart: https://openai.github.io/openai-agents-js/guides/quickstart/
- JS Voice agents: https://openai.github.io/openai-agents-js/guides/voice-agents/quickstart/
- Python Quickstart: https://openai.github.io/openai-agents-python/quickstart/
- Python Realtime: https://openai.github.io/openai-agents-python/realtime/quickstart/

## Project integration options

- Add a backend route that uses Agents SDK for server‑side orchestration.
- Keep ChatKit UI and proxy to Agents SDK logic instead of Agent Builder.
- Add a new page (`/agent-sdk`) explaining tradeoffs and linking to starter snippets.
- In this repo: server endpoint `POST /api/agents/run` runs a simple Agent with your `OPENAI_API_KEY`.

Example curl:

```bash
curl -sS -X POST http://localhost:3000/api/agents/run \
  -H 'Content-Type: application/json' \
  -d '{"input":"Say hi in one short sentence."}' | jq
```

Security: never expose your long‑lived `OPENAI_API_KEY` in the browser. For voice agents in the browser, generate ephemeral client secrets on the server.
