# Filename: rag_agent.py
# Description:
#   This module defines a simple retrieval-augmented generation (RAG) flow
#   using LangGraph and a knowledge base (e.g., vector database).
#   The model uses OpenAI-compatible LLMs and is suitable for medical Q&A systems.

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Optional, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# Initialize OpenAI chat model
chat_model = ChatOpenAI(model="gpt-4", temperature=0.5)

# Define the graph state structure
class BaseRagState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    history: Optional[List[BaseMessage]]
    question: str
    docs: str  # Simulated docs, replace with real vector search in production

# Simulate KB retrieval (replace with FAISS or other vector DB)
def retrieve_node(state: BaseRagState):
    fake_doc = "This is a simulated medical knowledge base result."
    state["docs"] = fake_doc
    return {"docs": fake_doc}

# Respond using knowledge
def response_node(state: BaseRagState):
    prompt = f"Using the following knowledge:
{state['docs']}

Answer the question:
{state['question']}"
    response = chat_model.invoke([HumanMessage(content=prompt)])
    return {"messages": [AIMessage(content=response.content)]}

# Build the RAG flow graph
def gen_rag_graph(chat_model):
    graph = StateGraph(BaseRagState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("respond", response_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", END)
    return graph
