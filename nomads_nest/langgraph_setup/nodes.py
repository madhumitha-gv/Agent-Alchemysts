# langgraph_setup/nodes.py
from agents import persona_agent, destination_agent, itinerary_agent, culture_agent, packing_agent

def analyze_persona(state: dict) -> dict:
    preferences = persona_agent.run(state, state["user_input"])
    state["persona"] = preferences
    return state

def recommend_destinations(state: dict) -> dict:
    matches = destination_agent.run(state)
    state["destination_scores"] = {dest[0]: dest[1] for dest in matches}
    state["destinations"] = list(state["destination_scores"].keys())
    state["top_destination"] = state["destinations"][0] if state["destinations"] else "Unknown"
    return state

def generate_itinerary(state: dict) -> dict:
    state["itinerary"] = itinerary_agent.run(state, num_days=2)
    return state

def provide_cultural_tips(state: dict) -> dict:
    state["culture_tips"] = culture_agent.cultural_tips(state["top_destination"])
    return state

def generate_packing_list(state: dict) -> dict:
    state["packing_list"] = packing_agent.generate_packing_list(
        state["top_destination"], state.get("persona", [])
    )
    return state