from dotenv import load_dotenv
from agents import Agent, Runner, trace, Tool, function_tool
import asyncio

load_dotenv(override=True)


@function_tool
def show_response(message: str) -> str:
    blue = "\033[34m"
    bold_cyan = "\033[1;36m"
    bold_magenta = "\033[1;35m"
    bold_yellow = "\033[1;33m"
    dim = "\033[2m"
    green = "\033[32m"
    white = "\033[37m"
    reset = "\033[0m"
    in_code_block = False

    print(f"{bold_cyan}Response from agent:{reset}\n")

    for line in message.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            print(f"{dim}{line}{reset}")
            continue

        if in_code_block:
            color = green
        elif stripped.startswith("###"):
            color = bold_cyan
        elif stripped.endswith(":"):
            color = bold_yellow
        elif "**" in stripped:
            color = bold_magenta
        elif stripped.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            color = blue
        else:
            color = white

        print(f"{color}{line}{reset}")

    return "Response displayed."


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

    tools: list[Tool] = [tool1, tool2, tool3, show_response]

    instructions = """
You are an Engineer Manager. Your goal is to find the single best function to calculate tips in python using the SOLID, DRY, KISS and CLEAN principles.
 
Follow these steps carefully:
1. Generate Drafts: Use all three developer_agent tools to generate three different functions in python. Do not proceed until all three drafts are ready.
2. Evaluate and Select: Review the function drafts and choose the single best function using your judgment of which one is most effective.
3. Call the show_response tool exactly once with your final formatted response.

Crucial Rules:
- You must use the developer agent tools to generate the function drafts — do not write them yourself.
- After calling show_response, do not repeat the same response in plain text.
"""

    engineer_manager = Agent(
        name="Engineer Manager",
        instructions=instructions,
        tools=tools,
        model="gpt-4o-mini",
    )

    message = "Create a calculate tip function in python'"

    with trace("Engineer manager"):
        await Runner.run(engineer_manager, message)

if __name__ == "__main__":
    asyncio.run(main())
