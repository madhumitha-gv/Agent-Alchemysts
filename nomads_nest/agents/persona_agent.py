from transformers import pipeline

# More powerful zero-shot model for nuanced classification
classifier = pipeline(
    "zero-shot-classification", 
    model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
)

# agents/persona_agent.py
def run(state, user_input):
    preferences = analyze_preferences(user_input)  # Uses your HF model
    state.persona = preferences
    return preferences

def analyze_preferences(user_text):
    labels = ["beach", "adventure", "relaxation", "history", 
              "culture", "food", "budget", "luxury", 
              "nature", "nightlife", "shopping", "family-friendly"]
              
    results = classifier(user_text, labels, multi_label=True)

    # Sort labels by scores (confidence)
    sorted_preferences = sorted(
        zip(results["labels"], results["scores"]),
        key=lambda x: x[1],
        reverse=True
    )

    # Return top 3 preferences clearly
    top_preferences = [label for label, score in sorted_preferences[:3]]
    
    return top_preferences
