
# agents/destination_agent.py
import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

with open('data/destinations.json') as f:
    destinations = json.load(f)

def run(state):
    if "persona" not in state:
        return []

    user_embedding = model.encode(", ".join(state["persona"]))
    scores = []
    for dest in destinations:
        dest_embedding = model.encode(dest["features"])
        sim_score = util.cos_sim(user_embedding, dest_embedding).item()
        scores.append((dest["name"], sim_score))

    sorted_destinations = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_destinations[:3]

