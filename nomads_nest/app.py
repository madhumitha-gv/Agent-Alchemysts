# import streamlit as st
# import pandas as pd
# import time
# import threading
# import queue
# import matplotlib.pyplot as plt
# from logger import log, log_queue
# from langgraph_setup.run_graph import run_trip_planner

# # Set the page configuration for the title and layout
# st.set_page_config(page_title="Nomads Nest", layout="wide")

# # 💜 Lavender-Themed CSS
# st.markdown("""
#     <style>
#         body {
#             background-color: #f8f4ff;
#             font-family: 'Arial', sans-serif;
#         }
#         .block-container {
#             padding-top: 2rem;
#         }
#         .stButton > button {
#             background-color: #b39ddb;
#             color: white;
#             font-weight: bold;
#             border: none;
#             border-radius: 8px;
#             padding: 10px 16px;
#         }
#         .stButton > button:hover {
#             background-color: #9575cd;
#         }
#         .stTextArea > label, .stDataFrame > label {
#             color: #5e35b1;
#         }
#         .log-box {
#             background-color: #f0e6ff;
#             border: 1px solid #d1c4e9;
#             border-radius: 10px;
#             padding: 10px;
#             font-family: monospace;
#             white-space: pre-wrap;
#             height: 200px;
#             overflow-y: auto;
#         }
#         .current-step-box {
#             height: 100px;  /* Reduced height of the current step box */
#         }
#         .left-column {
#             background-color: #d1c4e9;  /* Light Purple for Left Sidebar */
#             padding: 20px;
#             border-radius: 12px;
#             width: 25%;
#         }
#         .middle-column {
#             padding: 20px;
#             width: 40%;
#         }
#         .right-column {
#             background-color: #b39ddb;  /* Purple background for Right Column */
#             padding: 20px;
#             width: 30%;
#             border-radius: 12px;
#         }
#         .headline {
#             color: #5e35b1;
#             font-size: 32px;
#             font-weight: bold;
#             margin-bottom: 10px;
#         }
#         .subheadline {
#             color: #9575cd;
#             font-size: 11px;
#             margin-bottom: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # 🔠 Title
# st.markdown("""
#     <style>
#         .title {
#             text-align: center;
#             font-size: 20px;
#             font-weight: bold;
#             color: #5e35b1;
#         }
#     </style>
#     <p class="title">NOMADS NEST</p>
# """, unsafe_allow_html=True)


# st.markdown("""
#     <style>
#         .title {
#             text-align: center;
#             font-size: 30px;
#             font-weight: bold;
#             color: #5e35b1;
#         }
#     </style>
#     <p class="title">Let us take you to your destination</p>
# """, unsafe_allow_html=True)

# # Layout: Three Columns: Left for Logs, Middle for User Input, Right for Graph
# left_col, middle_col, right_col = st.columns([1.5, 2, 1.5], gap="large")

# # Left Column: Activity Log and Current Step
# with left_col:
#     # Current Step and Activity Log containers
#     st.markdown("### Current Step")
#     current_step_log = st.empty()

#     st.markdown("### Activity Log")
#     activity_log = st.empty()

# # Middle Column: User Input
# with middle_col:
#     # Headline and subheadline for the user input section

#     # Input and Submit button
#     st.markdown("### Whats your next destination?")
#     user_input = st.text_area("", placeholder="e.g. A cozy mountain escape with hiking and stargazing.")
#     start_button = st.button("Lets plan")

# # Right Column: Display Graph in Purple Container
# with right_col:
#     st.markdown("### Multi AI Agent graph")
#     # Example Graph in a Purple Container
#     fig, ax = plt.subplots(figsize=(5, 4))
#     ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
#     ax.set_title("graph", fontsize=14)
#     ax.set_xlabel("X Axis")
#     ax.set_ylabel("Y Axis")
#     st.pyplot(fig)

# # 🧳 Start Planning Process if Submit Button is Pressed
# if start_button:
#     if not user_input.strip():
#         st.warning("Please describe your trip preferences before generating a plan.")
#     else:
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
#                     current_step_log.markdown(f'<div class="log-box current-step-box">{msg}</div>', unsafe_allow_html=True)
#                     activity_log.markdown(f'<div class="log-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)
#                     last_log_time = time.time()
#                 except queue.Empty:
#                     if time.time() - last_log_time > 2 and not thread.is_alive():
#                         break
#                     time.sleep(0.1)

