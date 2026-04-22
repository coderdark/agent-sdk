# Agent SDK

Small Python demos that use the OpenAI Agents SDK to generate simple coding tasks with role-based agents, tools, and handoffs.

The repo includes four examples:

- `single-agent.py`: streams one agent's response token by token.
- `multiple-agents.py`: runs three developer agents in parallel, then asks a selector agent to choose the best result.
- `tools-from-agents.py`: exposes developer agents as tools that an engineer-manager agent can call before choosing the best result.
- `handoffs.py`: uses tools for sub-tasks, then hands work from a product-owner agent to an engineering-manager agent.

## What It Does

All scripts use a variation of the same demo prompt:

```text
Create a function to calculate tip based on the total bill amount and tip percentage.
```

### Single Agent Demo

`single-agent.py` creates one `Junior Developer` agent and uses `Runner.run_streamed(...)` to print the generated function as text deltas arrive.

### Multiple Agent Demo

`multiple-agents.py` creates four agents:

- `Junior Developer`
- `Senior Developer`
- `Staff Software Developer`
- `Selector`

For the prompt, it:

1. Runs the three developer agents at the same time with `asyncio.gather(...)`.
2. Prints each candidate code response.
3. Sends the combined outputs to the selector agent.
4. Prints the final "best" code block chosen by the selector.

### Tools From Agents Demo

`tools-from-agents.py` creates the same junior, senior, and staff software developer agents, then turns each one into a tool with `Agent.as_tool(...)`.

An `Engineer Manager` agent receives those tools and is instructed to:

1. Use all three developer-agent tools to generate function drafts.
2. Evaluate the drafts.
3. Return the single best tip-calculation function.

### Handoffs Demo

`handoffs.py` models a larger workflow:

1. A `PO` agent receives the user's product request.
2. The `PO` uses todo creator and todo reviewer agents as tools to build a reviewed feature list.
3. The `PO` hands the reviewed feature list to an `Engineer Manager` agent.
4. The `Engineer Manager` uses React, Python, and code reviewer agents as tools to generate and review the final code.

This example shows how tools and handoffs can work together: tools help an agent complete a task, while handoffs move control to another specialized agent.

## Tools vs Handoffs

Tools are capabilities an agent can call while it remains in control of the conversation. In this repo, `Agent.as_tool(...)` turns another agent into a callable tool, so a manager-style agent can ask specialist agents to draft code, review code, or create todo lists.

Handoffs transfer the conversation from one agent to another agent. The receiving agent becomes responsible for the next phase of the workflow. In `handoffs.py`, the `PO` agent gathers and reviews requirements, then hands the final feature list to the `Engineer Manager` agent to implement.

Use tools when one agent should orchestrate smaller helper actions. Use handoffs when the work should move to a different agent with a different role, instructions, or responsibility.

## Tech Stack

- Python 3.13+
- [`openai-agents`](https://pypi.org/project/openai-agents/)
- `python-dotenv`
- `asyncio`
- `uv` for dependency management

## Project Structure

```text
.
├── .env.example
├── .python-version
├── handoffs.py
├── multiple-agents.py
├── pyproject.toml
├── README.md
├── single-agent.py
├── tools-from-agents.py
└── uv.lock
```

## Setup

1. Create your environment file:

```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY="your_api_key_here"
```

3. Install dependencies:

```bash
uv sync
```

## Run

Run the streaming single-agent example:

```bash
uv run python single-agent.py
```

Run the parallel multi-agent selector example:

```bash
uv run python multiple-agents.py
```

Run the tools-from-agents manager example:

```bash
uv run python tools-from-agents.py
```

Run the handoffs workflow example:

```bash
uv run python handoffs.py
```

## Example Flow

When you run `single-agent.py`, you should see the generated code stream directly into the terminal.

When you run `multiple-agents.py`, you should see:

- The generated code from the junior agent
- The generated code from the senior agent
- The generated code from the staff-level agent
- A final selected result from the selector agent

When you run `tools-from-agents.py`, you should see the engineer-manager agent's selected final function after it calls the developer-agent tools.

When you run `handoffs.py`, you should see final generated code for a React tip-calculator application after the product-owner agent creates and reviews a feature list, then hands it off for implementation.

## How It Works

All scripts load environment variables with `load_dotenv(override=True)`, define role-specific instructions, and use `gpt-4o-mini` through the OpenAI Agents SDK.

`single-agent.py` wraps the run in a trace named `Creating tip function` and prints `ResponseTextDeltaEvent` chunks as they arrive.

`multiple-agents.py` wraps the parallel developer runs in a trace named `Parallel execution`, combines the final outputs, and passes them to the selector agent for comparison.

`tools-from-agents.py` uses `Agent.as_tool(...)` to make the developer agents callable by an `Engineer Manager` agent. The manager runs inside a trace named `Engineer manager` and prints its selected final output.

`handoffs.py` creates two levels of coordination. The `PO` agent uses todo-list agents as tools, then uses `handoffs=[engineer_manager]` to transfer the reviewed requirements to the engineering manager. The engineering manager then uses developer and reviewer agents as tools to produce the final code.

## Notes

- The current implementation uses hard-coded prompts.
- `.env` is intentionally not committed; use `.env.example` as the template.
- `multiple-agents.py` currently contains a small typo in the selector instructions: `requirments`.
- `tools-from-agents.py` currently contains a small typo in the manager instructions: `pythn`.
- `handoffs.py` currently contains a few typos in prompt strings, but the demo structure is still clear.
