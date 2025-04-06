
# Nomads Next- Agentic Travel Buddy
[image]

Nomad Nest is a multi-agent travel assistant that intelligently understands user preferences and suggests top destinations tailored to their tastes. It evaluates weather conditions, plans detailed itineraries, provides cultural insights, and even generates a personalized packing list — all automatically.


## Video Demo
## Google Drive Link
## Tech Stack
Frontend
- Python
- Streamlit
- Pytorch
Backend
- Transformers(Hugging face models)(gpt-neo-1.3B,all-MiniLM-L6-v2,Mistral-7B-)
- Langgraph


## Team Members
- Anmol Munnolli
- Vishwajyothi Reshmi
- Madhumitha Gannavaram

## Team Members
- Anmol Munnolli
- Vishwajyothi Reshmi
- Madhumitha Gannavaram

### **Features & Design**
The architecture will consist of:

- Frontend: Streamlit (Python-based web app) to interact with users.

- Backend: Agents (AI models like GPT-Neo, Mistral-7B) powered by Hugging Face, LangGraph for agent communication and logic flow.

Agents:

- Persona Agent: Handles user preferences, budget, interests.

- Destination Agent: Recommends travel destinations based on persona.

- Itinerary Agent: Suggests travel itineraries based on destination.

- Culture Agent: Provides insights into local culture, food, etc.

- Packing Agent: Helps users decide what to pack.

- Weather Agent: Checks weather conditions and provides feedback on destinations.

## **How to Run the Project**

### **1. Set up a Virtual Environment**
- First, create a virtual environment for the project by running the following command in your terminal:
```bash
  python -m venv venv
### **2. Activate the Virtual Environment**
- On **Windows**:
```bash
  .\venv\Scripts\activate
### **3. Install Dependencies**
- Install the required packages listed in requirements.txt:
```bash
   pip install -r requirements.txt
### **4. Run the Backend**
```bash
- After setting up the virtual environment and installing the dependencies, run the agent_controller.py file
### **5. Run the Frontend**
- To start the frontend using Streamlit, run the app.py file:
```bash
   streamlit run app.py

