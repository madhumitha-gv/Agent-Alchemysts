# langgraph_setup/run_graph.py
from langgraph_setup.trip_flow_graph import build_trip_graph

def run_trip_planner(user_input: str):
    graph = build_trip_graph()
    initial_state = {"user_input": user_input}
    final_state = graph.invoke(initial_state)
    return final_state