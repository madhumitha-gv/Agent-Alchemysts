import streamlit as st
import pandas as pd
import time
import threading
import queue
from logger import log, log_queue
from langgraph_setup.run_graph import run_trip_planner

st.set_page_config(page_title="🧳 TravelGenie – LangGraph Edition", layout="wide")
st.title("🧳 TravelGenie – AI-Powered Trip Planner (LangGraph)")

user_input = st.text_area("Describe your ideal trip:", placeholder="e.g. I want a relaxing beach trip with local food and cultural activities.")

if st.button("Plan My Trip"):
    if not user_input.strip():
        st.warning("Please describe your trip preferences before generating a plan.")
    else:
        log_area = st.empty()
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
                    log_area.text("\n".join(logs))
                    last_log_time = time.time()
                except queue.Empty:
                    if time.time() - last_log_time > 2 and not thread.is_alive():
                        break
                    time.sleep(0.1)

            thread.join()
            result = result_container["result"]  # ✅ Safe read

        # ✅ FINAL DISPLAY (after graph finishes)
        if result:
            st.success("Here’s your personalized trip plan! 🌍")

            st.subheader("🧠 Your Travel Preferences")
            st.write(result.get("persona", "Not detected."))

            st.subheader("📍 Recommended Destination")
            st.markdown(f"**🏁 Final Pick:** {result.get('top_destination', 'No destination')}")

            st.subheader("❄️ Weather Decisions (Backtracking Log)")
            weather_log = result.get("weather_log", [])
            if weather_log:
                df = pd.DataFrame(weather_log)
                df["Decision"] = df["skipped"].map({True: "⛔️ Skipped", False: "✅ Selected"})
                df = df.rename(columns={
                    "city": "City",
                    "temperature": "Temp (°C)",
                    "condition": "Condition"
                })[["City", "Temp (°C)", "Condition", "Decision"]]
                st.dataframe(df)
            else:
                st.write("No weather log available.")

            st.subheader("📅 Suggested Itinerary")
            st.text(result.get("itinerary", "No itinerary generated."))

            st.subheader("🌍 Cultural Tips")
            st.write(result.get("culture_tips", "No cultural information available."))

            st.subheader("🎒 Packing List")
            st.text(result.get("packing_list", "No packing list generated."))
        else:
            st.error("Something went wrong — no result returned.")
