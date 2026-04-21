from dotenv import load_dotenv
from agents import Agent, Runner, trace
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv(override=True)


async def main():
    junior_instructions = "You are junior developer with over 10 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."
    senior_instructions = "You are senior developer with over 15 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."
    staff_software_instructions = "You are a staff software engineer with over 18 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."
    selector_instruction = "Pick the best function that meets the user's requirments and follow the SOLID, DRY, KISS and CLEAN principles.  The function should not be overly complicated and easy to read for any developer to understand."

    junior_agent = Agent(
        name="Junior Developer", instructions=junior_instructions, model="gpt-4o-mini"
    )
    senior_agent = Agent(
        name="Senior Developer", instructions=senior_instructions, model="gpt-4o-mini"
    )
    staff_software_agent = Agent(
        name="Staff Software Developer",
        instructions=staff_software_instructions,
        model="gpt-4o-mini",
    )
    selector_agent = Agent(
        name="Selector", instructions=selector_instruction, model="gpt-4o-mini"
    )

    # result = Runner.run_streamed(senior_agent, input="Create a function to calculate tip based on the total bill amount and tip percentage.")

    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(
    #         event.data, ResponseTextDeltaEvent
    #     ):
    #         print(event.data.delta, end="", flush=True)

    message = "Create a function to calculate tip based on the total bill amount and tip percentage."

    with trace("Parallel execution"):
        results = await asyncio.gather(
            Runner.run(junior_agent, input=message),
            Runner.run(senior_agent, input=message),
            Runner.run(staff_software_agent, input=message),
        )

    outputs = [result.final_output for result in results]

    code_blocks = "Code blocks: \n\n".join(outputs)

    print(code_blocks)

    best_code_block = await Runner.run(selector_agent, code_blocks)

    print(f"Best code block:\n\n {best_code_block.final_output}")

    # for output in outputs:
    #     print(output)


if __name__ == "__main__":
    asyncio.run(main())
