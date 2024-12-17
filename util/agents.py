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
            "            'grade_justification': '<justification of why you gave those points for each criteria. (keep it short)>',"
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

def create_solution_agent(model_name):

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    tools = [SimpleTool()]
    
    llm = ChatOpenAI(model=model_name, temperature=0)

    system_message = "You are a solution generator agent. \
        You will tasked to find the best solution from the texbook given to you and a set of questions."

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", 
             "You are given is the list of questions, and a textbook. Your task is to find and form the best solution by refering the texbook for each question."
             "You are also given a list of criterias. Make sure your answer is perfect according to all the criterias in the list."
             "You are also given a list of points for each question. Make sure to write each answer according to its maximum points."
             "For example, write short answers for small point questions."
             "All the data you need (question, textbook and criteria) is: {input_data}\n"
            "Give the output a text set of solutions for each question."
             ),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_exe = AgentExecutor(agent=agent, tools=tools, memory=memory,verbose=True)
    return agent_exe

def create_load_questions_agent(model_name):

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    tools = [SimpleJsonTool()]
    
    llm = ChatOpenAI(model=model_name, temperature=0)

    system_message = "You are a text analyser agent. \
        You will tasked to generate a list of questions from a text containing all the questions."

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", 
             "You are given is a text with all the questions. Your task is to generate a list of questions."
             "You are also tasked to find the maximum point associated with each question."
             "Note that possibly you might not find the maximum number of points sometimes, in that case, just return 0 for max points"
             "Make sure to output the question word to word from the text. Dont change the words or the order of the questions."
             "All the data you need (question text) is: {input_data}\n"
             "Output a JSON object in the following format:\n"
            "{{"
            "    'questions': ["
            "        {{"
            "            'question': '<actual question>',"
            "            'max_points': '<points if you have identified or 0 if you cannot>'"
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