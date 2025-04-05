# app.py
import streamlit as st
from agents.persona_agent import analyze_preferences
from agents.destination_agent import rank_destinations
from agents.itinerary_agent import generate_itinerary
from agents.culture_agent import cultural_tips
from agents.packing_agent import generate_packing_list

st.title("✈️ TravelGenie MAS 🌍")

user_input = st.text_area("Describe your dream trip:")

if st.button("Plan My Trip!"):
    with st.spinner("Analyzing your preferences..."):
        prefs = analyze_preferences(user_input)
        st.write("### ✅ Your Top Preferences:", prefs)

    with st.spinner("Finding best destinations..."):
        top_dests = rank_destinations(prefs)
        st.write("### 🏖️ Top Destination Matches:", top_dests)

    selected_destination = top_dests[0][0]

    with st.spinner("Crafting itinerary..."):
        itinerary = generate_itinerary(selected_destination, prefs)
        st.write(f"## 📅 Itinerary for {selected_destination}:")
        st.write(itinerary)

    with st.spinner("Gathering cultural tips..."):
        culture = cultural_tips(selected_destination)
        st.write(f"## 🌍 Cultural Insights for {selected_destination}:")
        st.write(culture)

    with st.spinner("Preparing packing suggestions..."):
        packing = generate_packing_list(selected_destination, prefs)
        st.write(f"## 🧳 Packing Suggestions:")
        st.write(packing)
