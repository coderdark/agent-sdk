from dotenv import load_dotenv
from agents import Agent, Runner, trace
import asyncio

load_dotenv(override=True)


async def main():
    todo_instructions = "You write a todo list for the features that need to be implemented."
    todo_reviewer_instructions = "You review the todo list and make sure it is complete and if there is a missing feature, add it."

    todo_creator_agent = Agent(
        name="Todo List Creator",
        instructions=todo_instructions,
        model="gpt-4o-mini"
    )
    todo_reviewer_agent = Agent(
        name="Todo Reviewer",
        instructions=todo_reviewer_instructions,
        model="gpt-4o-mini"
    )

    tool1 = todo_creator_agent.as_tool(tool_name="todo_creator_agent", tool_description="Write a todo list for the features that need to implemented only")
    tool2 = todo_reviewer_agent.as_tool(tool_name="todo_reviewer_agent", tool_description="Review the todo list to make sure is good for development")
  

    tools = [tool1, tool2]
    
    react_dev_instructions = "You are react developer with over 10 years of experience. You create react code using react best practices. Only using functional components."
    python_dev_instructions = "You are python developer with over 10 years of experience. You create python code using python best practices. Only using functional components."

    react_agent = Agent(
        name="React Developer", instructions=react_dev_instructions, model="gpt-4o-mini"
    )
    python_agent = Agent(
        name="Python Developer", instructions=python_dev_instructions, model="gpt-4o-mini"
    )

    description = "Write the code needed to fulfill the feature requests list. Only provide the code and nothing else"

    tool3 = react_agent.as_tool(tool_name="react_agent", tool_description=description)
    tool4 = python_agent.as_tool(tool_name="python_agent", tool_description=description)

    tools2 = [tool3, tool4]

    engineering_manager_instructions = """
    You are an Engineer Manager. Your goal is to utilize any of the two developer tools for react or python to implement the feature requests provided by the engineering manager"
    You will use the react developer tool to create react code.
    You will use the python developer tool to create python code. 
    You do not write any code yourself. 
    You will only use the tools to write the code.
    You return only code and nothing else.
    """

    engineer_manager = Agent(
        name="Engineer Manager",
        instructions=engineering_manager_instructions,
        tools=tools2,
        model="gpt-4o-mini",
        handoff_description="To convert an application feature list into code and implement it."
    )

    handoffs= [engineer_manager]

    po_instructions = """
    You are a product owner with over 10 of experience in software. 
    You are in charge of defining the product and a list of features for a new product and provide the priority of each feature.
    
    1. Create a feature list using the todo creator tool available.
    2. Review the the feature list using the todo reviewer tool, you can use the tool as many time as needed.
    3. Handoff the final reviewed feature list to the engineering manager.

    Crucial Rules:
    - You must use the todo tools to create and review the feature list — do not write it yourself.
    - You must hand off exactly ONE reviewed feature list to the Engineer Manager — never more than one.
    """

    po_agent = Agent(
        name="PO",
        instructions=po_instructions,
        tools=tools,
        model="gpt-4o-mini",
        handoffs=handoffs,
    )

    message = "create a react application for calculating tips based on the total bill amount and tip'"

    with trace("PO"):
        result = await Runner.run(po_agent, message)

        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())