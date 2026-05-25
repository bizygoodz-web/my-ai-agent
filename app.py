import streamlit as st
from groq import Groq
import os

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
I can help you with:
- 💼 Career advice and resume tips
- 🤖 AI agent frameworks and tools
- 💻 Python and backend development
- 🔍 Any question you have!
""")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI agent built by Tirumalarao Kilari, an AI Engineer based in Pflugerville, TX. You specialize in AI agents, prompt engineering, RAG systems, Python development, and career advice. Be helpful, concise, and friendly."
                    },
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
                ]
            )
            answer = response.choices[0].message.content
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("---")
st.caption("Built by Tirumalarao Kilari · AI Engineer · Pflugerville, TX")
