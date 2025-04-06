# # agents/itinerary_agent.py
# from transformers import pipeline

# generator = pipeline("text-generation", model="gpt2")

# def run(state, num_days=2):
#     if "top_destination" not in state or not state["top_destination"]:
#         return "No destination selected."

#     destination = state["top_destination"]
#     preferences = ", ".join(state.get("persona", []))

#     prompt = f"A detailed {num_days}-day itinerary for a {preferences} trip to {destination}:"
#     output = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
#     return output
from dotenv import load_dotenv
import os
load_dotenv() 
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=HUGGINGFACEHUB_API_TOKEN)
def run(state, num_days=2):
    if "top_destination" not in state or not state["top_destination"]:
        return "No destination selected."

    destination = state["top_destination"]
    preferences = ", ".join(state.get("persona", []))  # ✅ FIXED HERE

    prompt = f"""[INST] You are a travel expert. Create a {num_days}-day itinerary for a trip to {destination}.
Preferences: {preferences}
Format:
Day 1:
- Morning:
- Afternoon:
- Evening:
...
No links, just cultural and food recommendations. [/INST]
"""

    output = client.text_generation(prompt, max_new_tokens=500, temperature=0.7)
    return output
