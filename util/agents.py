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
             "You are given the list of questions, and a set of solutions for each question, and a set of target answers to grade."
             "Your job is to compare the solution and the target answer. In order to compare, first extract the list of points from the solution."
             "After extracting different points, check whether these points are present in the target answer of the corresponding question."
             "Assign score to each point extracted from the solution. Give 0 for points present in solution, but missing in answers."
             "All the data you need (answer, question, solution) is: {input_data}\n"
            "Assign 0 points for missing answers.\n\n"
            "Output a JSON object in the following format:\n"
            "{{"
            "    'grades': ["
            "        {{"
            "            'question': '<actual question>',"
            "            'solution': '<actual solution>',"
            "            'answer': '<actual answer>,'"
            "            'notes': ["
            "               {{"
            "                   'point_solution': '<Extract text from the solution>',"
            "                   'point_answer': '<Exract text from the answer which covers this point (should be empty if not covered)>',"
            "                   'score': <score of whether the point is covered. Give partial points if partially covered>,"
            "               }}"
            "             ],"
            "            'total_score': '<calculate score as average of all scores for each point>,'"
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
             "You are also given a list of maximum points for each question. Make sure to write each answer according to its maximum points."
             "For example, write short answers for small point questions."
             "All the data you need (question, textbook and max_points) is: {input_data}\n"
            "Give the output strictly answers to each question and nothing more. Give your answers in a format:\n"
            "'Answer 1. <Your answer>'\n'Answer 2. <Your answer>'\n..."
            "Also keep your lenght of each answer stricly according to the maximum points. Your answer should be in the following range as per points:\n"
            "5 points: 30-40 words, 10 points: 60-80 words, etc."
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
    return await agent.ainvoke(input={"input_data": user_query_str}, verbose=True)