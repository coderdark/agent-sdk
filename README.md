# Agent SDK

Small Python demo that uses the OpenAI Agents SDK to generate the same coding task with multiple AI personas in parallel, then asks a selector agent to choose the best result.

## What It Does

The app creates four agents:

- `Junior Developer`
- `Senior Developer`
- `Staff Software Developer`
- `Selector`

For a single prompt, it:

1. Runs the three developer agents at the same time with `asyncio.gather(...)`.
2. Prints each candidate code response.
3. Sends the combined outputs to the selector agent.
4. Prints the final "best" code block chosen by the selector.

The current demo prompt is:

```text
Create a function to calculate tip based on the total bill amount and tip percentage.
```

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
├── main.py
├── pyproject.toml
└── uv.lock
```

## Setup

1. Create your environment file:

```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

3. Install dependencies:

```bash
uv sync
```

## Run

```bash
uv run python main.py
```

## Example Flow

When you run the script, you should see:

- The generated code from the junior agent
- The generated code from the senior agent
- The generated code from the staff-level agent
- A final selected result from the selector agent

## How It Works

[`main.py`](/Users/developer/projects/agent-sdk/main.py) loads environment variables with `load_dotenv(override=True)`, defines role-specific instructions for each agent, and executes the three coding agents in parallel. Their outputs are combined into a single string and passed to a selector agent that chooses the strongest implementation.

## Notes

- The current implementation is a demo script with a hard-coded prompt.
- If you want to make it interactive, the next step would be reading the prompt from user input or the command line.
- `.env` is intentionally not committed; use `.env.example` as the template.
- The lockfile includes `python-dotenv`, which is required because the script imports `load_dotenv`.