#             thread.join()
#             result = result_container["result"]

#         # ✅ Display Final Results on the Middle Panel
#         if result:
#             st.success("Here’s your personalized trip plan!")

#             st.markdown("### Your Travel Preferences")
#             st.write(result.get("persona", "Not detected."))

#             st.markdown("### Recommended Destination")
#             st.markdown(f"**Final Pick:** {result.get('top_destination', 'No destination')}")

#             st.markdown("### Weather Decisions (Backtracking Log)")
#             weather_log = result.get("weather_log", [])
#             if weather_log:
#                 df = pd.DataFrame(weather_log)
#                 df["Decision"] = df["skipped"].map({True: "Skipped", False: "Selected"})
#                 df = df.rename(columns={
#                     "city": "City",
#                     "temperature": "Temp (°C)",
#                     "condition": "Condition"
#                 })[["City", "Temp (°C)", "Condition", "Decision"]]
#                 st.dataframe(df)
#             else:
#                 st.write("No weather log available.")

#             st.markdown("### Suggested Itinerary")
#             st.text(result.get("itinerary", "No itinerary generated."))

#             st.markdown("### Cultural Tips")
#             st.write(result.get("culture_tips", "No cultural information available."))

#             st.markdown("### Packing List")
#             st.text(result.get("packing_list", "No packing list generated."))
#         else:
#             st.error("Something went wrong — no result returned.")
import streamlit as st
import pandas as pd
import time
import threading
import queue
import matplotlib.pyplot as plt
import networkx as nx
from logger import log, log_queue
from langgraph_setup.run_graph import run_trip_planner

# Set the page configuration for the title and layout
st.set_page_config(page_title="Nomads Nest", layout="wide")

