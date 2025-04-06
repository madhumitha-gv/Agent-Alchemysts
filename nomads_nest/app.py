# import streamlit as st
# import pandas as pd
# import time
# import threading
# import queue
# from logger import log, log_queue
# from langgraph_setup.run_graph import run_trip_planner
# st.set_page_config(page_title="🧳 TravelGenie – LangGraph Edition", layout="wide")
# st.title("🧳 TravelGenie – AI-Powered Trip Planner (LangGraph)")
# import streamlit as st
# import networkx as nx
# import matplotlib.pyplot as plt
# from langgraph_setup.run_graph import run_trip_planner

# # Define the function to create the agent network graph
# def plot_cute_agent_graph():
#     G = nx.DiGraph()  # Directed graph to show flow between agents

#     # Add nodes for each agent
#     agents = [
#         "Persona Analyzer",
#         "Destination Recommender",
#         "Weather Feedback",
#         "Itinerary Generator",
#         "Cultural Guide",
#         "Packing Assistant"
#     ]
#     G.add_nodes_from(agents)

#     # Add directed edges to represent the flow between agents
#     G.add_edges_from([
#         ("Persona Analyzer", "Destination Recommender"),
#         ("Destination Recommender", "Weather Feedback"),
#         ("Weather Feedback", "Itinerary Generator"),
#         ("Weather Feedback", "Destination Recommender"),
#         ("Itinerary Generator", "Cultural Guide"),
#         ("Cultural Guide", "Packing Assistant")
#     ])

#     # Generate the plot with cute styling
#     plt.figure(figsize=(3, 2))  # Smaller size for the graph

#     # Positions using spring layout for a more natural feel
#     pos = nx.spring_layout(G, seed=42)

#     # Node styling
#     nx.draw_networkx_nodes(G, pos, node_size=30, node_color='purple', edgecolors='black', alpha=0.3)
#     nx.draw_networkx_labels(G, pos, font_size=3, font_weight="bold", font_color='black')

#     # Edge styling
#     nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="black", width=0.5, arrows=True, style='solid')

#     # Display the plot in Streamlit inside a smaller container
#     st.subheader("🔗 Cute Agent Interaction Graph")

#     # Use columns for controlling layout width
#     col1, col2 = st.columns([0.2, 0.2])  # Make first column smaller to contain the graph
#     with col1:
#         st.write("")  # Empty text to use space in the first column
#     with col2:
#         st.pyplot(plt)
# plot_cute_agent_graph()



# user_input = st.text_area("Describe your ideal trip:", placeholder="e.g. I want a relaxing beach trip with local food and cultural activities.")

# if st.button("Plan My Trip"):
#     if not user_input.strip():
#         st.warning("Please describe your trip preferences before generating a plan.")
#     else:
#         log_area = st.empty()
#         logs = []
#         result_container = {"result": None}

#         with st.spinner("Planning your adventure..."):

#             def run_graph():
#                 result_container["result"] = run_trip_planner(user_input)

#             thread = threading.Thread(target=run_graph)
#             thread.start()

#             last_log_time = time.time()
#             while thread.is_alive() or not log_queue.empty():
#                 try:
#                     msg = log_queue.get(timeout=0.2)
#                     logs.append(msg)
#                     log_area.text("\n".join(logs))
#                     last_log_time = time.time()
#                 except queue.Empty:
#                     if time.time() - last_log_time > 2 and not thread.is_alive():
#                         break
#                     time.sleep(0.1)

#             thread.join()
#             result = result_container["result"]  # ✅ Safe read

#         # ✅ FINAL DISPLAY (after graph finishes)
#         if result:
#             st.success("Here’s your personalized trip plan! 🌍")

#             st.subheader("🧠 Your Travel Preferences")
#             st.write(result.get("persona", "Not detected."))

#             st.subheader("📍 Recommended Destination")
#             st.markdown(f"**🏁 Final Pick:** {result.get('top_destination', 'No destination')}")

