
# langgraph_setup/trip_flow_graph.py
from langgraph.graph import StateGraph
from langgraph_setup.nodes import (
    analyze_persona, recommend_destinations, generate_itinerary,
    provide_cultural_tips, generate_packing_list
)
from langgraph_setup.state import TripState

def build_trip_graph():
    builder = StateGraph(state_schema=TripState)
    builder.add_node("analyze_persona", analyze_persona)
    builder.add_node("recommend_destinations", recommend_destinations)
    builder.add_node("generate_itinerary", generate_itinerary)
    builder.add_node("provide_cultural_tips", provide_cultural_tips)
    builder.add_node("generate_packing_list", generate_packing_list)

    builder.set_entry_point("analyze_persona")
    builder.add_edge("analyze_persona", "recommend_destinations")
    builder.add_edge("recommend_destinations", "generate_itinerary")
    builder.add_edge("generate_itinerary", "provide_cultural_tips")
    builder.add_edge("provide_cultural_tips", "generate_packing_list")

    return builder.compile()
