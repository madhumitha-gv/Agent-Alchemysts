# app.py
import streamlit as st
from langchain_agents.agent_controller import run_agent_chain

st.title("🧳 TravelGenie – Multi-Agent Trip Planner")

user_input = st.text_area("Describe your ideal trip:")

if st.button("Let the AI Plan"):
    with st.spinner("Thinking..."):
        response = run_agent_chain(user_input)
    st.success("Plan Generated!")
    st.write(response)

days = st.slider("Trip Length (Days)", 1, 30, 5)
mood = st.selectbox("Preferred Vibe", ["Relaxing", "Adventurous", "Cultural"])

# Combine into a formatted prompt
combined_input = f"My trip should be {mood.lower()} and last {days} days. {user_input}"

if st.button("Plan with Custom Vibe"):
    response = run_agent_chain(combined_input)
    st.write(response)
