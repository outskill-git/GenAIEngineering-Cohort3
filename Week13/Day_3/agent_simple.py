from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Tool 1: Calculator
def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

# Tool 2: Text Length Counter
def text_length(text: str) -> str:
    return f"Length: {len(text)} characters"

# Create tools
tools = [
    Tool(name="Calculator", func=calculator, description="Does math calculations"),
    Tool(name="TextLength", func=text_length, description="Counts text length")
]

# Setup LLM with OpenRouter
llm = ChatOpenAI(
    model="openai/gpt-4o",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)


# Create agent
agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Main function
def main():
    # Test 1
    print("\n=== Test 1: Calculator ===")
    result = agent_executor.invoke({"input": "What is 25 * 4?"})
    print(f"Answer: {result['output']}")
    
    # Test 2
    print("\n=== Test 2: Text Length ===")
    result = agent_executor.invoke({"input": "How long is the text 'Hello World'?"})
    print(f"Answer: {result['output']}")

    # Test 3
    print("\n=== Test 2: Text Length ===")
    result = agent_executor.invoke({"input": "Who is Mark Zuzkerberg?"})
    print(f"Answer: {result['output']}")

if __name__ == "__main__":
    main()