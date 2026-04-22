# Agent SDK

Small Python demos that use the OpenAI Agents SDK to generate a simple coding task with role-based agents.

The repo includes three examples:

- `single-agent.py`: streams one agent's response token by token.
- `multiple-agents.py`: runs three developer agents in parallel, then asks a selector agent to choose the best result.
- `tools-from-agents.py`: exposes developer agents as tools that an engineer-manager agent can call before choosing the best result.

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

## Example Flow

When you run `single-agent.py`, you should see the generated code stream directly into the terminal.

When you run `multiple-agents.py`, you should see:

- The generated code from the junior agent
- The generated code from the senior agent
- The generated code from the staff-level agent
- A final selected result from the selector agent

When you run `tools-from-agents.py`, you should see the engineer-manager agent's selected final function after it calls the developer-agent tools.

## How It Works

All scripts load environment variables with `load_dotenv(override=True)`, define role-specific instructions, and use `gpt-4o-mini` through the OpenAI Agents SDK.

`single-agent.py` wraps the run in a trace named `Creating tip function` and prints `ResponseTextDeltaEvent` chunks as they arrive.

`multiple-agents.py` wraps the parallel developer runs in a trace named `Parallel execution`, combines the final outputs, and passes them to the selector agent for comparison.

`tools-from-agents.py` uses `Agent.as_tool(...)` to make the developer agents callable by an `Engineer Manager` agent. The manager runs inside a trace named `Engineer manager` and prints its selected final output.

## Notes

- The current implementation uses hard-coded prompts.
- `.env` is intentionally not committed; use `.env.example` as the template.
- `multiple-agents.py` currently contains a small typo in the selector instructions: `requirments`.
- `tools-from-agents.py` currently contains a small typo in the manager instructions: `pythn`.