# Pastel Color Scheme (Soft Greens and Purples)
st.markdown("""
    <style>
        body {
            background-color: #f4f8f6;  /* Light pastel background */
            font-family: 'Arial', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            background-color: #a5d6a7;  /* Pastel Green */
            color: black;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
        }
        .stButton > button:hover {
            background-color: #81c784;  /* Darker Green */
        }
        .stTextArea > label, .stDataFrame > label {
            color: black;
        }
        .log-box {
            background-color: #e8f5e9;  /* Light pastel green for logs */
            border: 1px solid #c8e6c9;
            border-radius: 10px;
            padding: 12px;
            font-family: monospace;
            white-space: pre-wrap;
            height: 200px;
            overflow-y: auto;
        }
        .current-step-box {
            height: 100px;
        }
        .left-column {
            background-color: #c8e6c9;  /* Pastel Green for Left Sidebar */
            padding: 20px;
            border-radius: 12px;
            width: 25%;
            height: 100%;
        }
        .middle-column {
            padding: 20px;
            width: 40%;
            background-color: #ffffff;  /* White background for user input */
            border-radius: 12px;
        }
        .right-column {
            background-color: #c5cae9;  /* Soft pastel purple for the graph section */
            padding: 20px;
            width: 30%;
            border-radius: 12px;
        }
        .headline {
            color: black;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subheadline {
            color: #388e3c;  /* Pastel Green accent for subheadline */
            font-size: 16px;
            margin-bottom: 20px;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #388e3c;  /* Pastel Green for title */
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #388e3c;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Set the local image as the background
image_path = "background_image.jpg"  # Replace with your image's file path
st.markdown(f"""
    <style>
        body {{
            background-image: url('{image_path}');
            background-size: cover;  /* Ensures the image covers the whole screen */
            background-position: center;  /* Centers the image */
            background-attachment: fixed;  /* Keeps the image fixed when scrolling */
            color: white;  /* Text color to contrast with background */
        }}
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown("<p class='title'>Nomads Nest</p>", unsafe_allow_html=True)

# Subtitle with description
st.markdown("<p class='subheadline'>Let us take you to your next adventure</p>", unsafe_allow_html=True)

# Layout: Three Columns (Left for Logs, Middle for User Input, Right for Graph)
left_col, middle_col, right_col = st.columns([1.5, 2, 1.5], gap="large")

# Left Column: Activity Log and Current Step
with left_col:
    st.markdown("<p class='section-title'>Current Step</p>", unsafe_allow_html=True)
    current_step_log = st.empty()

    st.markdown("<p class='section-title'>Activity Log</p>", unsafe_allow_html=True)
    activity_log = st.empty()

# Middle Column: User Input
with middle_col:
    st.markdown("<p class='section-title'>What’s Your Next Destination?</p>", unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="e.g. A cozy mountain escape with hiking and stargazing.", height=150)
    start_button = st.button("Let’s Plan")

# Right Column: Display AI Agent Graph
with right_col:
    st.markdown("<p class='section-title'>AI Agent Graph</p>", unsafe_allow_html=True)
    
    # Build the directed graph for AI agents
    G = nx.DiGraph()

    # Add nodes (AI agents)
    agents = [
        "analyze_persona", 
        "recommend_destinations", 
        "check_weather", 
        "generate_itinerary", 
        "provide_cultural_tips", 
        "generate_packing_list", 
        "fail"
    ]
    G.add_nodes_from(agents)

    # Add edges (connections between AI agents)
    G.add_edge("analyze_persona", "recommend_destinations")
    G.add_edge("recommend_destinations", "check_weather")
    G.add_edge("check_weather", "generate_itinerary")
    G.add_edge("generate_itinerary", "provide_cultural_tips")
    G.add_edge("provide_cultural_tips", "generate_packing_list")
    G.add_edge("fail", "provide_cultural_tips")  # or end the graph

    # Visualize the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="#a5d6a7", font_size=10, font_weight='bold', edge_color="#388e3c", width=2, arrows=True)
    plt.title("AI Agent Network")
    st.pyplot(plt)

# 🧳 Start Planning Process if Submit Button is Pressed
if start_button:
    if not user_input.strip():
        st.warning("Please describe your trip preferences before generating a plan.")
    else:
        logs = []
        result_container = {"result": None}

        with st.spinner("Planning your adventure..."):

            def run_graph():
                result_container["result"] = run_trip_planner(user_input)

            thread = threading.Thread(target=run_graph)
            thread.start()

            last_log_time = time.time()
            while thread.is_alive() or not log_queue.empty():
                try:
                    msg = log_queue.get(timeout=0.2)
                    logs.append(msg)
                    current_step_log.markdown(f'<div class="log-box current-step-box">{msg}</div>', unsafe_allow_html=True)
                    activity_log.markdown(f'<div class="log-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)
                    last_log_time = time.time()
                except queue.Empty:
                    if time.time() - last_log_time > 2 and not thread.is_alive():
                        break
                    time.sleep(0.1)

            thread.join()
            result = result_container["result"]

        # ✅ Display Final Results on the Middle Panel
        if result:
            st.success("Here’s your personalized trip plan!")

            st.markdown("<p class='section-title'>Your Travel Preferences</p>", unsafe_allow_html=True)
            st.write(result.get("persona", "Not detected."))

            st.markdown("<p class='section-title'>Recommended Destination</p>", unsafe_allow_html=True)
            st.markdown(f"**Final Pick:** {result.get('top_destination', 'No destination')}")

            st.markdown("<p class='section-title'>Weather Decisions (Backtracking Log)</p>", unsafe_allow_html=True)
            weather_log = result.get("weather_log", [])
            if weather_log:
                df = pd.DataFrame(weather_log)
                df["Decision"] = df["skipped"].map({True: "Skipped", False: "Selected"})
                df = df.rename(columns={
                    "city": "City",
                    "temperature": "Temp (°C)",
                    "condition": "Condition"
                })[["City", "Temp (°C)", "Condition", "Decision"]]
                st.dataframe(df)
            else:
                st.write("No weather log available.")

            st.markdown("<p class='section-title'>Suggested Itinerary</p>", unsafe_allow_html=True)
            st.text(result.get("itinerary", "No itinerary generated."))

            st.markdown("<p class='section-title'>Cultural Tips</p>", unsafe_allow_html=True)
            st.write(result.get("culture_tips", "No cultural information available."))

            st.markdown("<p class='section-title'>Packing List</p>", unsafe_allow_html=True)
            st.text(result.get("packing_list", "No packing list generated."))
        else:
            st.error("Something went wrong — no result returned.")
