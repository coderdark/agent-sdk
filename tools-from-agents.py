from dotenv import load_dotenv
from agents import Agent, Runner, trace
import asyncio

load_dotenv(override=True)


async def main():
    junior_instructions = "You are junior developer with over 10 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."
    senior_instructions = "You are senior developer with over 15 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."
    staff_software_instructions = "You are a staff software engineer with over 18 years of experience. You can create any function using the SOLID, DRY, KISS and CLEAN principles. Only provide the code the user asks and nothing else."

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

    description = "Create a function to calculate tip based on the total bill amount and tip percentage."

    tool1 = junior_agent.as_tool(tool_name="junior_agent", tool_description=description)
    tool2 = senior_agent.as_tool(tool_name="senior_agent", tool_description=description)
    tool3 = staff_software_agent.as_tool(
        tool_name="staff_software_agent", tool_description=description
    )

    tools = [tool1, tool2, tool3]

    instructions = """
You are an Engineer Manager. Your goal is to find the single best function to calculate tips in python using the SOLID, DRY, KISS and CLEAN principles.
 
Follow these steps carefully:
1. Generate Drafts: Use all three developer_agent tools to generate three different functions in pythn. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the function drafts and choose the single best function using your judgment of which one is most effective.
 
Crucial Rules:
- You must use the developer agent tools to generate the function drafts — do not write them yourself.
"""

    engineer_manager = Agent(
        name="Engineer Manager",
        instructions=instructions,
        tools=tools,
        model="gpt-4o-mini",
    )

    message = "Create a calculate tip function in python'"

    with trace("Engineer manager"):
        result = await Runner.run(engineer_manager, message)

        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
