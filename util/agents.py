import json
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent

from util.langchain_tools import SimpleTool, SimpleJsonTool


def create_grader_agent(model_name):

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    tools = [SimpleJsonTool()]
    
    llm = ChatOpenAI(model=model_name, temperature=0)

    system_message = "You are a grader agent to compare questions and answers."

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", 
             "You are given is the list of questions, and a set of solutions for each question, and a set of target answers to grade"
             "Compare each solution with the answer for the corresponding question based on the given set of criterias."
             "All the data you need (answer, question, solution and criteria) is: {input_data}\n"
            "Assign grade points for each criterion. Grade points are measured in percentage score, so give every score in criteria out of 100."
            "Assign 0 points for missing questions.\n\n"
            "Output a JSON object in the following format:\n"
            "{{"
            "    'grades': ["
            "        {{"
            "            'question': '<actual question>',"
            "            'solution': '<actual solution>',"
            "            'answer': '<actual answer>,'"
            "            '<criteria1 from list of criterias>': <score>,"
            "            '<criteria2 from list of criterias>': <score>,"
            "            '...': <score>,"
            "            'explaination': '<justification of why you gave those points for each criteria>',"
            "        }},"
            "        ..."
            "    ]"
            "}}"
             ),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_exe = AgentExecutor(agent=agent, tools=tools, memory=memory,verbose=True)
    return agent_exe


async def run_agent(agent, user_query):
    user_query_str = json.dumps(user_query)
    print(agent.memory.chat_memory)
    print("********************")
    print("user_query", user_query)
    return await agent.ainvoke(input={"input_data": user_query_str}, verbose=True)