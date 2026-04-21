# Agent SDK

Small Python demos that use the OpenAI Agents SDK to generate a simple coding task with role-based agents.

The repo includes two examples:

- `single-agent.py`: streams one agent's response token by token.
- `multiple-agents.py`: runs three developer agents in parallel, then asks a selector agent to choose the best result.

## What It Does

Both scripts use the same demo prompt:

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

## Example Flow

When you run `single-agent.py`, you should see the generated code stream directly into the terminal.

When you run `multiple-agents.py`, you should see:

- The generated code from the junior agent
- The generated code from the senior agent
- The generated code from the staff-level agent
- A final selected result from the selector agent

## How It Works

Both scripts load environment variables with `load_dotenv(override=True)`, define role-specific instructions, and use `gpt-4o-mini` through the OpenAI Agents SDK.

`single-agent.py` wraps the run in a trace named `Creating tip function` and prints `ResponseTextDeltaEvent` chunks as they arrive.

`multiple-agents.py` wraps the parallel developer runs in a trace named `Parallel execution`, combines the final outputs, and passes them to the selector agent for comparison.

## Notes

- The current implementation uses hard-coded prompts.
- `.env` is intentionally not committed; use `.env.example` as the template.
- `multiple-agents.py` currently contains a small typo in the selector instructions: `requirments`.
