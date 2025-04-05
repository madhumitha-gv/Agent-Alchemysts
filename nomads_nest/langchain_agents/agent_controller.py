

from dotenv import load_dotenv
load_dotenv()  # Loads from .env

# langchain_agents/agent_controller.py
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain_agents.tools import tools

llm = HuggingFaceHub(
    repo_id="tiiuae/falcon-7b-instruct",
    model_kwargs={"temperature": 0.5, "max_new_tokens": 128}
)



memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

def run_agent_chain(user_input: str):
    return agent.run(user_input)
