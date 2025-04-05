# agents/itinerary_agent.py
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_itinerary(destination, preferences):
    prompt = f"A detailed 2-day itinerary for a {', '.join(preferences)} trip to {destination}:"
    itinerary = generator(prompt, max_length=120, num_return_sequences=1)[0]['generated_text']
    return itinerary
