import streamlit as st
from langgraph_setup.run_graph import run_trip_planner

st.set_page_config(page_title="🧳 TravelGenie – LangGraph Edition", layout="wide")

st.title("🧳 TravelGenie – AI-Powered Trip Planner (LangGraph)")

user_input = st.text_area("Describe your ideal trip:", placeholder="e.g. I want a relaxing beach trip with local food and cultural activities.")

if st.button("Plan My Trip"):
    if not user_input.strip():
        st.warning("Please describe your trip preferences before generating a plan.")
    else:
        with st.spinner("Planning your adventure..."):
            result = run_trip_planner(user_input)

        st.success("Here’s your personalized trip plan! 🌍")

        st.subheader("🧠 Your Travel Preferences")
        st.write(result.get("persona", "Not detected."))

        st.subheader("📍 Recommended Destination")
        st.write(result.get("top_destination", "No destination found."))

        st.subheader("📅 Suggested Itinerary")
        st.text(result.get("itinerary", "No itinerary generated."))

        st.subheader("🌍 Cultural Tips")
        st.write(result.get("culture_tips", "No cultural information available."))

        st.subheader("🎒 Packing List")
        st.text(result.get("packing_list", "No packing list generated."))
