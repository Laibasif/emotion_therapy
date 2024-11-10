import streamlit as st
from typing import List, TypedDict
from langchain_groq import ChatGroq

# Define the State class with messages as a list of strings
class State(TypedDict):
    messages: List[str]  # List of messages

# Define the chatbot function
def chatbot(state: State):
    # Assuming `llm_model.invoke()` handles the conversation, and state["messages"] holds user inputs.
    response = llm_model.invoke({"messages": state["messages"]})
    return {"messages": response["messages"]}

# MemorySaver class (ensure you have this class or replace it as necessary)
class MemorySaver:
    def __init__(self):
        self.memory = []

    def save(self, state: dict):
        self.memory.append(state)

memory = MemorySaver()

# Therapy agent setup
def therapy_agent():
    # Define START and END to mark the beginning and end of the graph flow
    START = "start"
    END = "end"

    graph_builder = StateGraph(State)
    llm_model = ChatGroq(
        model="llama-3.2-1b-preview",
        verbose=True,
        temperature=0.5,
        api_key="your_api_key_here"  # Replace with your actual API key
    )

    # Add nodes to the graph
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    # Compile the graph (this may include a checkpointer)
    graph = graph_builder.compile(checkpointer=memory)
    return graph, llm_model

# Emotion therapy function
def emotion_therapy(user_input: str):
    # Initialize the therapy agent and create the graph
    graph, llm_model = therapy_agent()
    
    # Retrieve messages from the state (conversation history)
    messages = [{"role": "user", "content": user_input}]  # Initial user message
    
    # Simulate a stream of messages from the graph (replace with actual stream logic)
    events = graph.stream(
        {"messages": messages},  # Send user input as part of the messages
        stream_mode="values"
    )

    # Collect messages from the event stream
    conversation = []
    for event in events:
        conversation.extend(event['messages'])  # Collect each event message

    # Extract the latest AI message from the response
    ai_messages = [msg for msg in conversation if 'content' in msg]
    
    return ai_messages[-1]['content'] if ai_messages else "No response from AI."  # Return the last AI message if available

# Streamlit interface
st.title("Emotion Therapy Chatbot")

# Initialize session state to store messages between interactions
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You**: {message['content']}")
    else:
        st.write(f"**AI**: {message['content']}")

# Get user input through Streamlit text input
user_input = st.text_input("Enter your message:")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get the AI response from the emotion therapy function
    result = emotion_therapy(user_input)
    
    # Add AI response to session state
    st.session_state.messages.append({"role": "AI", "content": result})
    
    # Rerun the app to show the updated conversation
    st.experimental_rerun()