#             st.subheader("❄️ Weather Decisions (Backtracking Log)")
#             weather_log = result.get("weather_log", [])
#             if weather_log:
#                 df = pd.DataFrame(weather_log)
#                 df["Decision"] = df["skipped"].map({True: "⛔️ Skipped", False: "✅ Selected"})
#                 df = df.rename(columns={
#                     "city": "City",
#                     "temperature": "Temp (°C)",
#                     "condition": "Condition"
#                 })[["City", "Temp (°C)", "Condition", "Decision"]]
#                 st.dataframe(df)
#             else:
#                 st.write("No weather log available.")

#             st.subheader("📅 Suggested Itinerary")
#             st.text(result.get("itinerary", "No itinerary generated."))

#             st.subheader("🌍 Cultural Tips")
#             st.write(result.get("culture_tips", "No cultural information available."))

#             st.subheader("🎒 Packing List")
#             st.text(result.get("packing_list", "No packing list generated."))
#         else:
#             st.error("Something went wrong — no result returned.")





import streamlit as st
import pandas as pd
import time
import threading
import queue
from logger import log, log_queue
from langgraph_setup.run_graph import run_trip_planner
import networkx as nx
import matplotlib.pyplot as plt

# Set page config for a cleaner layout
st.set_page_config(page_title="🧳 TravelGenie – LangGraph Edition", layout="wide")

# ---------- Sidebar Navigation ----------
with st.sidebar:
    st.title("Navigate")
    if st.button("🏠 Home"):
        st.session_state.active_section = "home"
        st.rerun()
    if st.button("✈️ Planner"):
        st.session_state.active_section = "planner"
        st.rerun()

# ---------- Custom CSS for Styling ----------
st.markdown("""
<style>
/* General Styling */
html, body {
    font-family: 'Poppins', sans-serif;
    background-color: #f7f5ff;
    color: #3a3b5a;
}

/* Header and Title */
h1, h2, h3 {
    color: #3a3b5a;
}

/* Sidebar */
.css-1d391kg {
    background-color: #f7f5ff;
}

/* Chat interface styling */
.chat-message {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 70%;
    margin-left: auto;
    margin-right: auto;
}

/* User and Assistant message styling */
.user-message {
    background-color: #e0c3fc;
    color: #3a3b5a;
    text-align: left;
}

.assistant-message {
    background-color: #d4e2ff;
    color: #3a3b5a;
    text-align: right;
}

/* Lavender table theme */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

th, td {
    padding: 12px;
    text-align: center;
    border: 1px solid #ddd;
}

th {
    background-color: #e0c3fc;
    color: #3a3b5a;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f7f5ff;
}

tr:nth-child(odd) {
    background-color: #ffffff;
}

/* Button and inputs styling */
.stButton > button {
    background-color: #6a5acd;
    color: white;
    border-radius: 30px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #5a4db8;
}
</style>
""", unsafe_allow_html=True)

# Function to display chat messages
def display_message(content, message_type="assistant"):
    if message_type == "user":
        st.markdown(f'<div class="chat-message user-message">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message">{content}</div>', unsafe_allow_html=True)

# Function to create the agent network graph
def plot_cute_agent_graph():
    G = nx.DiGraph()  # Directed graph to show flow between agents

    # Add nodes for each agent
    agents = [
        "Persona Analyzer",
        "Destination Recommender",
        "Weather Feedback",
        "Itinerary Generator",
        "Cultural Guide",
        "Packing Assistant"
    ]
    G.add_nodes_from(agents)

    # Add directed edges to represent the flow between agents
    G.add_edges_from([("Persona Analyzer", "Destination Recommender"),
                      ("Destination Recommender", "Weather Feedback"),
                      ("Weather Feedback", "Itinerary Generator"),
                      ("Weather Feedback", "Destination Recommender"),
                      ("Itinerary Generator", "Cultural Guide"),
                      ("Cultural Guide", "Packing Assistant")])

    # Generate the plot with cute styling
    plt.figure(figsize=(3, 2))  # Smaller size for the graph

    # Positions using spring layout for a more natural feel
    pos = nx.spring_layout(G, seed=42)

    # Node styling
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='purple', edgecolors='black', alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=3, font_weight="bold", font_color='black')

    # Edge styling
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="black", width=0.5, arrows=True, style='solid')

    st.subheader("🔗 Cute Agent Interaction Graph")

    # Use columns for controlling layout width
    col1, col2 = st.columns([0.2, 0.2])
    with col1:
        st.write("")  # Empty text to use space in the first column
    with col2:
        st.pyplot(plt)

