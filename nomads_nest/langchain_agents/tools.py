# langchain_agents/tools.py
from langchain.agents import Tool
from agents import persona_agent, destination_agent, itinerary_agent

tools = [
    Tool(
        name="Persona Analyzer",
        func=lambda x: persona_agent.run(None, x),  # You can wire in shared_state later
        description="Classifies the user's travel preferences based on a sentence"
    ),
    Tool(
        name="Destination Recommender",
        func=lambda _: destination_agent.run(None),  # Assumes persona already exists in state
        description="Recommends destinations based on travel preferences"
    ),
    Tool(
        name="Itinerary Generator",
        func=lambda _: itinerary_agent.run(None, num_days=5),
        description="Generates a 5-day itinerary for the selected destination"
    )
]
