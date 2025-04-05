# agents/itinerary_agent.py
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_itinerary(destination, preferences):
    prompt = f"A detailed 2-day itinerary for a {', '.join(preferences)} trip to {destination}:"
    itinerary = generator(prompt, max_length=120, num_return_sequences=1)[0]['generated_text']
    return itinerary

# agents/itinerary_agent.py
def run(state, num_days=5):
    if not state.destination_scores:
        return None

    top_place = max(state.destination_scores, key=state.destination_scores.get)
    plan = generate_itinerary(top_place, num_days)  # Using LLMs like flan-t5
    state.itinerary = plan
    return plan
