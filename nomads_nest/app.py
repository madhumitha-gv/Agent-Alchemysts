import streamlit as st
from langgraph_setup.run_graph import run_trip_planner
import pandas as pd

# Page settings
st.set_page_config(page_title="🧳 TravelGenie – LangGraph Edition", layout="wide")
st.title("🧳 TravelGenie – AI-Powered Trip Planner (LangGraph)")

# User input box
user_input = st.text_area("Describe your ideal trip:", placeholder="e.g. I want a relaxing beach trip with local food and cultural activities.")

# Action button
if st.button("Plan My Trip"):
    if not user_input.strip():
        st.warning("Please describe your trip preferences before generating a plan.")
    else:
        with st.spinner("Planning your adventure..."):
            result = run_trip_planner(user_input)

        st.success("Here’s your personalized trip plan! 🌍")

        # Display persona
        st.subheader("🧠 Your Travel Preferences")
        st.write(result.get("persona", "Not detected."))

        # Display destination
        st.subheader("📍 Recommended Destination")
        st.markdown(f"**🏁 Final Pick:** {result.get('top_destination', 'No destination')}")

        # Display weather decision log
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

        # Display itinerary
        st.subheader("📅 Suggested Itinerary")
        print(result)
        st.text(result.get("itinerary", "No itinerary generated."))

        # Cultural tips
        st.subheader("🌍 Cultural Tips")
        st.write(result.get("culture_tips", "No cultural information available."))

        # Packing list
        st.subheader("🎒 Packing List")
        st.text(result.get("packing_list", "No packing list generated."))
