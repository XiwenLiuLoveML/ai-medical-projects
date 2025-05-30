# Filename: medical_keywords_extract.py
# Description:
#   This module extracts medical keywords from user input using an LLM (OpenAI).
#   The extracted keywords are intended for use with a RAG (Retrieval-Augmented Generation) pipeline
#   in a controlled, offline medical knowledge base.

import json
from datetime import date
from typing import Annotated, Union
from typing_extensions import TypedDict

from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Initialize OpenAI model (requires OPENAI_API_KEY env variable)
llm = ChatOpenAI(temperature=0.2, model="gpt-4", max_tokens=512)

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]

async def medical_keywords_extract(state: GraphState) -> GraphState:
    """Use LLM to extract medical-specific keywords from the user query."""
    today = date.today().strftime("%Y-%m-%d")
    query = state['messages'][-1].content + f" Current date: {today}"

    prompt = ChatPromptTemplate.from_messages([
        ('system', (
            "You are a medical assistant that helps extract medical-related keywords from user questions.
"
            "Your goal is to identify relevant terms for searching a structured medical knowledge base.
"
            "Please extract 3-6 concise keywords or short phrases that capture the key clinical concepts.
"
            "Use JSON format: a list of strings.

"
            "Examples:
"
            "- Input: 'What is the best hypertension medication for elderly women with diabetes?'
"
            "  Output: ["hypertension", "elderly women", "diabetes", "blood pressure medication"]
"
            "- Input: 'How to treat stage 3 chronic kidney disease?'
"
            "  Output: ["stage 3", "chronic kidney disease", "CKD", "treatment"]
"
            "If you cannot extract meaningful keywords, return []"
        )),
        ('user', '{query}')
    ])

    chain = prompt | llm

    try:
        result = chain.invoke({'query': query})
        return {'messages': result}
    except Exception as e:
        return {'messages': [HumanMessage(content=f"[] # Error: {str(e)}")]}

def create_graph():
    graph_builder = StateGraph(GraphState)
    graph_builder.add_node('extract_keywords', medical_keywords_extract)
    graph_builder.add_edge(START, 'extract_keywords')
    graph_builder.add_edge('extract_keywords', END)
    return graph_builder.compile()

keywords_graph = create_graph()

async def extract_medical_keywords(query: str, session_id: str) -> Union[list[str], None]:
    """Public entry point to generate medical keywords from user input."""
    messages = {'messages': [HumanMessage(content=query)]}
    config = {'configurable': {'thread_id': session_id}}

    async for output in keywords_graph.astream(messages, config, stream_mode='values'):
        content = output['messages'][-1].content.strip()

    try:
        keywords = json.loads(content)
        if isinstance(keywords, list):
            return keywords
    except json.JSONDecodeError:
        return None
    return None
