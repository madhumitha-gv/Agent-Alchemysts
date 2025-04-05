# agents/itinerary_agent.py
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def run(state, num_days=2):
    if "top_destination" not in state or not state["top_destination"]:
        return "No destination selected."

    destination = state["top_destination"]
    preferences = ", ".join(state.get("persona", []))

    prompt = f"A detailed {num_days}-day itinerary for a {preferences} trip to {destination}:"
    output = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
    return output