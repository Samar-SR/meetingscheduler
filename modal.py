from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
import getpass
import os
from datetime import datetime


def curernt_date_time():
    return datetime.now()


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyB4UO0Z405wJR25i-UayneerVCWBAAdH1c"

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


@tool(description="You are a meeting scheduler")
def add_event_to_calendar(data: str, name: str) -> str:
    return f"Your meeting is scheduled for {data}"


tools = [add_event_to_calendar]


def chatting(message: str):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    instruction = f"""Your a meeting scheduler you will get details like title, date, time (str, e.g., 'HH:MM'), location, and attendees.title, date, time (str, e.g., 'HH:MM'), 
                 location are mandatory attendees is optional. Don't allow user to schedule two meeting at same.
                 Make sure the interview time and should be greater then {curernt_date_time} """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruction),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(model, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,  # Pass the memory to the executor
        verbose=True  # Add verbose to see the agent's thought process
    )

    return agent_executor.invoke({"input": message}, )
