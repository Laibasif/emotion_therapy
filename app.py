def therapy_agent():
    # Define START and END to mark the beginning and end of the graph flow
    START = "start"
    END = "end"

    graph_builder = StateGraph()  # Remove the argument here
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
