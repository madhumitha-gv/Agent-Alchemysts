# agents/culture_agent.py
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def cultural_tips(destination):
    text = f"Travelers visiting {destination} should be aware of cultural norms including respect, attire, etiquette, and local customs."
    summary = summarizer(text, max_length=1200, min_length=300)[0]['summary_text']
    return summary