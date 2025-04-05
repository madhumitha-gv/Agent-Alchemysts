# langgraph_setup/nodes.py

from agents import (
    persona_agent,
    destination_agent,
    itinerary_agent,
    culture_agent,
    packing_agent,
    weather_agent
)

from utils.weather_api import fetch_apparent_temperature
from utils.weather_utils import get_current_weather

# Define harsh weather conditions that should trigger backtracking
HARSH_CONDITIONS = {"freezing", "very hot", "hot", "cold"}

# Step 1: Analyze user input to extract persona/preferences
def analyze_persona(state: dict) -> dict:
    preferences = persona_agent.run(state, state["user_input"])
    state["persona"] = preferences
    return state

# Step 2: Recommend destinations based on persona
def recommend_destinations(state: dict) -> dict:
    matches = destination_agent.run(state)

    if not matches or not isinstance(matches, list):
        print("⚠️ No destination matches found.")
        state["top_destination"] = "Unknown"
        state["destination_scores"] = {}
        state["destinations"] = []
        state["all_recommendations"] = []
        return state

    state["all_recommendations"] = matches
    state["current_rec_index"] = 0
    state["top_destination"] = matches[0]["name"]
    state["destination_scores"] = {d["name"]: d["score"] for d in matches}
    state["destinations"] = [d["name"] for d in matches]

    return state

# Step 3: Check weather for each recommended destination
def check_weather(state: dict) -> dict:
    recs = state.get("all_recommendations", [])
    index = state.get("current_rec_index", 0)

    if index >= len(recs):
        state["weather_check_result"] = "fail"
        return state

    destination = recs[index]
    lat, lng = destination["lat"], destination["lng"]
    temp = fetch_apparent_temperature(lat, lng)
    condition = get_current_weather(temp)

    print(f"Checking weather at {destination['name']}: {condition}")

    if condition in HARSH_CONDITIONS:
        state["current_rec_index"] += 1
        state["weather_check_result"] = "harsh"
    else:
        state["final_destination"] = destination
        state["top_destination"] = destination["name"]  # ✅ This line is critical!
        state["weather_check_result"] = "ok"

    return state

# Step 4: Generate itinerary based on selected destination
def generate_itinerary(state: dict) -> dict:
    state["itinerary"] = itinerary_agent.run(state, num_days=2)
    return state

# Step 5: Provide cultural tips for the destination
def provide_cultural_tips(state: dict) -> dict:
    state["culture_tips"] = culture_agent.cultural_tips(state["top_destination"])
    return state

# Step 6: Generate packing list
def generate_packing_list(state: dict) -> dict:
    state["packing_list"] = packing_agent.generate_packing_list(
        state["top_destination"], state.get("persona", [])
    )
    return state
