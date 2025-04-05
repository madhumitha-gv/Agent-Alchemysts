# agents/packing_agent.py
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_packing_list(destination, preferences):
    prompt = f"Essential packing list for {', '.join(preferences)} vacation in {destination}:"
    packing_list = generator(prompt, max_length=80, num_return_sequences=1)[0]['generated_text']
    return packing_list
