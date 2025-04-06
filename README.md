# 🧳 Nomads Nest - Agentic Travel Buddy

Nomads Nest is a **multi-agent travel assistant** that intelligently understands user preferences and suggests top destinations tailored to their tastes. It evaluates weather conditions, plans detailed itineraries, provides cultural insights, and even generates a personalized packing list — all automatically. 🌍✈️

### 🎬 Video Demo
[Google Drive Link](#)

## 🚀 Tech Stack

### Frontend:
- **Python** 🐍
- **Streamlit** 📊

### Backend:
- **Pytorch** 🔥
- **Transformers (Hugging Face Models)** 🤖 (GPT-Neo 1.3B, all-MiniLM-L6-v2, Mistral-7B)
- **LangGraph** 🔗

## 👨‍💻 Team Members
- **Anmol Munnolli** 👨‍💻
- **Vishwajyothi Reshmi** 👩‍💻
- **Madhumitha Gannavaram** 👩‍💻

## 💡 Features & Design

The architecture will consist of:

### Frontend:
- **Streamlit** (Python-based web app) to interact with users.

### Backend:
- **Agents** powered by **Hugging Face**, **LangGraph** for agent communication and logic flow.

### Agents:
- **Persona Agent** 👤: Handles user preferences, budget, interests.
- **Destination Agent** 🌍: Recommends travel destinations based on persona.
- **Itinerary Agent** 🗓️: Suggests travel itineraries based on destination.
- **Culture Agent** 🍲: Provides insights into local culture, food, etc.
- **Packing Agent** 🧳: Helps users decide what to pack.
- **Weather Agent** 🌦️: Checks weather conditions and provides feedback on destinations.

## 🛠️ How to Run the Project

### 1. Set up a Virtual Environment
First, create a virtual environment for the project by running the following command in your terminal:
```bash
python -m venv venv