# ---------- Session State Init ----------
if "trip_started" not in st.session_state:
    st.session_state.trip_started = False
if "trip_result" not in st.session_state:
    st.session_state.trip_result = None
if "active_section" not in st.session_state:
    st.session_state.active_section = "home"

# ---------- Page Sections ----------

def show_home():
    st.markdown("""
    <div style='text-align: center; padding-top: 2rem;'>
        <div class='icon-placeholder'>✈️</div>
        <h1>NOMADS NEST</h1>
        <p>Curated travel planning – weather-aware, culturally rich, and personalized just for you!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Planning ✨"):
        st.session_state.active_section = "planner"
        st.rerun()

def show_planner():
    display_message("Welcome! Tell me about your trip preferences:", message_type="assistant")
    user_input = st.text_area("Describe your trip...", key="trip_input")

    if st.button("Start Planning ➡️"):
        if user_input.strip():
            st.session_state.user_input = user_input
            st.session_state.trip_started = True
            st.session_state.active_section = "preferences"
            st.rerun()
        else:
            st.warning("Please enter a trip description.")

def show_preferences():
    display_message("Got it! I’ll use these preferences to suggest a trip plan:", message_type="assistant")

    user_input = st.session_state.get("user_input", "")
    preferences = ["relaxation", "beach", "luxury"]  # Example preferences extraction
    st.session_state.extracted_preferences = preferences

    # Show the preferences
    display_message(f"Top Preferences: {', '.join(preferences)}", message_type="assistant")

    with st.spinner("Planning your perfect adventure..."):
        result_container = {"result": None}

        # Function to run graph in a separate thread
        def run_graph():
            result_container["result"] = run_trip_planner(user_input)

        thread = threading.Thread(target=run_graph)
        thread.start()

        log_area = st.empty()
        logs = []
        last_log_time = time.time()
        while thread.is_alive() or not log_queue.empty():
            try:
                msg = log_queue.get(timeout=0.2)  # Capture logs from the log queue
                logs.append(msg)
                log_area.text("\n".join(logs))  # Update log area
                last_log_time = time.time()
            except queue.Empty:
                # If no logs for 2 seconds, stop waiting
                if time.time() - last_log_time > 2 and not thread.is_alive():
                    break
                time.sleep(0.1)

        thread.join()
        result = result_container["result"]

    if result:
        display_message(f"Here's your personalized trip plan! 🌍", message_type="assistant")
        display_message(f"Recommended Destination: {result.get('top_destination', 'No destination')}", message_type="assistant")

        # Displaying Weather Decisions (lavender-themed table)
        weather_log = result.get("weather_log", [])
        if weather_log:
            df = pd.DataFrame(weather_log)
            df["Decision"] = df["skipped"].map({True: "⛔️ Skipped", False: "✅ Selected"})
            df = df.rename(columns={
                "city": "City",
                "temperature": "Temp (°C)",
                "condition": "Condition"
            })[["City", "Temp (°C)", "Condition", "Decision"]]
            st.markdown("<div style='border-radius: 12px; overflow: hidden;'>", unsafe_allow_html=True)
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            display_message("No weather data available.", message_type="assistant")

        display_message(f"Suggested Itinerary: {result.get('itinerary', 'No itinerary available.')}", message_type="assistant")
        display_message(f"Cultural Tips: {result.get('culture_tips', 'No cultural information available.')}", message_type="assistant")
        display_message(f"Packing List: {result.get('packing_list', 'No packing list available.')}", message_type="assistant")

# ---------- Routing the page based on active section ----------
section = st.session_state.active_section
if section == "home":
    show_home()
elif section == "planner":
    show_planner()
elif section == "preferences":
    show_preferences()