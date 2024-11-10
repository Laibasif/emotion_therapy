import streamlit as st 
from typing import List, TypedDict
from langchain_groq import ChatGroq

# Define the State class with messages as a list of strings
class State(TypedDict):
    messages: List[str]  # List of messages

# Define chatbot function
def chatbot(state: State):
    return {"messages": [llm_model.invoke(state["messages"])]}

# MemorySaver class (ensure you have this class or replace it as necessary)
class MemorySaver:
    def __init__(self):
        self.memory = []

    def save(self, state: dict):
        self.memory.append(state)

memory = MemorySaver()

# Therapy agent setup
def therapy_agent():
    graph_builder = StateGraph(State)
    llm_model = ChatGroq(
        model="llama-3.2-1b-preview",
        verbose=True,
        temperature=0.5,
        api_key="your_api_key_here"  # Replace with your actual API key
    )

    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile(checkpointer=memory)
    return graph

# Emotion therapy function
def emotion_therapy(memory: str):
    graph = therapy_agent()
    messages = []
    config = {"configurable": {"thread_id": "1556"}}
    events = graph.stream(
        {"messages": [("user", memory)]}, 
        config=config,
        stream_mode="values"
    )
    for event in events:
        messages.extend(event['messages'])  # Collect each event message

    # Filter for the last AIMessage in the accumulated messages
    ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
    return ai_messages[-1].content if ai_messages else None  # Return the last AI message if available

# Streamlit interface
import streamlit as st

# Streamlit app setup
st.title("Emotion Therapy Chatbot")
user_input = st.text_input("Enter your message:")

if user_input:
    result = emotion_therapy(user_input)
    if result:
        st.write("AI Response:", result)
    else:
        st.write("No response from AI.")
