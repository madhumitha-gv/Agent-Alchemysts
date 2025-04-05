# agents/persona_agent.py
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def analyze_preferences(user_text):
    labels = ["beach", "adventure", "relaxation", "culture", "food", "budget", "luxury"]
    results = classifier(user_text, labels)
    top_preferences = results["labels"][:3]
    return top_preferences
