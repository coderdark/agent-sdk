from dotenv import load_dotenv
from agents import Agent, Runner, trace
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)


async def main():
    junior_instructions = "You are junior developer with over 10 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."

    junior_agent = Agent(
        name="Junior Developer", instructions=junior_instructions, model="gpt-4o-mini"
    )

    with trace("Creating tip function"):
        result = Runner.run_streamed(junior_agent, input="Create a function to calculate tip based on the total bill amount and tip percentage.")

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
