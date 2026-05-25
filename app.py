import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import os
import json

st.set_page_config(
    page_title="Tirumalarao's AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Tirumalarao's AI Agent")
st.caption("AI Engineer · Prompt Engineer · RAG Systems Builder")
st.markdown("---")

st.markdown("""
**Hi! I am an AI agent built by Tirumalarao Kilari.**
I can search the web in real time and answer anything!
""")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information, news, jobs, or any topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def web_search(query):
    results = DDGS().text(query, max_results=4)
    output = ""
    for r in results:
        output += f"Title: {r['title']}\nSummary: {r['body']}\n\n"
    return output

def run_agent(user_message, history):
    messages = [
        {
            "role": "system",
            "content": "You are an expert AI agent built by Tirumalarao Kilari, an AI Engineer in Pflugerville TX. You have web search capability. Always search for current information when asked about news, jobs, prices, events, or anything that changes over time. Be helpful, concise, and friendly."
        }
    ]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    while True:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                query = json.loads(tool_call.function.arguments)["query"]
                st.info(f"🔍 Searching: {query}")
                result = web_search(query)
                messages.append({"role": "assistant", "content": None, "tool_calls": msg.tool_calls})
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            return msg.content

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me anything — I can search the web!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = run_agent(user_input, st.session_state.messages[:-1])
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.caption("Built by Tirumalarao Kilari · AI Engineer · Pflugerville, TX")
